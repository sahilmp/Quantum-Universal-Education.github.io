---
title: "Benchmarking Quantum Circuit Simulators: One Circuit, Five Backends"
categories:
  - Blog
tags:
  - tutorial
  - benchmarking
  - simulators
  - Qiskit
  - Cirq
  - PennyLane
  - Qibo
  - Amazon Braket
  - UCC
  - unitaryHACK
  - quantum computing
author:
  - Abhiyan Ampally
---

<script src="https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML" type="text/javascript"></script>

A quantum *simulator* is an ordinary classical program that pretends to be a quantum computer: you hand it a circuit and it computes what the qubits would do. There are many simulators to choose from, and they are not equally fast. In this tutorial we take **one and the same circuit**, run it on **five different simulators**, and measure how long each one takes &mdash; and, crucially, how that time grows as we add qubits and make the circuit deeper. This tutorial is written for high school and undergraduate students; all you need is a little Python.

## Why Simulating Quantum Circuits Is Hard

A classical computer stores the full state of $$n$$ qubits as a list of complex numbers called the **statevector**. The catch is its length: a system of $$n$$ qubits needs

$$
    2^{n}
$$

complex amplitudes. Ten qubits is $$2^{10} = 1024$$ numbers, which is nothing. But every extra qubit *doubles* the memory, so 20 qubits is about a million amplitudes, 30 qubits is a billion, and 40 qubits already needs more memory than most supercomputers have. Worse, every gate has to update the whole statevector, so the time to apply a circuit of $$g$$ gates grows roughly like

$$
    \text{time} \approx O(g \cdot 2^{n}).
$$

That exponential $$2^{n}$$ is exactly why quantum computers are interesting (they avoid it) and why simulators get slow. Benchmarking shows us *where* the wall is for each tool.

## The Benchmarking Goal

We borrow our methodology from [UCC](https://github.com/unitaryfoundation/ucc) and its companion benchmarking suite [ucc-bench](https://github.com/unitaryfoundation/ucc-bench), built by [Unitary Foundation](https://unitary.foundation/). Their golden rule is simple and we follow it here:

> Feed the **exact same circuit** to every backend, measure one well-defined number, and report it in a structured, reproducible way.

For us the "one number" is the median wall-clock time to run an *unoptimized* circuit &mdash; we do **not** let any simulator compile or simplify it first, so all five do the same work. We then repeat the measurement across a range of qubit counts and depths to see how each simulator *scales*.

## The Five Simulators

All five are open-source and listed in the [QOSF list of quantum simulators](https://qosf.org/project_list/#quantum-simulators):

- **[Qiskit Aer](https://github.com/Qiskit/qiskit-aer)** &mdash; IBM's high-performance simulator, with a C++ statevector engine.
- **[Cirq](https://quantumai.google/cirq)** &mdash; Google's framework and its built-in `Simulator`.
- **[PennyLane](https://pennylane.ai/)** &mdash; Xanadu's library, using its `default.qubit` device.
- **[Qibo](https://qibo.science/)** &mdash; an open framework here using its NumPy backend.
- **[Amazon Braket](https://github.com/amazon-braket/amazon-braket-sdk-python)** &mdash; AWS's SDK and its `LocalSimulator` (`braket_sv`), which runs on your own machine.

## One Circuit for Everyone

To be fair, every simulator must run the *identical* circuit. The trap is that each library has its own way of writing a circuit, so it is easy to accidentally build five slightly different ones. We avoid that by describing the circuit **once**, as a neutral list of plain tuples, and letting each simulator translate that single description.

```python
import numpy as np

seed = 1234

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
```

A gate like `("rx", 3, 1.57)` means "apply an X-rotation of 1.57 radians to qubit 3", and `("cx", 0, 1)` means "apply a CNOT from qubit 0 to qubit 1". Fixing the random `seed` makes the circuit reproducible, so you get the same circuit every time you run the script.

## Timing Fairly

Two small tricks keep the timings honest. First, we do a **warm-up** run that we throw away, because the very first call to a simulator often pays one-time costs (imports, caching, just-in-time compilation). Second, we run the circuit several times and report the **median**, which ignores the occasional unlucky slow run.

```python
import time
import statistics

warmups = 1
repeats = 5

def time_run(execute):
    for _ in range(warmups):
        execute()
    samples = []
    for _ in range(repeats):
        start = time.perf_counter()
        execute()
        samples.append(time.perf_counter() - start)
    return statistics.median(samples)
```

## Running on Each Simulator

Now one small function per simulator. Each takes our neutral gate list, builds the circuit in that library's own language, and returns a function that runs it and produces the final statevector. Here are two of the five; the rest follow the same shape and are in the [full script](/assets/quantum_programs/quantum_simulation_benchmarking/benchmark_simulators.py).

```python
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
```

We register all five by name, the way ucc-bench keeps a registry of backends:

```python
simulators = {
    "qiskit_aer": run_qiskit_aer,
    "cirq": run_cirq,
    "pennylane": run_pennylane,
    "qibo": run_qibo,
    "braket": run_braket,
}
```

## Results: Scaling with Qubit Count

First we hold the depth fixed at 10 layers and grow the circuit from 10 to 16 qubits. Every number below is the median execution time in seconds, measured on a laptop (your absolute numbers will differ, but the *shapes* of the curves will not):

| Qubits | qiskit_aer | cirq | pennylane | qibo | braket |
|:------:|:----------:|:----:|:---------:|:----:|:------:|
| 10 | 0.0108 | 0.0224 | 0.0238 | 0.0055 | 0.0973 |
| 12 | 0.0106 | 0.0279 | 0.0360 | 0.0115 | 0.1215 |
| 14 | 0.0272 | 0.0391 | 0.0538 | 0.0357 | 0.1838 |
| 16 | 0.0525 | 0.0795 | 0.1049 | 0.2299 | 0.1841 |

![png](/assets/quantum_programs/quantum_simulation_benchmarking/output_qubit_scaling.png)

The vertical axis is on a log scale, so a straight line means the time is multiplying by a constant factor with every step &mdash; that is the $$2^{n}$$ growth showing up as a roughly straight climb.

## Results: Scaling with Circuit Depth

Next we hold the qubit count fixed at 12 and make the circuit deeper, from 5 to 40 layers:

| Depth | qiskit_aer | cirq | pennylane | qibo | braket |
|:-----:|:----------:|:----:|:---------:|:----:|:------:|
| 5  | 0.0054 | 0.0125 | 0.0188 | 0.0058 | 0.0607 |
| 10 | 0.0103 | 0.0314 | 0.0339 | 0.0116 | 0.1299 |
| 20 | 0.0204 | 0.0566 | 0.0690 | 0.0236 | 0.2415 |
| 40 | 0.0432 | 0.1053 | 0.1391 | 0.0485 | 1.4170 |

![png](/assets/quantum_programs/quantum_simulation_benchmarking/output_depth_scaling.png)

Here the growth is **linear** in depth (doubling the gates roughly doubles the time), which matches the $$O(g \cdot 2^{n})$$ formula: at a fixed qubit count, the $$2^{n}$$ factor is constant and only the gate count $$g$$ changes.

## What the Numbers Tell Us

- **No simulator wins everywhere.** Qibo's NumPy backend is the fastest at 10 qubits but the slowest at 16, while Qiskit Aer starts modestly and scales the best. The only way to know which tool fits *your* problem is to measure it &mdash; which is the whole point of benchmarking.
- **Constant overhead matters at small sizes.** Braket's `LocalSimulator` is consistently the slowest here, dominated by a fixed per-run cost rather than the circuit itself; notice it changes the least as we add qubits.
- **Depth is cheaper than width.** Going from depth 5 to 40 (eight times the gates) costs at most about eight times the time. Adding six qubits costs far more, because each qubit *doubles* the work. If you have a choice, a deep narrow circuit simulates faster than a shallow wide one.

## Dependencies

Everything runs locally on CPU. Create a fresh environment and install:

```bash
pip install qiskit qiskit-aer cirq pennylane qibo amazon-braket-sdk matplotlib numpy
```

The versions used to produce the numbers above were Qiskit Aer 0.17, Cirq 1.6, PennyLane 0.45, Qibo 0.3, and Amazon Braket SDK 1.118, on Python 3.12. A ready-made [`requirements.txt`](/assets/quantum_programs/quantum_simulation_benchmarking/requirements.txt) is included. Then run:

```bash
cd assets/quantum_programs/quantum_simulation_benchmarking
pip install -r requirements.txt
python benchmark_simulators.py
```

The script prints both tables, writes `results_qubits.csv` and `results_depth.csv`, and saves the two plots. There is also a [Jupyter notebook](/assets/quantum_programs/quantum_simulation_benchmarking/benchmark_simulators.ipynb) version if you prefer to run it cell by cell.

## A Short Demo

This is the qubit-scaling plot being drawn one measurement at a time &mdash; watch the simulators spread apart as the circuits get wider:

![demo](/assets/quantum_programs/quantum_simulation_benchmarking/demo.gif)

## How I Got Started

I got into quantum computing the slightly backwards way: through *code*, not equations. The first time I ran a Bell-state circuit on a simulator and saw the `00` and `11` outcomes appear with no `01` or `10`, I was hooked &mdash; I could *see* entanglement happen in a few lines of Python before I fully understood the math behind it. Benchmarking became my favourite way to learn, because it forced me to actually run things instead of just reading about them. If you are starting out, my advice is to pick one small circuit, run it five different ways like we did here, and stay curious about *why* the numbers come out the way they do. You do not need a quantum computer or a physics degree to begin &mdash; a laptop and a bit of stubbornness are enough.

## Use of AI

I used an AI assistant (Anthropic's Claude) as a co-pilot to help draft and organize this write-up and to scaffold the boilerplate in the benchmark script. Every benchmark in this tutorial was actually executed by me in the environment described above, and all the numbers, tables, and plots are real measurements from those runs &mdash; not generated text. The explanations were reviewed and edited by hand for correctness.

## References

[1] Unitary Foundation. (2024). [UCC: Unitary Compiler Collection](https://github.com/unitaryfoundation/ucc).

[2] Unitary Foundation. (2024). [ucc-bench: Quantum Compiler Benchmarking Suite](https://github.com/unitaryfoundation/ucc-bench).

[3] Javadi-Abhari, A., et al. (2024). Quantum computing with Qiskit. arXiv preprint arXiv:2405.08810.

[4] Developers of Cirq. (2024). [Cirq](https://quantumai.google/cirq), Google Quantum AI.

[5] Bergholm, V., et al. (2018). PennyLane: Automatic differentiation of hybrid quantum-classical computations. arXiv preprint arXiv:1811.04968.

[6] Efthymiou, S., et al. (2021). Qibo: a framework for quantum simulation with hardware acceleration. Quantum Science and Technology, 7(1), 015018.

[7] Nielsen, M. A., & Chuang, I. L. (2010). Quantum Computation and Quantum Information. Cambridge University Press.

## Author
Abhiyan Ampally
