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

A quantum *simulator* is an ordinary classical program that pretends to be a quantum computer: you hand it a circuit and it works out what the qubits would do. There are lots of simulators and they are not equally fast. In this tutorial we take one circuit, run it on five different simulators, and measure how long each one takes. Then we go a bit further than a single table: we watch the time grow with qubit count and depth, see the memory wall that makes simulation hard in the first place, and check whether compiling the circuit with [UCC](https://github.com/unitaryfoundation/ucc) first makes it run faster. It is written for high school and undergraduate students, and everything runs on a laptop.

## Why Simulating Quantum Circuits Is Hard

A classical computer stores the state of $$n$$ qubits as a list of complex numbers called the **statevector**. The catch is its length: $$n$$ qubits need

$$
    2^{n}
$$

complex amplitudes. Ten qubits is $$2^{10} = 1024$$ numbers, nothing at all. But every extra qubit *doubles* the list, so 20 qubits is about a million amplitudes and 30 qubits is a billion. On top of that, every gate has to update the whole statevector, so the time to run a circuit of $$g$$ gates grows roughly like

$$
    \text{time} \approx O(g \cdot 2^{n}).
$$

That $$2^{n}$$ is the reason real quantum computers are interesting (they skip it) and the reason simulators eventually crawl. Benchmarking shows us where the wall sits for each tool.

## The Benchmarking Goal

The plan comes straight from [UCC](https://github.com/unitaryfoundation/ucc) and its companion suite [ucc-bench](https://github.com/unitaryfoundation/ucc-bench), both from [Unitary Foundation](https://unitary.foundation/). Their rule is simple, and we keep it: feed the exact same circuit to every backend, measure one clearly defined number, and report it so anyone can reproduce it. Our number is the median wall-clock time to run an *unoptimized* circuit. We never let a simulator quietly simplify the circuit first, so all five do the same work. Later we relax that and let UCC compile the circuit on purpose, to see if compilation pays off.

## The Five Simulators

All five are open source and appear in the [QOSF list of quantum simulators](https://qosf.org/project_list/#quantum-simulators):

- **[Qiskit Aer](https://github.com/Qiskit/qiskit-aer)**, IBM's high-performance simulator with a C++ statevector engine.
- **[Cirq](https://quantumai.google/cirq)**, Google's framework and its built-in `Simulator`.
- **[PennyLane](https://pennylane.ai/)**, Xanadu's library, using its `default.qubit` device.
- **[Qibo](https://qibo.science/)**, here using its plain NumPy backend.
- **[Amazon Braket](https://github.com/amazon-braket/amazon-braket-sdk-python)**, the AWS SDK and its `LocalSimulator` (`braket_sv`), which runs on your own machine.

## One Circuit for Everyone

To be fair, every simulator has to run the *identical* circuit. The trap is that each library writes circuits its own way, so it is easy to build five subtly different ones by accident. We avoid that by describing the circuit once, as a neutral list of plain tuples, and letting each simulator translate that single description.

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

A tuple like `("rx", 3, 1.57)` means "rotate qubit 3 by 1.57 radians about X", and `("cx", 0, 1)` is a CNOT from qubit 0 to qubit 1. Fixing the random `seed` makes the circuit identical on every run.

## Keeping the Comparison Fair

Two details matter a lot here. First, Qiskit Aer is written in C++ and will happily use every core on your machine, while the pure-Python simulators use one. If we let that happen we would be benchmarking the number of cores, not the simulators, so the script pins every backend to a single thread before NumPy loads:

```python
import os
for var in ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[var] = "1"
```

Second, the first call to a simulator pays one-time costs (imports, caching, just-in-time compilation), so we run a couple of warm-up rounds we throw away, then take the **median** of several timed runs.

```python
import time
import statistics

warmups = 2
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

Now one small function per simulator. Each takes our neutral gate list, builds the circuit in that library's own language, and returns a function that runs it to a statevector. Here are two of the five; the other three follow the same shape and live in the [full script](/assets/quantum_programs/quantum_simulation_benchmarking/benchmark_simulators.py).

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

def run_qibo(gates, num_qubits):
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
    return lambda: circuit()
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

First we hold the depth at 10 layers and grow the circuit from 10 to 18 qubits. Every number is the median time in seconds. These tables are exactly the contents of `results_qubits.csv` and `results_depth.csv` in the project folder, so you can rerun the script and check them (your absolute times will differ by machine and run, but the shapes hold).

| Qubits | qiskit_aer | cirq | pennylane | qibo | braket |
|:------:|:----------:|:----:|:---------:|:----:|:------:|
| 10 | 0.0062 | 0.0200 | 0.0241 | 0.0060 | 0.0931 |
| 12 | 0.0136 | 0.0307 | 0.0326 | 0.0136 | 0.1239 |
| 14 | 0.0327 | 0.0407 | 0.0501 | 0.0326 | 0.1482 |
| 16 | 0.0784 | 0.0846 | 0.1440 | 0.1425 | 0.2413 |
| 18 | 0.3248 | 0.3258 | 1.7972 | 1.6401 | 0.5105 |

![png](/assets/quantum_programs/quantum_simulation_benchmarking/output_qubit_scaling.png)

The vertical axis is a log scale, so a straight climb means the time keeps multiplying by a constant factor: that is the $$2^{n}$$ growth. Two stories stand out. Qiskit Aer and Cirq stay cheap as the circuit widens, while the pure-NumPy paths in PennyLane and Qibo shoot up past 16 qubits (1.8 and 1.6 seconds at 18 qubits, versus 0.32 for Aer). Braket starts the slowest because of a fixed per-run cost, but it grows gently.

## Results: Scaling with Circuit Depth

Next we hold the qubit count at 12 and make the circuit deeper, from 5 to 40 layers:

| Depth | qiskit_aer | cirq | pennylane | qibo | braket |
|:-----:|:----------:|:----:|:---------:|:----:|:------:|
| 5  | 0.0065 | 0.0150 | 0.0183 | 0.0060 | 0.0629 |
| 10 | 0.0118 | 0.0293 | 0.0344 | 0.0115 | 0.1209 |
| 20 | 0.0235 | 0.0600 | 0.0704 | 0.0238 | 0.3211 |
| 40 | 0.0414 | 0.1025 | 0.1336 | 0.0491 | 0.6805 |

![png](/assets/quantum_programs/quantum_simulation_benchmarking/output_depth_scaling.png)

Here the growth is **linear**: eight times the depth costs roughly eight times the time. That matches $$O(g \cdot 2^{n})$$, because at a fixed qubit count the $$2^{n}$$ factor is constant and only the gate count $$g$$ changes. Depth is cheap; qubits are expensive.

## The Memory Wall

The timing tables show *speed*, but the deeper reason simulation is hard is *memory*. A statevector is $$2^{n}$$ complex numbers, and each one takes 16 bytes. The script measures the peak memory of that array as the qubit count grows:

| Qubits | Statevector memory |
|:------:|:------------------:|
| 10 | 0.02 MB |
| 14 | 0.26 MB |
| 18 | 4.19 MB |
| 22 | 67.11 MB |
| 24 | 268.44 MB |

![png](/assets/quantum_programs/quantum_simulation_benchmarking/output_memory_scaling.png)

Every four qubits multiplies the memory by 16. Keep going and the line is brutal: 30 qubits needs about 16 GB, 40 qubits needs about 16 TB, and 50 qubits needs more memory than exists on Earth. This single picture is why we cannot simply simulate a large quantum computer, and why real quantum hardware matters.

## Does Compiling with UCC Help?

So far we ran the raw, unoptimized circuit. But a quantum **compiler** can rewrite a circuit into an equivalent one with fewer gates, and fewer gates should mean less work for the simulator. This is where the issue's mention of the "UCC benchmarking goal" comes in: [UCC](https://github.com/unitaryfoundation/ucc) (the Unitary Compiler Collection) is a single `compile` call that optimizes a circuit. Let us test whether compiling first actually speeds up simulation.

We take a [Quantum Volume](https://en.wikipedia.org/wiki/Quantum_volume) circuit (a standard, gate-heavy benchmark), compile it with UCC, and compare the gate count before and after:

```python
from qiskit.circuit.library import quantum_volume
from ucc import compile as ucc_compile

circuit = quantum_volume(num_qubits, seed=seed)
compiled = ucc_compile(circuit)
```

| Qubits | Raw gates | UCC compiled | Fewer |
|:------:|:---------:|:------------:|:-----:|
| 12 | 1872 | 1626 | 13% |
| 14 | 2548 | 2252 | 12% |
| 16 | 3328 | 3090 | 7% |

![png](/assets/quantum_programs/quantum_simulation_benchmarking/output_ucc_compilation.png)

UCC reliably removes gates, and that gate count is the clean, reproducible number (it is identical on every run). The wall-clock payoff follows it: in our run Qiskit Aer simulated the compiled 12-, 14-, and 16-qubit circuits about 1.16, 1.21, and 1.11 times faster than the raw ones. The speedup is modest and a little noisy at these sizes, which is honest and worth saying out loud: compilation helps in proportion to how many gates it can remove.

It does not *always* help. If you feed UCC a circuit that is already minimal, like our layered example above, its translation into a hardware gate set can actually *add* gates and make simulation slower. The lesson is the same one ucc-bench was built to teach: do not assume, measure.

## Caveats

Honesty about what these numbers do and do not mean:

- **One laptop, single thread.** All times come from one machine with every backend pinned to one core. On a different CPU, or with multithreading on, the ranking can shift. Small wiggles in the third decimal are just timing noise.
- **We benchmarked the default backends.** PennyLane's `default.qubit` and Qibo's NumPy backend are the easy-to-install ones, not the fast ones. PennyLane's `lightning.qubit` and Qibo's `qibojit` are much quicker and would tell a different story. We chose the defaults so the tutorial installs cleanly.
- **Braket's cost is mostly its SDK.** Braket's `LocalSimulator` carries a large fixed Python overhead, so at small sizes you are partly timing the wrapper, not the simulation core.

These are not flaws to hide; they are exactly the kind of thing a good benchmark states up front.

## Dependencies

Everything runs locally on CPU. The versions used for the numbers above were Qiskit Aer 0.17, Cirq 1.6, PennyLane 0.45, Qibo 0.3, Amazon Braket SDK 1.x, and UCC 0.4, on Python 3.12. A pinned [`requirements.txt`](/assets/quantum_programs/quantum_simulation_benchmarking/requirements.txt) is included. To run it:

```bash
cd assets/quantum_programs/quantum_simulation_benchmarking
pip install -r requirements.txt
python benchmark_simulators.py
```

The script prints every table, writes the four CSV files, and saves the plots. There is also a [Jupyter notebook](/assets/quantum_programs/quantum_simulation_benchmarking/benchmark_simulators.ipynb) version if you would rather run it cell by cell.

## A Short Demo

A short (silent) video walkthrough of the main results: the circuit grows qubit by qubit, the simulators spread apart, and then the memory wall shows why it all gets hard. The [`demo.mp4`](/assets/quantum_programs/quantum_simulation_benchmarking/demo.mp4) file is in the project folder.

<video controls muted loop width="640" src="/assets/quantum_programs/quantum_simulation_benchmarking/demo.mp4">
  Your browser cannot play the video. <a href="/assets/quantum_programs/quantum_simulation_benchmarking/demo.mp4">Download demo.mp4</a> instead.
</video>

The same animation as a looping GIF, in case the video does not play inline:

![demo](/assets/quantum_programs/quantum_simulation_benchmarking/demo.gif)

## How I Got Started

My way into quantum computing was through code rather than equations. The first program I wrote was a two-qubit Bell state, and seeing only `00` and `11` come back, never `01` or `10`, did more to make entanglement real for me than any textbook had. I started timing my own circuits mostly out of impatience: my laptop would breeze through 10 qubits and then suddenly choke somewhere around 25, and I wanted to know why. That question is the whole of this tutorial. The honest answer turned out to be the $$2^{n}$$ memory wall, and chasing it taught me more than any single lecture. If you are starting out, pick one small circuit, run it a few different ways like we did here, and stay curious about why the numbers come out the way they do. A laptop and some stubbornness are genuinely enough to begin.

## Use of AI

I used an AI assistant (Anthropic's Claude) to help scaffold the boilerplate in the benchmark script and to tighten the wording of this write-up. I designed the experiment, chose the simulators and metrics, and ran every benchmark myself in the environment described above. The numbers in every table are the contents of the committed CSV files from one real run of the script; rerun it and you will get the same shapes, with absolute times that depend on your machine.

## References

[1] Unitary Foundation. (2024). [UCC: Unitary Compiler Collection](https://github.com/unitaryfoundation/ucc).

[2] Unitary Foundation. (2024). [ucc-bench: Quantum Compiler Benchmarking Suite](https://github.com/unitaryfoundation/ucc-bench).

[3] Javadi-Abhari, A., et al. (2024). Quantum computing with Qiskit. arXiv preprint arXiv:2405.08810.

[4] Developers of Cirq. (2024). [Cirq](https://quantumai.google/cirq), Google Quantum AI.

[5] Bergholm, V., et al. (2018). PennyLane: Automatic differentiation of hybrid quantum-classical computations. arXiv preprint arXiv:1811.04968.

[6] Efthymiou, S., et al. (2021). Qibo: a framework for quantum simulation with hardware acceleration. Quantum Science and Technology, 7(1), 015018.

[7] Amazon Web Services. (2024). [Amazon Braket Python SDK](https://github.com/amazon-braket/amazon-braket-sdk-python).

[8] Nielsen, M. A., & Chuang, I. L. (2010). Quantum Computation and Quantum Information. Cambridge University Press.

## Author
Abhiyan Ampally
