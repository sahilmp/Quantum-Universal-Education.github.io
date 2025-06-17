---
layout: page
title:  "NMR Qubits"
permalink: /hardware/nmr-qubits/
---

**Nuclear Magnetic Resonance (NMR)**

NMR uses the magnetic properties of atomic nuclei to perform quantum computation. Each nucleus with spin-½ (like hydrogen-1 or carbon-13) behaves like a tiny magnet. When placed in a strong magnetic field, these spins align either with or against the field, forming two energy levels that can be used as qubit states—|0⟩ and |1⟩.

To control these nuclear spins, we apply **radio-frequency (RF) pulses** at their specific resonance frequencies. Each spin’s orientation can be flipped or rotated to perform quantum gates.

![Zeeman splitting of nuclear spins](https://tse1.mm.bing.net/th/id/OIP.3ySx29MhcQywNTdh83pOMAHaFj?pid=Api)  
[Zeeman Splitting and Spin States](https://tse1.mm.bing.net/th/id/OIP.3ySx29MhcQywNTdh83pOMAHaFj?pid=Api)

---

**NMR Qubits as quantum bits**

In a typical NMR quantum computer, we use molecules where each spin-active nucleus behaves as a qubit. These molecules are placed in a magnetic field inside an NMR spectrometer. The nuclei interact with each other via **J-coupling**, which enables entangling gates. Control is achieved through **carefully designed RF pulse sequences**.

The signal from these nuclear spins is detected as an oscillating voltage induced in a nearby coil (the readout). However, this signal comes from an **ensemble of molecules**, not individual qubits.

![Liquid-state NMR quantum computing setup](https://tse1.mm.bing.net/th/id/OIP.Xw7OTDtRFiuNxEvv29RIhAHaFj?pid=Api)  
[Schematic of NMR setup for quantum computing](https://tse1.mm.bing.net/th/id/OIP.Xw7OTDtRFiuNxEvv29RIhAHaFj?pid=Api)

---

**Calibration operations**

| Operation               | Description                                                                                       | Typical Time / Notes               |
|-------------------------|---------------------------------------------------------------------------------------------------|------------------------------------|
| **Initialization**      | Use pulse sequences and gradients to create a pseudo-pure state ensemble                         | ~1–10 ms                           |
| **Single-Qubit Gates**  | RF pulses at a specific frequency rotate individual nuclear spins                                | ~10–100 µs per gate                |
| **Two-Qubit Gates**     | J-coupling enables interactions between spins in the same molecule                               | ~1–10 ms                           |
| **Readout**             | Detected as voltage from net magnetization using RF coils                                        | Ensemble measurement only          |
| **Calibration Routines**| Includes pulse shaping, field tuning, shimming for homogeneity                                  | Done routinely for high fidelity   |

---

**Decoherence and Noise**

| Source of Noise                  | Description                                                                          | Typical Impact                            |
|----------------------------------|--------------------------------------------------------------------------------------|--------------------------------------------|
| **Dipolar and J-coupling effects** | Can cause unwanted entanglement or dephasing                                        | Limits fidelity and scalability            |
| **Magnetic Field Inhomogeneity** | Variations in B₀ across the sample broaden resonance lines                          | Impacts control accuracy                   |
| **Pulse Errors**                | Inaccurate RF pulses may cause gate imperfections                                   | Reduces fidelity of operations             |
| **Low Signal Strength**         | Due to small magnetic moments of nuclei and ensemble averaging                       | Hard to scale beyond 10–15 qubits          |

---

**Error correction**

NMR systems enabled early demonstrations of quantum error correction. While not scalable, they showed how error-correcting codes work using 3–7 qubit molecules. Some examples include:

- **3-qubit bit-flip and phase-flip codes**
- **5-qubit perfect code**
- **Decoherence-free subspaces**

But NMR cannot perform active error correction on individual spins since only the ensemble is measured.

---

**Variants of NMR Quantum Technology**

| Variant            | Description                                                              | Pros                                         | Cons                                           | Example                                                                 |
|--------------------|--------------------------------------------------------------------------|----------------------------------------------|------------------------------------------------|-------------------------------------------------------------------------|
| **Liquid-State NMR** | Molecules in solution; spins manipulated by RF pulses in a spectrometer | - Mature technique<br>- Easy control         | - Ensemble only<br>- Weak signal scaling      | IBM’s 5-qubit demonstration of Shor’s algorithm                        |
| **Solid-State NMR** | Spins embedded in crystal lattice                                         | - Better coherence potential<br>- Scalability | - Complex interactions<br>- Requires cooling  | Phosphorus-doped silicon (Kane model)                                  |
| **Zero-Field NMR**  | Uses internal spin interactions only, no external magnetic field         | - Simpler setup<br>- Magnetic noise resistant | - Harder spin addressability                   | Harvard/MIT research on field-free quantum sensors                     |

---

**Applications of NMR Qubits**

1. **Quantum algorithm demonstrations**  
   NMR was used to implement Grover’s, Deutsch-Jozsa, and Shor’s algorithms using 2–7 qubits.

2. **Pulse sequence design & benchmarking**  
   Helped develop and test pulse optimization, gate fidelity, and basic error correction.

3. **Educational platform**  
   Still widely used in universities and labs to **teach quantum computing**.

---

**List of institutions working in NMR quantum computing and their contributions**

1. **[IBM Almaden](https://www.ibm.com/research/labs/almaden)**  
   Implemented Shor’s algorithm with 5 NMR qubits in a liquid-state setup. One of the earliest and most notable demonstrations of quantum computing using NMR.

2. **[MIT](https://web.mit.edu/physics/)** & [Harvard](https://physics.harvard.edu/)**  
   Pioneered techniques for pulse shaping and pseudo-pure state generation. Collaborated on foundational theory for NMR-based quantum logic gates.

3. **[Oxford University](https://www.physics.ox.ac.uk/)**  
   Worked on logic gate calibration, spin dynamics, and early quantum error correction using NMR systems.

4. **[Indian Institute of Science (IISc)](https://iisc.ac.in/)**  
   Focused on quantum simulations, NMR spectroscopy, and pulse engineering to optimize control fidelity.

5. **[Chinese Academy of Sciences – Institute of Physics (CAS)](https://english.iop.cas.cn/)**  
   Developed multi-qubit molecular NMR systems and advanced spin interaction models. High-fidelity experiments on complex molecules.

---

**Universities and Labs contributing to NMR research**

1. **Oxford Quantum Group**  
   [Oxford NMR Research](https://en.wikipedia.org/wiki/Centre_for_Quantum_Computation)

2. **IBM Research**  
   [IBM: What is NMR Quantum Computing?](https://research.ibm.com/quantum-computing)

3. **MIT-Harvard Center for Ultracold Atoms**  
   Strong foundational work in early NMR-based algorithms.

4. **CAS Institute of Physics**  
   [Chinese Academy of Sciences NMR work](https://english.cas.cn/research/highlight/qp/)

---

**In summary**, NMR quantum computing was one of the first platforms to demonstrate real quantum logic gates and algorithms. Although it's not scalable for modern use due to ensemble limitations, it helped validate the theory of quantum computing and inspired the design of scalable architectures.

---