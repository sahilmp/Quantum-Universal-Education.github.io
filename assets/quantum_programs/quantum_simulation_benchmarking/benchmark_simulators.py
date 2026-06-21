# Benchmarking quantum circuit simulators
# Companion script for the "Benchmarking Quantum Circuit Simulators" tutorial.
#
# We describe ONE unoptimized circuit as a neutral list of gates, hand that exact
# same circuit to five different simulators, and time how long each takes to run it.
# Then we look at three things:
#   1. how the time scales as we add qubits and depth,
#   2. how much memory a statevector needs (the 2^n wall),
#   3. whether compiling the circuit with UCC first makes it simulate faster.
#
# The five simulators: Qiskit Aer, Cirq, PennyLane (default.qubit), Qibo, Amazon Braket.

# Pin every backend to a single thread BEFORE numpy loads, so the comparison is fair
# (Qiskit Aer would otherwise use every core while the pure-Python sims use one).
import os
for _var in ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[_var] = "1"

import time
import csv
import statistics
import tracemalloc
import warnings
import numpy as np
import matplotlib.pyplot as plt

warnings.filterwarnings("ignore")

# Benchmark parameters
seed = 1234
warmups = 2          # Throw-away runs so caching / JIT does not pollute the first timing
repeats = 5          # Timed runs; we report the median
qubit_sweep = [10, 12, 14, 16, 18]   # Vary qubits at fixed depth
depth_sweep = [5, 10, 20, 40]        # Vary depth at fixed qubits
memory_sweep = [10, 14, 18, 22, 24]  # Statevector memory only (no simulation cost)
fixed_depth = 10
fixed_qubits = 12
ucc_sizes = [12, 14, 16]             # Quantum Volume sizes for the compilation test


def build_gate_list(num_qubits, depth):
    # The same circuit for everyone, written as plain tuples so no simulator is favoured.
    # Each layer is a wall of single-qubit rotations followed by a ladder of CNOTs.
    rng = np.random.default_rng(seed)
    gates = []
    for _ in range(depth):
        for q in range(num_qubits):
            gates.append(("rx", q, float(rng.uniform(0, 2 * np.pi))))
            gates.append(("rz", q, float(rng.uniform(0, 2 * np.pi))))
        for q in range(num_qubits - 1):
            gates.append(("cx", q, q + 1))
    return gates


def run_qiskit_aer(gates, num_qubits):
    from qiskit import QuantumCircuit
    from qiskit_aer import AerSimulator
    circuit = QuantumCircuit(num_qubits)
    for gate in gates:
        if gate[0] == "rx":
            circuit.rx(gate[2], gate[1])
        elif gate[0] == "ry":
            circuit.ry(gate[2], gate[1])
        elif gate[0] == "rz":
            circuit.rz(gate[2], gate[1])
        elif gate[0] == "cx":
            circuit.cx(gate[1], gate[2])
    circuit.save_statevector()
    simulator = AerSimulator(method="statevector")
    return lambda: simulator.run(circuit).result()


def run_cirq(gates, num_qubits):
    import cirq
    qubits = cirq.LineQubit.range(num_qubits)
    circuit = cirq.Circuit()
    for gate in gates:
        if gate[0] == "rx":
            circuit.append(cirq.rx(gate[2]).on(qubits[gate[1]]))
        elif gate[0] == "ry":
            circuit.append(cirq.ry(gate[2]).on(qubits[gate[1]]))
        elif gate[0] == "rz":
            circuit.append(cirq.rz(gate[2]).on(qubits[gate[1]]))
        elif gate[0] == "cx":
            circuit.append(cirq.CNOT(qubits[gate[1]], qubits[gate[2]]))
    simulator = cirq.Simulator()
    return lambda: simulator.simulate(circuit)


def run_pennylane(gates, num_qubits):
    import pennylane as qml
    device = qml.device("default.qubit", wires=num_qubits)

    def circuit():
        for gate in gates:
            if gate[0] == "rx":
                qml.RX(gate[2], wires=gate[1])
            elif gate[0] == "ry":
                qml.RY(gate[2], wires=gate[1])
            elif gate[0] == "rz":
                qml.RZ(gate[2], wires=gate[1])
            elif gate[0] == "cx":
                qml.CNOT(wires=[gate[1], gate[2]])
        return qml.state()

    node = qml.QNode(circuit, device)
    return lambda: node()


def run_qibo(gates, num_qubits):
    from qibo import Circuit, gates as qibo_gates, set_backend
    set_backend("numpy")
    circuit = Circuit(num_qubits)
    for gate in gates:
        if gate[0] == "rx":
            circuit.add(qibo_gates.RX(gate[1], theta=gate[2]))
        elif gate[0] == "ry":
            circuit.add(qibo_gates.RY(gate[1], theta=gate[2]))
        elif gate[0] == "rz":
            circuit.add(qibo_gates.RZ(gate[1], theta=gate[2]))
        elif gate[0] == "cx":
            circuit.add(qibo_gates.CNOT(gate[1], gate[2]))
    return lambda: circuit()


def run_braket(gates, num_qubits):
    from braket.circuits import Circuit
    from braket.devices import LocalSimulator
    circuit = Circuit()
    for gate in gates:
        if gate[0] == "rx":
            circuit.rx(gate[1], gate[2])
        elif gate[0] == "ry":
            circuit.ry(gate[1], gate[2])
        elif gate[0] == "rz":
            circuit.rz(gate[1], gate[2])
        elif gate[0] == "cx":
            circuit.cnot(gate[1], gate[2])
    circuit.state_vector()
    device = LocalSimulator("braket_sv")
    return lambda: device.run(circuit).result()


# Each simulator is registered by name, the way ucc-bench registers its backends
simulators = {
    "qiskit_aer": run_qiskit_aer,
    "cirq": run_cirq,
    "pennylane": run_pennylane,
    "qibo": run_qibo,
    "braket": run_braket,
}


# --- correctness: do the five simulators actually agree? ----------------------

# Qiskit numbers qubits one way and the others the opposite way, so to compare
# statevectors we put them all in Qiskit's order by reversing the qubit axis.
reversed_qubit_order = {"cirq", "pennylane", "qibo", "braket"}


def to_qiskit_order(state, name, num_qubits):
    state = np.asarray(state).ravel().astype(complex)
    if name in reversed_qubit_order:
        state = state.reshape([2] * num_qubits).transpose(range(num_qubits - 1, -1, -1)).ravel()
    return state / np.linalg.norm(state)


def final_state(name, gates, num_qubits):
    # Run the circuit on one simulator and pull out the final statevector
    if name == "qiskit_aer":
        from qiskit import QuantumCircuit
        from qiskit_aer import AerSimulator
        circuit = QuantumCircuit(num_qubits)
        for gate in gates:
            if gate[0] == "rx":
                circuit.rx(gate[2], gate[1])
            elif gate[0] == "rz":
                circuit.rz(gate[2], gate[1])
            elif gate[0] == "cx":
                circuit.cx(gate[1], gate[2])
        circuit.save_statevector()
        result = AerSimulator(method="statevector").run(circuit).result()
        state = result.get_statevector().data
    elif name == "cirq":
        import cirq
        qubits = cirq.LineQubit.range(num_qubits)
        circuit = cirq.Circuit()
        for gate in gates:
            if gate[0] == "rx":
                circuit.append(cirq.rx(gate[2]).on(qubits[gate[1]]))
            elif gate[0] == "rz":
                circuit.append(cirq.rz(gate[2]).on(qubits[gate[1]]))
            elif gate[0] == "cx":
                circuit.append(cirq.CNOT(qubits[gate[1]], qubits[gate[2]]))
        state = cirq.Simulator().simulate(circuit).final_state_vector
    elif name == "pennylane":
        import pennylane as qml
        device = qml.device("default.qubit", wires=num_qubits)

        def circuit():
            for gate in gates:
                if gate[0] == "rx":
                    qml.RX(gate[2], wires=gate[1])
                elif gate[0] == "rz":
                    qml.RZ(gate[2], wires=gate[1])
                elif gate[0] == "cx":
                    qml.CNOT(wires=[gate[1], gate[2]])
            return qml.state()

        state = qml.QNode(circuit, device)()
    elif name == "qibo":
        from qibo import Circuit, gates as qibo_gates, set_backend
        set_backend("numpy")
        circuit = Circuit(num_qubits)
        for gate in gates:
            if gate[0] == "rx":
                circuit.add(qibo_gates.RX(gate[1], theta=gate[2]))
            elif gate[0] == "rz":
                circuit.add(qibo_gates.RZ(gate[1], theta=gate[2]))
            elif gate[0] == "cx":
                circuit.add(qibo_gates.CNOT(gate[1], gate[2]))
        state = circuit().state()
    elif name == "braket":
        from braket.circuits import Circuit
        from braket.devices import LocalSimulator
        circuit = Circuit()
        for gate in gates:
            if gate[0] == "rx":
                circuit.rx(gate[1], gate[2])
            elif gate[0] == "rz":
                circuit.rz(gate[1], gate[2])
            elif gate[0] == "cx":
                circuit.cnot(gate[1], gate[2])
        circuit.state_vector()
        state = LocalSimulator("braket_sv").run(circuit).result().values[0]
    return to_qiskit_order(state, name, num_qubits)


def check_agreement(num_qubits, depth):
    # A benchmark you can trust: confirm every simulator computes the SAME state.
    # Fidelity |<a|b>|^2 should be 1 (it ignores an irrelevant global phase).
    gates = build_gate_list(num_qubits, depth)
    reference = final_state("qiskit_aer", gates, num_qubits)
    worst = 1.0
    for name in simulators:
        state = final_state(name, gates, num_qubits)
        fidelity = abs(np.vdot(reference, state)) ** 2
        worst = min(worst, fidelity)
        print("  %-11s fidelity vs qiskit_aer = %.12f" % (name, fidelity))
    print("  -> all five agree (largest infidelity %.1e)" % (1 - worst))


def time_run(execute):
    # Warm up, then return the median wall-clock time over several timed runs
    for _ in range(warmups):
        execute()
    samples = []
    for _ in range(repeats):
        start = time.perf_counter()
        execute()
        samples.append(time.perf_counter() - start)
    return statistics.median(samples)


def benchmark_point(num_qubits, depth):
    gates = build_gate_list(num_qubits, depth)
    row = {"qubits": num_qubits, "depth": depth}
    for name, builder in simulators.items():
        row[name] = time_run(builder(gates, num_qubits))
    return row


def statevector_memory(num_qubits):
    # Peak memory of the 2^n complex amplitudes a statevector simulator must store
    tracemalloc.start()
    state = np.zeros(2 ** num_qubits, dtype=complex)
    state[0] = 1.0
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    del state
    return peak / 1e6  # megabytes


# --- UCC compilation helpers ---------------------------------------------------

def flatten_to_gate_list(circuit):
    # Rewrite a Qiskit circuit into the rz/ry/cx gate set our simulators all speak,
    # then read it back out as our neutral tuple list.
    from qiskit import transpile
    flat = transpile(circuit, basis_gates=["rz", "ry", "cx"], optimization_level=0)
    gates = []
    for instruction in flat.data:
        name = instruction.operation.name
        wires = [flat.find_bit(q).index for q in instruction.qubits]
        params = instruction.operation.params
        if name in ("rz", "ry"):
            gates.append((name, wires[0], float(params[0])))
        elif name == "cx":
            gates.append(("cx", wires[0], wires[1]))
    return gates


def ucc_compilation_point(num_qubits):
    # Compare simulating a Quantum Volume circuit before and after UCC compilation
    from qiskit.circuit.library import quantum_volume
    from ucc import compile as ucc_compile
    circuit = quantum_volume(num_qubits, seed=seed)
    raw_gates = flatten_to_gate_list(circuit)
    compiled_gates = flatten_to_gate_list(ucc_compile(circuit))
    row = {
        "qubits": num_qubits,
        "raw_gates": len(raw_gates),
        "compiled_gates": len(compiled_gates),
    }
    for name, builder in simulators.items():
        row[name + "_raw"] = time_run(builder(raw_gates, num_qubits))
        row[name + "_compiled"] = time_run(builder(compiled_gates, num_qubits))
    return row


# --- runners ------------------------------------------------------------------

def run_scaling_sweep(label, points):
    print("\n%s" % label)
    print("  %-7s %-7s " % ("qubits", "depth") + " ".join("%-11s" % n for n in simulators))
    rows = []
    for num_qubits, depth in points:
        row = benchmark_point(num_qubits, depth)
        rows.append(row)
        print("  %-7d %-7d %s" % (num_qubits, depth,
              " ".join("%9.4fs" % row[n] for n in simulators)))
    return rows


def save_csv(rows, fieldnames, out_file):
    with open(out_file, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print("Saved %d rows to %s" % (len(rows), out_file))


def plot_sweep(rows, x_key, x_label, out_file, title):
    x_values = [row[x_key] for row in rows]
    for name in simulators:
        plt.plot(x_values, [row[name] for row in rows], marker="o", label=name)
    plt.yscale("log")
    plt.xlabel(x_label)
    plt.ylabel("Median execution time (s, log scale)")
    plt.title(title)
    plt.legend()
    plt.savefig(out_file, dpi=120, bbox_inches="tight")
    plt.close()
    print("Saved plot to %s" % out_file)


def gates_in_circuit(num_qubits, depth):
    # Two single-qubit rotations per qubit plus an (n-1)-long CNOT ladder, per layer
    return depth * (2 * num_qubits + (num_qubits - 1))


def fit_scaling(qubit_rows, depth):
    # Fit time ~ C * (gates * 2^n) + overhead, then predict where each simulator
    # crosses one second, one minute, and runs out of 16 GB of memory.
    ram_bytes = 16e9
    work = np.array([gates_in_circuit(r["qubits"], depth) * 2 ** r["qubits"] for r in qubit_rows])
    rows = []
    print("\nScaling fit  (time ~ C * gates * 2^n)   and predictions")
    print("  %-11s %-10s %-6s %-8s %-9s %-9s" % ("simulator", "C", "R^2", "1 second", "1 minute", "16GB OOM"))
    for name in simulators:
        times = np.array([r[name] for r in qubit_rows])
        slope, intercept = np.polyfit(work, times, 1)
        predicted = slope * work + intercept
        r_squared = 1 - np.sum((times - predicted) ** 2) / np.sum((times - times.mean()) ** 2)

        def qubits_for(target):
            for n in range(8, 41):
                if slope * gates_in_circuit(n, depth) * 2 ** n + intercept >= target:
                    return n
            return 40
        oom = next(n for n in range(8, 60) if 2 ** n * 16 > ram_bytes)
        row = {"simulator": name, "C": slope, "r_squared": r_squared,
               "one_second_qubits": qubits_for(1.0), "one_minute_qubits": qubits_for(60.0),
               "oom_qubits": oom}
        rows.append(row)
        print("  %-11s %.2e   %.3f  %-8d %-9d %-9d"
              % (name, slope, r_squared, row["one_second_qubits"],
                 row["one_minute_qubits"], oom))
    return rows


if __name__ == "__main__":
    # 0. A benchmark you can trust: confirm every simulator computes the same state
    print("Correctness check (8 qubits, depth 5)")
    check_agreement(8, 5)

    # 1. Scaling with qubit count and with depth
    qubit_rows = run_scaling_sweep(
        "Scaling with qubit count (depth = %d)" % fixed_depth,
        [(n, fixed_depth) for n in qubit_sweep])
    depth_rows = run_scaling_sweep(
        "Scaling with circuit depth (qubits = %d)" % fixed_qubits,
        [(fixed_qubits, d) for d in depth_sweep])

    save_csv(qubit_rows, ["qubits", "depth"] + list(simulators), "results_qubits.csv")
    save_csv(depth_rows, ["qubits", "depth"] + list(simulators), "results_depth.csv")
    plot_sweep(qubit_rows, "qubits", "Number of qubits", "output_qubit_scaling.png",
               "Execution time vs qubit count (depth = %d)" % fixed_depth)
    plot_sweep(depth_rows, "depth", "Circuit depth", "output_depth_scaling.png",
               "Execution time vs circuit depth (qubits = %d)" % fixed_qubits)

    # 2. The memory wall
    print("\nStatevector memory")
    memory_rows = []
    for num_qubits in memory_sweep:
        megabytes = statevector_memory(num_qubits)
        memory_rows.append({"qubits": num_qubits, "memory_mb": megabytes})
        print("  %2d qubits -> %9.1f MB" % (num_qubits, megabytes))
    save_csv(memory_rows, ["qubits", "memory_mb"], "results_memory.csv")
    plt.plot([r["qubits"] for r in memory_rows], [r["memory_mb"] for r in memory_rows], marker="o")
    plt.yscale("log")
    plt.xlabel("Number of qubits")
    plt.ylabel("Statevector memory (MB, log scale)")
    plt.title("Memory needed to store the statevector")
    plt.savefig("output_memory_scaling.png", dpi=120, bbox_inches="tight")
    plt.close()
    print("Saved plot to output_memory_scaling.png")

    # 3. Does compiling with UCC make a circuit simulate faster?
    print("\nUCC compilation effect on Quantum Volume (raw -> compiled)")
    ucc_rows = []
    for num_qubits in ucc_sizes:
        row = ucc_compilation_point(num_qubits)
        ucc_rows.append(row)
        print("  %2d qubits: gates %4d -> %4d   aer %7.4fs -> %7.4fs   speedup x%.2f"
              % (num_qubits, row["raw_gates"], row["compiled_gates"],
                 row["qiskit_aer_raw"], row["qiskit_aer_compiled"],
                 row["qiskit_aer_raw"] / row["qiskit_aer_compiled"]))
    ucc_fields = ["qubits", "raw_gates", "compiled_gates"]
    for name in simulators:
        ucc_fields += [name + "_raw", name + "_compiled"]
    save_csv(ucc_rows, ucc_fields, "results_ucc.csv")

    # Plot the gate count, which is the clean reproducible win; wall-clock follows it
    # but is small and noisy at these sizes (see the CSV for the raw/compiled times).
    labels = [str(r["qubits"]) for r in ucc_rows]
    positions = range(len(labels))
    width = 0.35
    raw_counts = [r["raw_gates"] for r in ucc_rows]
    compiled_counts = [r["compiled_gates"] for r in ucc_rows]
    plt.bar([p - width / 2 for p in positions], raw_counts, width, label="raw")
    plt.bar([p + width / 2 for p in positions], compiled_counts, width, label="UCC compiled")
    plt.xticks(list(positions), labels)
    plt.xlabel("Number of qubits (Quantum Volume)")
    plt.ylabel("Gate count")
    plt.title("Gates a simulator must run, before vs after UCC compilation")
    plt.legend()
    plt.savefig("output_ucc_compilation.png", dpi=120, bbox_inches="tight")
    plt.close()
    print("Saved plot to output_ucc_compilation.png")

    # 4. Turn the qubit-scaling data into a predictive model
    scaling_rows = fit_scaling(qubit_rows, fixed_depth)
    save_csv(scaling_rows,
             ["simulator", "C", "r_squared", "one_second_qubits", "one_minute_qubits", "oom_qubits"],
             "results_scaling.csv")
