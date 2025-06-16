---
layout: page
title:  "Topological Qubits"
permalink: /hardware/topological-qubits/
---

Topology is the mathematical study of features that remain unchanged when an object is smoothly deformed—shifted, bent, or stretched—without tearing or re-attaching pieces. Topological quantum computing applies this idea by encoding information in global properties of exotic quasiparticles called anyons that emerge in certain low-temperature materials. When two anyons are exchanged, the quantum state acquires a transformation: if every pairwise exchange simply multiplies the state by a fixed phase (so the order of exchanges does not matter), the anyons are called Abelian; if different exchange sequences lead to distinct quantum states (meaning the operations do not commute), they are non-Abelian. Non-Abelian anyons are especially valuable because the resulting “braids” of world-lines can implement robust quantum logic gates whose resilience to local disturbances offers built-in error protection for future quantum computers.

---

### **Topological Qubits as Quantum Bits**

| Feature                | Description                                                                 |
|------------------------|-----------------------------------------------------------------------------|
| **Qubit Encoding**     | Stored in the collective state of anyons (e.g., 4 Majoranas per qubit)       |
| **Gate Operations**    | Performed by braiding paths of non-Abelian anyons                           |
| **Readout**            | Fusion outcome of anyons reveals the logical qubit state                    |
| **Error Protection**   | Inherent in the topology; gates are insensitive to small local disturbances |

---

### **Calibration Operations**

| Operation               | Description                                                            | Notes                                           |
|-------------------------|------------------------------------------------------------------------|-------------------------------------------------|
| **Initialization**      | Cooling and arranging anyons in specific configurations                | Requires extreme cryogenic environments         |
| **Gate Execution**      | Braiding of quasiparticles to apply logic gates                        | Topologically protected, order-sensitive        |
| **Fusion/Measurement**  | Fusion of anyons reveals encoded qubit state                           | Often destructive, depending on protocol        |
| **Calibration Routines**| Material growth, topoconductor tuning, and quasiparticle localization  | Ongoing area of experimental research           |

---

### **Decoherence and Noise**

| Source of Noise            | How Topological Qubits Mitigate It                             |
|----------------------------|------------------------------------------------------------------|
| **Local Defects/Noise**    | Braiding depends on topology, not local imperfections           |
| **Charge Fluctuations**    | Anyon states are globally defined, not charge-sensitive          |
| **Control Errors**         | Robustness to timing and amplitude errors due to non-local logic |
| **Thermal Noise**          | Requires cryogenic isolation to maintain topological phase       |

---

### **Error Correction**

Topological qubits aim to **bypass traditional error correction** through built-in protection:

- Information is stored in **non-local** degrees of freedom
- Logical gates are **topologically robust**
- However, for **scaling to millions of qubits**, surface code-style active correction may still be layered on top

---

### **Variants of Topological Qubits**

| Variant                  | Description                                                              | Pros                                               | Cons                                               | Example Company                                   |
|--------------------------|--------------------------------------------------------------------------|----------------------------------------------------|----------------------------------------------------|---------------------------------------------------|
| **Majorana Qubits**      | Encoded in Majorana zero modes in superconductors                       | Built-in protection, solid-state compatible         | Detection and manipulation still under research    | Microsoft Azure Quantum                          |
| **Fractional QH Anyons** | Anyons emerge in fractional quantum Hall states                         | Naturally occurring non-Abelian anyons             | Operate at extremely low temperatures and high fields | Nokia Bell Labs                                  |
| **Simulated Anyons**     | Anyons simulated on existing platforms like superconducting qubits      | Easier to test braid logic                          | Not truly topological or error-immune              | Google Quantum AI                                |

---

### **Applications of Topological Quantum Computing**

1. **Fault-tolerant quantum computing**  
   Logical gates immune to local errors enable more stable large-scale systems.

2. **Secure quantum communication**  
   Braiding operations and fusion outcomes offer security features based on topology.

3. **Quantum simulation**  
   Ideal for modeling exotic quantum phases and condensed matter systems.

4. **Mathematical testing ground**  
   TQC brings together topology, group theory, and quantum field theory.

---

### **List of Companies Working in Topological Qubits**

1. **[Microsoft Azure Quantum](https://quantum.microsoft.com/)**  
   Developing **Majorana 1**, a silicon-superconductor chip encoding qubits using four Majorana zero modes. Their roadmap includes a **million-qubit**, fault-tolerant device under the DARPA US2QC program.

2. **[Nokia Bell Labs](https://www.nokia.com/bell-labs/research/air-lab/data-and-devices/topological-quantum-computing/)**  
   Working on **non-Abelian anyons** in 2D electron gases (GaAs/AlGaAs). Their "Quest for a Quality Qubit" program has already demonstrated single-charge manipulation and long coherence times.

3. **[Google Quantum AI](https://quantumai.google/)**  
   Demonstrated **simulated braiding** of non-Abelian anyons using their superconducting qubit platform. This experimental work is a step toward implementing topological quantum gates.

4. **[Quantinuum](https://arxiv.org/abs/2305.03766)**  
   Achieved experimental **creation and manipulation of non-Abelian anyons** in a trapped-ion quantum computer, showcasing topological dynamics on controllable hardware.

---

### **Academic & Research Resources**

1. [A Short Introduction to Topological Quantum Computing (arXiv)](https://arxiv.org/abs/1705.04103)  
2. [Mathematical Background from Princeton](https://www.princeton.edu/~sondhi/misc/simon.pdf)

---

**In summary**, topological qubits promise the holy grail of quantum computing: **built-in error protection**, **robust logic gates**, and **scalable architectures**. While experimentally demanding, breakthroughs by companies like Microsoft and Nokia signal real progress toward realizing a new era of **fault-tolerant quantum computation**.
