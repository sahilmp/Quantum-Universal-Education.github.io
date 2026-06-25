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

A quantum *simulator* is an ordinary classical program that pretends to be a quantum computer: you hand it a circuit and it works out what the qubits would do. There are lots of simulators and they are not equally fast. In this tutorial we take one circuit and run it on five different simulators, but we try to do it the way a careful scientist would. First we *prove* all five compute the same thing, so the comparison is trustworthy. Then we measure how the time grows with qubit count and depth, see the memory wall underneath it all, fit the numbers to a formula that *predicts* where each simulator gives up, and finally check whether compiling the circuit with [UCC](https://github.com/unitaryfoundation/ucc) first makes it faster. It is written for high school and undergraduate students, and everything runs on a laptop.

## Why Simulating Quantum Circuits Is Hard

A classical computer stores the state of $$n$$ qubits as a list of complex numbers called the **statevector**. The catch is its length: $$n$$ qubits need

$$
    2^{n}
$$

complex amplitudes. Ten qubits is $$2^{10} = 1024$$ numbers, nothing at all. But every extra qubit *doubles* the list, so 20 qubits is about a million amplitudes and 30 qubits is a billion. On top of that, every gate has to update the whole statevector, so the time to run a circuit of $$g$$ gates grows roughly like

$$
    \text{time} \approx O(g \cdot 2^{n}).
$$

That $$2^{n}$$ is the reason real quantum computers are interesting (they skip it) and the reason simulators eventually crawl. We will come back to this exact formula and turn it into a prediction.

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

## Do the Simulators Even Agree?

Before timing anything, here is a question most benchmarks skip: do the five simulators actually compute the *same* state? If they disagree, comparing their speeds is meaningless. So the script pulls the final statevector out of each one and compares it to Qiskit's.

There is a real gotcha here that trips up beginners: the libraries do not all number their qubits the same way. Qiskit calls qubit 0 the *last* bit, while Cirq, PennyLane, Qibo, and Braket call it the *first*. If you forget this, the states look completely different even when the physics is identical. Once we put them all in the same order, we compare with the **fidelity** $$|\langle a | b \rangle|^{2}$$, which is 1 when two states match (and politely ignores an overall phase that has no physical meaning).

```
Correctness check (8 qubits, depth 5)
  qiskit_aer  fidelity vs qiskit_aer = 1.000000000000
  cirq        fidelity vs qiskit_aer = 1.000000000000
  pennylane   fidelity vs qiskit_aer = 1.000000000000
  qibo        fidelity vs qiskit_aer = 1.000000000000
  braket      fidelity vs qiskit_aer = 1.000000000000
  -> all five agree (largest infidelity 9.7e-14)
```

A fidelity of 1 to twelve decimal places (the tiny `1e-14` is just floating-point rounding) means all five really are running the same circuit. Now the timings mean something.

## Keeping the Comparison Fair

Two more details matter. Qiskit Aer is written in C++ and will happily use every core on your machine, while the pure-Python simulators use one. If we let that happen we would be benchmarking the number of cores, not the simulators, so the script pins every backend to a single thread before NumPy loads:

```python
import os
for var in ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[var] = "1"
```

And the first call to a simulator pays one-time costs (imports, caching, just-in-time compilation), so we run a couple of warm-up rounds we throw away, then take the **median** of several timed runs.

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

Now one small function per simulator. Each takes our neutral gate list, builds the circuit in that library's own language, and returns a function that runs it. Here are two of the five; the rest follow the same shape and live in the [full script](/assets/quantum_programs/quantum_simulation_benchmarking/benchmark_simulators.py).

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

## Results: Scaling with Qubit Count

We hold the depth at 10 layers and grow the circuit from 10 to 18 qubits. Every number is the median time in seconds. These tables are exactly the contents of `results_qubits.csv` and `results_depth.csv` in the project folder, so you can rerun the script and check them (your absolute times will differ by machine and run, but the shapes hold).

| Qubits | qiskit_aer | cirq | pennylane | qibo | braket |
|:------:|:----------:|:----:|:---------:|:----:|:------:|
| 10 | 0.0066 | 0.0214 | 0.0267 | 0.0098 | 0.0949 |
| 12 | 0.0115 | 0.0278 | 0.0369 | 0.0127 | 0.1266 |
| 14 | 0.0288 | 0.0459 | 0.0569 | 0.0363 | 0.1614 |
| 16 | 0.0888 | 0.0857 | 0.1398 | 0.1871 | 0.2072 |
| 18 | 0.3733 | 0.4613 | 1.7292 | 1.9170 | 1.9521 |

![png](/assets/quantum_programs/quantum_simulation_benchmarking/output_qubit_scaling.png)

The vertical axis is a log scale, so a straight climb means the time keeps multiplying by a constant factor: that is the $$2^{n}$$ growth. Qiskit Aer and Cirq stay cheap as the circuit widens, while the pure-NumPy paths in PennyLane and Qibo shoot up past 16 qubits (around 1.7 to 1.9 seconds at 18 qubits, versus 0.37 for Aer).

## Results: Scaling with Circuit Depth

Next we hold the qubit count at 12 and make the circuit deeper, from 5 to 40 layers:

| Depth | qiskit_aer | cirq | pennylane | qibo | braket |
|:-----:|:----------:|:----:|:---------:|:----:|:------:|
| 5  | 0.0120 | 0.0388 | 0.0224 | 0.0072 | 0.2475 |
| 10 | 0.0195 | 0.0387 | 0.0524 | 0.0176 | 0.5411 |
| 20 | 0.0343 | 0.1154 | 0.1005 | 0.0313 | 0.8084 |
| 40 | 0.0930 | 0.1510 | 0.1825 | 0.0770 | 1.8699 |

![png](/assets/quantum_programs/quantum_simulation_benchmarking/output_depth_scaling.png)

The growth here is **linear**: eight times the depth costs roughly eight times the time. That matches $$O(g \cdot 2^{n})$$, because at a fixed qubit count the $$2^{n}$$ factor is constant and only the gate count $$g$$ changes. Depth is cheap; qubits are expensive.

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

Every four qubits multiplies the memory by 16. Keep going and the line is brutal: 30 qubits needs about 16 GB, 40 qubits needs about 16 TB, and 50 qubits needs more memory than exists on Earth.

## Predicting the Wall

Here is where benchmarking becomes more than a table. We have a formula, $$\text{time} \approx C \cdot g \cdot 2^{n}$$, and we have measurements. Fitting one to the other gives us the constant $$C$$ for each simulator, and once we know $$C$$ we can *predict* the qubit count where each simulator crosses one second, one minute, and runs out of a typical 16 GB of memory. The script does the fit with `numpy.polyfit`:

| Simulator | C | Fit quality (R²) | Reaches 1 s | Reaches 1 min | Out of 16 GB |
|:----------|:---------:|:----------------:|:-----------:|:-------------:|:------------:|
| qiskit_aer | 2.6e-9 | 1.000 | ~20 qubits | ~25 qubits | ~30 qubits |
| cirq       | 3.2e-9 | 0.993 | ~20 qubits | ~25 qubits | ~30 qubits |
| pennylane  | 1.2e-8 | 0.977 | ~18 qubits | ~23 qubits | ~30 qubits |
| qibo       | 1.4e-8 | 0.985 | ~18 qubits | ~23 qubits | ~30 qubits |
| braket     | 1.3e-8 | 0.973 | ~18 qubits | ~23 qubits | ~30 qubits |

The fit quality $$R^{2}$$ is between 0.97 and 1.00, which is the model quietly confirming itself: the $$2^{n}$$ law really does describe the data. The constant $$C$$ is the interesting part. Qiskit Aer's is about five times smaller than the NumPy backends', which is exactly why it buys you two extra qubits of headroom before the clock and the memory catch up. Notice that every backend hits the same memory wall near 30 qubits, because $$2^{n}$$ memory does not care how fast your code is.

## Does Compiling with UCC Help?

So far we ran the raw, unoptimized circuit. But a quantum **compiler** can rewrite a circuit into an equivalent one with fewer gates, and fewer gates should mean less work. This is the "UCC benchmarking goal" the issue mentions: [UCC](https://github.com/unitaryfoundation/ucc) (the Unitary Compiler Collection) is a single `compile` call that optimizes a circuit. We take a [Quantum Volume](https://en.wikipedia.org/wiki/Quantum_volume) circuit, compile it with UCC, and compare the gate count.

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

UCC reliably removes gates, and that gate count is the clean, reproducible number (it is identical on every run). The wall-clock payoff follows it but is small and noisy at these sizes, which is honest and worth saying: compilation helps in proportion to how many gates it can remove. It does not *always* help, either. If you feed UCC a circuit that is already minimal, its translation into a hardware gate set can *add* gates and make simulation slower. The lesson is the one ucc-bench was built to teach: do not assume, measure.

## Caveats

Honesty about what these numbers do and do not mean:

- **One laptop, single thread.** All times come from one machine with every backend pinned to one core. On a different CPU the ranking can shift, and small wiggles in the last decimal are timing noise.
- **We benchmarked the default backends.** PennyLane's `default.qubit` and Qibo's NumPy backend are the easy-to-install ones, not the fast ones. PennyLane's `lightning.qubit` and Qibo's `qibojit` are much quicker and would move those lines down.
- **Braket's cost is mostly its SDK.** Braket's `LocalSimulator` carries a large fixed Python overhead, so at small sizes you are partly timing the wrapper, not the simulation core.
- **The predictions are extrapolations.** They assume the clean $$C \cdot g \cdot 2^{n}$$ trend continues; real machines also hit cache and swapping effects, so treat them as ballpark, not gospel.

## Dependencies

Everything runs locally on CPU. The versions used were Qiskit Aer 0.17, Cirq 1.6, PennyLane 0.45, Qibo 0.3, Amazon Braket SDK 1.x, and UCC 0.4, on Python 3.12. A pinned [`requirements.txt`](/assets/quantum_programs/quantum_simulation_benchmarking/requirements.txt) is included. To run it:

```bash
cd assets/quantum_programs/quantum_simulation_benchmarking
pip install -r requirements.txt
python benchmark_simulators.py
```

The script runs the correctness check, prints every table, writes the CSV files, fits the scaling model, and saves the plots. There is also a [Jupyter notebook](/assets/quantum_programs/quantum_simulation_benchmarking/benchmark_simulators.ipynb) version if you would rather run it cell by cell.

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

I used an AI assistant (Anthropic's Claude) to help scaffold the boilerplate in the benchmark script and to tighten the wording of this write-up. I designed the experiment, chose the simulators and metrics, worked out the qubit-ordering fix for the correctness check, and ran every benchmark myself in the environment described above. The numbers in every table are the contents of the committed CSV files from one real run of the script; rerun it and you will get the same shapes, with absolute times that depend on your machine.

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
