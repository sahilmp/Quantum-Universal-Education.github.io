---
layout: page
title:  "Photonic Qubits"
permalink: /hardware/photonic-qubits/
---

**What are Photonic Qubits?**

Light is made up of photons. Each photons always carry energy (E = hv). And there is not correct or exact number of photons a beam of light carries. Sometimes a dim beam of light carries less photons. A continuous pulse of light has more photons each carrying energy hv.And photons are indivisble nature. Also, light consists of many photons, where each photon is the smallest indivisible chunk of the electromagnetic field and carries a fixed energy (E=hν). Light exhibits dual nature of wave and particle. Depending upon the experiments light exhibits itself as particle (Photoelectric effect experiment) and as wave (double-slit experiment). Its not like switching between wave nature and particle nature. Depending upon how we want to use the photons, respective nature is exhibited. 

Photons exhibit **wave-particle duality**:
- In some experiments (e.g., **double-slit**), light acts like a **wave**.
- In others (e.g., **photoelectric effect**), it behaves like **particles**.

When you send exactly one photon into your circuit, you know it will either register as “there” (one click on your detector) or “not there” (no click). That discrete nature is what lets you treat it as a qubit (0 or 1).

Detection always collapses the photon into a single “particle” event—a click—so you need the photon to really be a distinct, indivisible entity.

Quantum photonics include the generation (single-photon emitters), manipulation and detection (photon counting) of light and matter on the quantum level.

**Variants of Photonic Quantum Computing**

| Variant                             | Description                                                                     | Pros                                            | Cons                                           |
|-------------------------------------|---------------------------------------------------------------------------------|-------------------------------------------------|------------------------------------------------|
| **Linear Optics Quantum Computing** | Uses beam splitters, phase shifters, detectors (KLM protocol)                  | Room-temperature, well-studied                  | Probabilistic gates, needs lots of resources   |
| **Measurement-Based (Cluster States)** | Uses entangled photon networks and measurements to perform computation       | Modular, scalable in theory                     | Requires massive entangled states              |
| **Boson Sampling / Photonic Simulators** | Uses multi-photon interference to solve specific problems (not universal)  | Demonstrates quantum advantage                  | Not general-purpose computing                  |

---

**Calibration operations**

| Operation               | Description                                                                                     | Typical Time / Notes                         |
|-------------------------|-------------------------------------------------------------------------------------------------|----------------------------------------------|
| **Initialization**      | Single-photon sources (e.g., quantum dots, SPDC) generate one photon at a time                 | Tuned for frequency, timing, and coherence   |
| **Single-Qubit Gates**  | Waveplates, phase shifters, or interferometers rotate qubit states                             | Passive and low-latency                      |
| **Two-Qubit Gates**     | Performed probabilistically using entanglement and beam splitters (KLM protocol)               | Low success rate; requires error correction  |
| **Readout**             | Single-photon detectors count photons or track coincidence events                              | Time-resolved detection                      |
| **Recalibration**       | Phase stabilization, laser drift correction, and filter alignment                              | Required for high-visibility interference     |

---

**Decoherence and Noise**

| Source of Noise             | Description                                                                 | Typical Impact                        |
|-----------------------------|-----------------------------------------------------------------------------|----------------------------------------|
| **Photon Loss**             | Loss in fibers, waveguides, or detectors                                   | Reduces entanglement and fidelity      |
| **Mode Mismatch**           | Misalignment in photon shape (temporal/spectral) affects interference      | Lowers gate success probability        |
| **Detector Noise**          | Dark counts or inefficiencies in photon detectors                          | False detections or missed photons     |
| **Timing Jitter**           | Small variations in photon arrival times                                   | Impacts interference-based gates       |

---

**Applications of Quantum photonics**

Quantum photonics is applied in areas where unique properties of light can be utilized. For example: In the applications where superposition, entanglement and squeezing provide an advantage over classical approaches.

1. Quantum Communication & Cryptography
2. Quantum Sensing & Metrology
3. Quantum Imaging & Microscopy
4. Quantum Simulation of Many-Body Systems
5. Quantum enhanced spectroscopy

**List of Companies Working in Photonic Qubits and Their Breakthroughs**

1. **[Quandela](https://www.quandela.com/)**  
   Offers photonic quantum computing solutions for cybersecurity, energy, and finance. Developed a 6–24 qubit photonic quantum computer.  
   ![Quandela's hardware](/assets/images/hardwares/quandela.png)

2. **[Diamond Quanta](https://diamondquanta.com/)**  
   Advances power electronics and photonic devices using diamond-based materials.

3. **[PsiQuantum](https://www.psiquantum.com/)**  
   Developing fault-tolerant, million-qubit photonic quantum computers. Introduced **Omega** platform and a novel non-dilution cooling system.  
   [Nature Paper](https://www.nature.com/articles/s41586-025-08820-7)

4. **[Nu Quantum](https://www.nu-quantum.com/)**  
   Built the world’s first **rack-mount photonic quantum network control unit** for distributed entanglement.  
   ![Nu Quantum Quantum Networking Unit](/assets/images/hardwares/nu_quantum_.png)

5. **[NTT Laboratories](https://www.rd.ntt/e/organization/laboratory/)**  
   Researches optical and quantum networking technologies for communication and computing.

6. **[Aegiq](https://aegiq.com/)**  
   Built the **Artemis** photonic quantum computer, targeting industries like defence, aerospace, and cybersecurity.

7. **[Quantum Source](https://www.qs-labs.com/)**  
   Uses single atoms and atom-photon entanglement to generate photons and build large 3D cluster states for error correction.

8. **[Xanadu](https://www.xanadu.ai/)**  
   Launched the **Aurora** photonic quantum computer.  
   [Aurora Paper in Nature](https://www.nature.com/articles/s41586-024-08406-9)

9. **[Photonic](https://photonic.com/)**  
   Builds a scalable, fault-tolerant, optically linked silicon spin-photon hybrid platform.

10. **[QuiX Quantum](https://www.quixquantum.com/)**  
   Building a universal photonic quantum computer with integrated photonics—offering room-temperature operation and scalability.

---

**Universities Working in Photonic Quantum Computing**

1. **University of Science and Technology of China**  
   Demonstrated a high-efficiency single-photon source for scalable computing.  
   [Link to paper](https://www.nature.com/articles/s41566-025-01639-8)

2. **Southern University of Science and Technology, Shenzhen**  
   Demonstrated photonic **quantum teleportation of a Toffoli gate** across three locations.  
   [Link to paper](https://opg.optica.org/oe/fulltext.cfm?uri=oe-32-22-39675&id=561529)

3. **ETRI, KAIST & University of Trento (collaboration)**  
   Created an 8-photon silicon photonic chip with 6-qubit entanglement. Operates at room temperature with low energy usage.

---

**Limitations of Photonic Qubits**

- Two-qubit gates are often probabilistic  
- Photon loss is a major challenge for scaling  
- Requires extremely efficient single-photon sources and detectors  
- Cluster state generation at scale remains resource intensive

---

**Some Insightful Articles / Sources**

1. [Introduction to Quantum Photonics – Pyroistech](https://www.pyroistech.com/quantum-photonics/)  
2. [Quantum Photonics – Springer Book](https://link.springer.com/book/10.1007/978-3-030-47325-9)

