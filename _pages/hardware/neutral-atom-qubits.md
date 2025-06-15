---
layout: page
title:  "Neutral Atom Qubits"
permalink: /hardware/neutral-atom-qubits/
---

**Neutral atoms**

An atom has electrons, protons and neutrons. Electrons are negative charge, protons are positive charge and neutrons have no charge. If the number of electrons are equal to the number of protons then their charge cancel out and the atom is electrically neutral. This state of having equal protons and neutrons is what we call as neutral atoms. If you add or remove an electrons and if the count doesn't match with the protons, then the atom becomes an ion.

**Physical principles of Neutral atoms**

Neutral-atom qubits encode information in two long-lived internal states of individual atoms, such as Rubidium-87, Cesium-133, or Strontium-87. Those internal states are called as hyperfine levels. 


**Hyperfine splitting** - Every atom's energy levels are defined by the interaction of its electrons and nucleus. In neutral-atom systems, two closely spaced energy levels in the ground state—known as hyperfine levels—are chosen to represent qubit states. These are stable states that can be controlled using microwaves or carefully tuned lasers (known as Raman lasers).

**Optical trapping (tweezers)** - Atoms are laser-cooled to near absolute zero, so they barely move. Then, tightly focused laser beams—called optical tweezers—trap each atom in place inside an ultra-high vacuum chamber. These traps isolate the atoms from external disturbances, giving them long coherence times (up to 100 ms or more).

Some of the key components and control systems used in neutral atoms are:

Ultra-high vacuum chambers, Laser cooling setup, Optical tweezer array, Control Electronics, Detector etc.

![Schematic overview of cold atom quantum computer](/assets/images/hardwares/overview_coldatom_computer.png) [Reference of the image](https://epjquantumtechnology.springeropen.com/articles/10.1140/epjqt/s40507-023-00190-1)

**Caliberation operations**

| Operation              | Description                                                                 | Typical Time / Notes                         |
|------------------------|-----------------------------------------------------------------------------|----------------------------------------------|
| **Initialization & Rearrangement** | Atoms are loaded randomly (50–60% fill). A camera detects filled sites; mobile tweezers rearrange atoms to get a defect-free array. | ~400 ms total setup time                     |
| **Single-Qubit Gates** | Raman laser or microwave pulses rotate qubits on the Bloch sphere. Controlled via pulse duration, phase, and power. | ~1–5 µs per gate                              |
| **Two-Qubit Gates (Rydberg Blockade)** | One atom is excited to a Rydberg state, blocking nearby excitations. Enables a fast CZ gate. Combined with Hadamards → CNOT. | ~200–600 ns per entangling gate              |
| **Calibration Routines** | Techniques include laser frequency scans, spin-echo for coherence, and trap alignment to improve fidelity. | Performed regularly to optimize performance  |


**Decoherence and Noise**

| Source of Noise            | Description                                                                                   | Typical Impact                          |
|----------------------------|-----------------------------------------------------------------------------------------------|------------------------------------------|
| **Hyperfine-State Decoherence** | Caused by ambient magnetic field fluctuations and background gas collisions.                | Limits coherence to ~10–100 ms           |
| **Rydberg-State Decay**        | Rydberg levels decay via spontaneous emission during two-qubit gates.                        | Limits entangling fidelity; ~100 µs lifetime |
| **Motional Heating**           | Residual atom motion due to trap instability or gas interactions shifts atomic energy levels. | Reduces gate accuracy and phase stability |
| **Laser Intensity / Phase Noise** | Fluctuations in cooling, trapping, or gate lasers introduce unintended transitions or errors. | Affects fidelity of qubit operations      |

**Error correction**

Many physical qubits are combined into logical qubits to improve the fault tolerance of neutral-atom quantum computers.  A typical error-correcting code, such as the surface code, could take 7-13 atoms per logical qubit.  Rydberg-based entangling gates can produce correlated errors (e.g., simultaneous decay), necessitating specialized rectification techniques.

**Variants of Neutral-Atom Technology**

| Variant                  | Description                                                          | Pros                                                                                   | Cons                                                                                 | Example                                                                                                                                           |
|--------------------------|----------------------------------------------------------------------|-----------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------|
| **Optical Tweezer Arrays** | Each atom is held by a movable, tightly focused laser beam ("tweezer"). | - Reconfigurable layout<br>- High-fidelity control<br>- Mid-circuit rearrangement       | - Complex optics<br>- Slower setup (~100s ms)<br>- Needs high laser power           | QuEra Aquila (256-atom array)<br>See: Bluvstein et al., *Nature*, 2022 [doi:10.1038/s41586-022-04682-0](https://doi.org/10.1038/s41586-022-04682-0) |
| **Optical Lattice Arrays** | Atoms are held in a fixed grid formed by intersecting standing-wave laser beams. | - Very large scale<br>- Passive & stable<br>- Fewer optical components                  | - Fixed layout<br>- Hard to address atoms<br>- Random initial loading                | High-speed imaging in lattices:<br>Su et al., *Nat Commun.* (2025), [doi:10.1038/s41467-025-56305-y](https://doi.org/10.1038/s41467-025-56305-y)  |


**Applications of neutral atoms**

Neutral atoms field is an evolving field and not as matured as superconducting qubits , trapped ions. Thus the applications in this field is a proof-of-concept method. However, few applications are:

1. **Quantum simulations and many body physics** Neutral atoms are arranged in a 2-D or 3-D format. This mimics the lattice-based models and many body physics concept. Thus exploring next-gen materials with neutral atoms can be feasible.

2. **Quantum Sensing** Optical clocks, Interial sensor may share some trends with neutral atom architecture.


**List of companies working in neutral atoms and some of their breakthroughs and roadmap**

1. **PasQal**

[Pasqal](https://www.pasqal.com/) a leading organisation in neutral atom computing has recently demonstrated the trapping of more than 1110 rubidium atoms with approximately 2000 traps demonstrating the feasibility of large-scale neutral atom quantum computing . Recently PasQal and Riverlane partnered to integrate Pasqal’s neutral atom platform with Riverlane’s Deltaflow quantum error correction stack to achieve fault-tolerant quantum computing.![Pasqal roadmap](/assets/images/hardwares/pasqal_roadmap.png) in this image they have a dedicated roadmap.

And their colloboration with NQCC has resulted in the demonstration of 16 x 16 neutral atom array which is the largest in UK. This became a crucial step towards scalable quantum computing. Recently, EuroHPC selected Pasqal to build 140 qubit neutral atom simulator in Italy.

2. **QuEra**

[QuEra](https://www.quera.com/) has developed a publicily accessible  neutral atom computer named Aquilla (256 qubit quantum computer) now available on Amazon Braket. 

3. **Infleqtion**

[Infleqtion](https://infleqtion.com/) mission is to commercialize atom-based quantum products that provide orders of magnitude improvement in sensing and computing applications​. Inflqetion alongwith JPMOrgan chase has announced the release of [Infleqtion open-source library]( https://github.com/qLDPCOrg/qldpc) open-source library for error correction. 

4. **Atom computing**

[Atom Computing](https://atom-computing.com/) builds highly scalable, gate-based quantum computers with arrays of optically-trapped neutral atoms, which will empower unprecedented breakthroughs. Also they partnered with microsoft to develop quantum supercomputers.

 5. **planqc**

[planqc]( https://planqc.eu/) store information in Individual atoms. Quantum information is processed by arranging these qubits in highly scalable arrays and manipulating them with precisely controlled laser pulses


**Some Insightful educational articles / sources**

1. [What is Neutral atoms?](https://www.quera.com/glossary/neutral-atoms)

2. [Key advantages of Neutral atoms architecture](https://www.quera.com/blog-posts/key-advantages-of-neutral-atom-quantum-computer-architectures)

3. [Neutral atom review paper](https://quantum-journal.org/papers/q-2020-09-21-327/)




