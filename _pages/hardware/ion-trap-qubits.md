---
layout: page
title:  "Ion-Trap Qubits"
permalink: /hardware/ion-trap-qubits/
---

Trapped ions means trapping an atom after removing an electron thus it becomes net positive charge. If the atom is neutral, electric forces couldn't be felt and thus confinement doesn't occur. Negative ions (atom with an extra electron) can be trapped too but they aren't used as quantum bits. We need positive charge because in an electric field a positive charge always experience a force in the direction of field lines. Negative ions feels in opposite direction and neutral atoms doesn't feel a net force and thus can't be held by electric fields.  Usually Calcium, ytterbium or beryllium ions are used an ion. 

**Steps to trap ions**

We trap this positively charged ion by creating an electric cage inside a vacuum chamber. 
Oscillating voltages on specially shaped metal electrodes generate forces that keep the ion suspended in free space, with no physical container touching it. Because the ion is locked in place by those carefully tuned electromagnetic fields, it floats almost motionless, allowing scientists to use lasers to control its internal energy levels (the qubit “0” and “1”) and to read out its state with very high precision. In short, a trapped ion is simply a single, positively charged atom held in midair by electric fields so that we can manipulate its quantum states.

**Types of traps**

There are two ways to trap ions(charged particle). By using electric field and magnetic fields.

1. **Paul traps (RF)** This trap uses the combination of static and oscillating electric field for confinement
2. **Penning traps** This trap uses strong static electric and magnetic field for confinement.

Each trap has different uses. Penning traps can be used for precise magnetic measurements in spectroscopy. Studies of quantum state manipulation most often use the Paul trap.

**Applications of Ion traps**

1. Precision measurements in atomic physics

2. Mass spectrometry

3. Anti-matter storage

4. Optical and microwave spectroscopy

5. Laser cooling

**Calibration Operations**

| Operation              | Description                                                                 | Typical Time / Notes                         |
|------------------------|-----------------------------------------------------------------------------|----------------------------------------------|
| **Initialization**     | Ions are cooled and pumped into a well-defined ground state using lasers.   | ~100 µs per ion                              |
| **Single-Qubit Gates** | Laser or microwave pulses manipulate internal energy levels.                | ~1–10 µs                                     |
| **Two-Qubit Gates**    | Uses Mølmer–Sørensen or similar gates via motional coupling.                 | ~10–100 µs                                   |
| **Measurement**        | Detect fluorescence to read quantum state.                                  | ~100 µs with >99% fidelity                   |
| **Calibration Routines** | Includes Doppler cooling, trap tuning, coherence checks, sideband scans.   | Performed routinely to maintain high fidelity|

---

**Decoherence and Noise**

| Source of Noise              | Description                                                                               | Typical Impact                                |
|------------------------------|-------------------------------------------------------------------------------------------|------------------------------------------------|
| **Magnetic Field Fluctuations** | Impacts phase coherence of hyperfine qubits.                                           | Coherence time reduced to ~10 ms – 10 s       |
| **Laser Phase / Amplitude Noise** | Disturbs gate accuracy during qubit operations.                                     | Lowers gate fidelity                          |
| **Electric Field Noise**     | Causes motional heating of ions in the trap.                                             | Reduces two-qubit gate reliability            |
| **Spontaneous Emission**     | Occurs during off-resonant laser operations.                                             | Contributes to qubit decoherence              |
| **Background Gas Collisions**| Leads to ion loss or state flip due to poor vacuum.                                      | Requires ultra-high vacuum (~10⁻¹¹ Torr)      |

---

**Key Properties of Ion-Trap Qubits**

| Property                    | Typical Value / Range                            | Notes                                             |
|-----------------------------|--------------------------------------------------|---------------------------------------------------|
| **Qubit Coherence Time**    | ~10 ms to >1000 s                                | Among the highest in any qubit modality           |
| **Single-Qubit Gate Fidelity** | >99.9%                                      | Extremely precise                                 |
| **Two-Qubit Gate Fidelity** | >99%                                            | Constantly improving                              |
| **Connectivity**            | All-to-all within a local trap                  | Facilitates efficient entanglement                |
| **Temperature Requirement** | Room temperature (~300 K)                       | No cryogenics needed                              |
| **Operation Mechanism**     | Laser or microwave-controlled gates             | Requires precise tuning and beam alignment        |

**Companies working in developing Trapped Ions architecture**

1. **Quantinuum**

[Quantinuum](https://www.quantinuum.com/) is one of the world's largest integrated quantum company focussed on developing Quantum Hardware architecture (Trapped ion), Computational chemistry , cybersecurity, AI/ML, Mathematics etc. Researchers also developed a roadmap for improvement in Hardware architecture till 2029.

2. **IonQ**

[IONQ](https://ionq.com/) is one of the well-known companies working in Ion trap technology. They built quantum systems which are universally accessible, high-performing and are commercially available. And these quantum computers are accessible via Quantum cloud and support most prominent Quantum SDK's like cirq, qiskit, aws, azure.

3. **Alpine Quantum Technology**

[AQT](https://www.aqt.eu/) offers fully functional trapped-ion quantum computers, ready for integration into existing high-performance computing (HPC) data centre installations, and cloud accessibility. Below image shows the 19-inch rack mounted quantum computer that operates at room temperature and consumes less than two kilowatts of electrical power, eliminating the need for special cooling, water, or extensive energy infrastructure.

![Alpine Quantum Technology](/assets/images/hardwares/Alpine.png) 


4. **Universal quantum**

[Universal quantum](https://universalquantum.com/) published the first practical blueprint for a large-scale trapped ion systems.

5. **Oxford Ionics**

[Oxford Ionics](https://www.oxionics.com/) works to achieve fault-tolerant quantum computing using trapped ion systems and they recently released a broad roadmap to achieve fault-tolerant quantum computing with the development of 10,000 + high-fidelity quantum processor in next 3 years. 


![Oxford Ionics](/assets/images/hardwares/OxfordIonics.png) 

6. **Open Quantum Design**

[Open Quantum Design](https://openquantumdesign.org/) Open Quantum Design (OQD) announced the world’s first open-source, full-stack, trapped-ion quantum computer providing access to global community to accelerate quantum research and bridge the gap between academia and Industry.

7. **eleQtron**

[eleQtron](https://eleqtron.com/en/) develops and operates quantum computers. Their computing machines will be able to solve problems, outperforming the best conventional supercomputers. To do this, they are using the quantum states of ions controlled by established and miniaturized microwave technology. A unique concept called MAGIC (Magnetic Gradient Induced Coupling).

**Some other recent breakthroughs**

IonQ introduced a [hybrid quantum classical architecture](https://arxiv.org/abs/2504.08732) to enhance LLM fine-tuning, where a pre-trained LLM is supplemented with a small set of training data to customize its functionality via quantum machine learning. 

**Some Insightful educational articles / sources**

1. [Basics of Ion traps](https://arxiv.org/pdf/1311.7220) -> Must read paper.

2. [Applications of Ion traps](https://arxiv.org/pdf/1311.7220)

---


