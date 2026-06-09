# Benchmarking quantum circuit simulators
# Companion script for the "Benchmarking Quantum Circuit Simulators" tutorial.
#
# We describe ONE unoptimized circuit as a neutral list of gates, hand that exact
# same circuit to five different simulators, and time how long each takes to run it.
# Then we watch how that time grows as we add qubits and as we make the circuit deeper.
#
# The five simulators: Qiskit Aer, Cirq, PennyLane (default.qubit), Qibo, Amazon Braket.

import time
import csv
import statistics
import warnings
import numpy as np
import matplotlib.pyplot as plt

warnings.filterwarnings("ignore")

# Benchmark parameters
seed = 1234
warmups = 1          # Throw-away runs so caching / JIT does not pollute the first timing
repeats = 5          # Timed runs; we report the median
qubit_sweep = [10, 12, 14, 16]   # Vary the number of qubits at fixed depth
depth_sweep = [5, 10, 20, 40]    # Vary the depth at fixed number of qubits
fixed_depth = 10                 # Depth used while sweeping qubits
fixed_qubits = 12                # Qubits used while sweeping depth


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
            elif gate[0] == "rz":
                qml.RZ(gate[2], wires=gate[1])
            elif gate[0] == "cx":
                qml.CNOT(wires=[gate[1], gate[2]])
        return qml.state()

    node = qml.QNode(circuit, device)
    return lambda: node()


def run_qibo(gates, num_qubits):
    from qibo import Circuit, gates as qibo_gates
    circuit = Circuit(num_qubits)
    for gate in gates:
        if gate[0] == "rx":
            circuit.add(qibo_gates.RX(gate[1], theta=gate[2]))
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
        elif gate[0] == "rz":
            circuit.rz(gate[1], gate[2])
        elif gate[0] == "cx":
            circuit.cnot(gate[1], gate[2])
    circuit.state_vector()
    device = LocalSimulator("braket_sv")
    return lambda: device.run(circuit).result()


# Each simulator is registered by name, the way ucc-bench registers its compilers
simulators = {
    "qiskit_aer": run_qiskit_aer,
    "cirq": run_cirq,
    "pennylane": run_pennylane,
    "qibo": run_qibo,
    "braket": run_braket,
}


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
        execute = builder(gates, num_qubits)
        row[name] = time_run(execute)
    return row


def run_sweep(label, points):
    print("\n%s" % label)
    header = "  %-7s %-7s " % ("qubits", "depth") + " ".join("%-11s" % n for n in simulators)
    print(header)
    rows = []
    for num_qubits, depth in points:
        row = benchmark_point(num_qubits, depth)
        rows.append(row)
        times = " ".join("%9.4fs" % row[n] for n in simulators)
        print("  %-7d %-7d %s" % (num_qubits, depth, times))
    return rows


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


def save_csv(rows, out_file):
    fieldnames = ["qubits", "depth"] + list(simulators)
    with open(out_file, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print("Saved %d rows to %s" % (len(rows), out_file))


if __name__ == "__main__":
    qubit_rows = run_sweep(
        "Scaling with qubit count (depth = %d)" % fixed_depth,
        [(n, fixed_depth) for n in qubit_sweep])
    depth_rows = run_sweep(
        "Scaling with circuit depth (qubits = %d)" % fixed_qubits,
        [(fixed_qubits, d) for d in depth_sweep])

    save_csv(qubit_rows, "results_qubits.csv")
    save_csv(depth_rows, "results_depth.csv")
    plot_sweep(qubit_rows, "qubits", "Number of qubits",
               "output_qubit_scaling.png",
               "Execution time vs qubit count (depth = %d)" % fixed_depth)
    plot_sweep(depth_rows, "depth", "Circuit depth",
               "output_depth_scaling.png",
               "Execution time vs circuit depth (qubits = %d)" % fixed_qubits)
