---
layout: page
title:  "NV Center in Diamond"
permalink: /hardware/nv-center-in-diamond/
---

In pure diamond, every carbon atom is bonded in a tight 3-D network. Sometimes, one of the carbon atom is replaced by nitrogen atom (This is called as impurity) and the spot next to the nitrogen atom is a vacant spot but usually thats the spot where a carbon atom should be placed originally. That nitrogen + vacant spair becomes the NV center. This NV center is of high importance because in pure diamond the carbon atom has exactly 4  valence electrons and when carbon atom is replaced with a nitrogen atom there is one extra valence electron because nitrogen atom has 5 valence electrons. Thus, one electron doesnt have a pair inside the lattice. That spot becomes vacant. That vacant spot traps the electron in the defect. Together, they form a tiny **atom** inside the diamond that has unpaired electron spins and special energy levels. Due to their unique optical and spin properties, NV centers are among the most promising candidates for room-temperature solid-state qubits and quantum sensors.


**Key properties of NV center in diamond**

| **Property**              | **Details**                                                            |
|---------------------------|------------------------------------------------------------------------|
| **Qubit Type**            | Electron spin (spin-1 system, but often reduced to spin-½ subspace)    |
| **Physical System**       | Point defect in diamond (Nitrogen-Vacancy center)                      |
| **Control Mechanism**     | Microwave pulses + green laser excitation                              |
| **Readout Method**        | Fluorescence emission (red light: bright vs. dim distinguishes states) |
| **Operating Temperature** | Room temperature (very rare for qubits!)                               |
| **Coherence Time**        | Up to milliseconds under ideal conditions                              |




![NV center in diamond](/assets/images/hardwares/NV_center_vacancy.png) 
[NV center in diamond](https://magnetometryrp.quantumtinkerer.tudelft.nl/1_NVbackground/) 



The trapped electron in the NV center behaves like a small magnet with a spin. The spin state can be 0 or 1 for a two level qubit system. When you shine a green laser on NV center, photons are absorbed and emits fluroscence (usually red photons).If th electron is in 0 state, bright red light is emitted. If the electron is in 1 state, the fluorscence emitted is dimmer.

When you apply microwave pulse electron spins can be changed. By adjusting the pulse length, power, and phase, you can perform precise “quantum gates” on that one NV qubit. The NV center’s electron spin is surprisingly well-isolated from the surrounding diamond, so it can stay “coherent” (i.e., keep its quantum state) for milliseconds at room temperature—long enough to do many logical operations or sensing tasks.

**Variants of Color Centers (Defect Qubits)**

There is not only one defect point in diamonds. There can be several defect points(also called “color centers” because they often change the way the diamond absorbs or emits light). For ex:

1. **Nitrogen vacancy**

 - It’s created when a nitrogen atom replaces a carbon atom next to an empty spot (a **vacancy**). 

 - Works at room temperature

 - When hit with green laser light, it glows red, and the brightness tells us what state the electron spin is in

 - You can flip the spin with microwaves and use it like a quantum bit (qubit)

 - ![NV center in diamond](https://ars.els-cdn.com/content/image/1-s2.0-S0079656522000322-gr3_lrg.jpg) 
 

2. **Silicon vacancy (SiV)**

  - A silicon atom replaces two carbon atoms in the diamond and sits between two vacancies.

  - Gives off very sharp and stable light (good for communication)

  - Not as noisy as NV centers

  - Needs very low temperatures (liquid helium kind of cold) to work well.
 
  - ![Structure of the SiV center with a silicon atom in a split vacancy site](/assets/images/hardwares/silicon_vacancy_diamond.png) *Source: [Theoretical study of SiV center](https://doi.org/10.1016/j.diamond.2022.109200)*



3. **Germanium vacancy (GeV)**

  - Similar in shape to SiV, but uses a germanium atom instead

  - Emits light at a slightly different color (around 602 nm)

  - Also great for photon-based communication

  - Still being studied and developed

  - Also prefers cryogenic temperatures

  - ![Germanium vacancy in diamond](/assets/images/hardwares/germanium_vacancy_diamond.png) *Source: [Germanium-Vacancy Color Centers in Diamond](https://pubs.acs.org/doi/10.1021/acs.nanolett.2c01959)*



4. **Tin Vacancy (SnV) or Lead Vacancy (PbV)**

  - These are newer and less explored, but really promising.

  - Bigger atoms like tin and lead distort the diamond structure more

  - That distortion helps split up energy levels, making spin control easier

  - Also need very cold temperatures

  - Could offer longer coherence times—great for stable quantum memory.
 
  - ![Lead Vacancy in diamond](/assets/images/hardwares/lead_vacancy_diamond.png) *Source: [Lead-vacancy centers in diamond as building blocks for large-scale quantum networks](https://phys.org/news/2024-04-vacancy-centers-diamond-blocks-large.html)*


5. **Chromium related or nickel related defects**

  - These are a bit different—mostly studied for their bright single-photon emission.

  - Work at room temperature

  - Not yet fully usable as qubits (still under exploration)

  - Great for making single-photon sources for quantum communication





| Color Center | Main Atom       | Temp Needed | Strength                            | Used For                 |
| ------------ | --------------- | ----------- | ----------------------------------- | ------------------------ |
| NV           | Nitrogen        | Room temp   | Spin control, sensing               | Quantum memory, sensors  |
| SiV          | Silicon         | Cryo        | Very stable optical line            | Quantum communication    |
| GeV          | Germanium       | Cryo        | Photon source, stable emission      | Quantum networking       |
| SnV/PbV      | Tin/Lead        | Cryo        | Long coherence, better spin control | Quantum processors       |
| Cr/Ni        | Chromium/Nickel | Room temp   | Bright photon emission              | Single-photon generation |



**Decoherence and sources of Noise**

| **Source**               | **Description**                                                          |
|--------------------------|---------------------------------------------------------------------------|
| Magnetic noise           | Interaction with nearby nuclear spins in the diamond lattice             |
| Temperature fluctuations | Can affect spin transitions in centers like SiV, GeV (not as much in NV) |
| Strain in the crystal    | Defects and imperfections cause energy level shifts                      |
| Readout noise            | Optical contrast between spin-0 and spin-1 isn't perfect—leads to error  |

**Experimental progress**

- Room temperature quantum sensing - NV centers are used today in magnetic field sensing at the nanoscale. Commerical products are available.

- Entanglement in NV centers - [Entanglement in Nitrogen vacany centers](https://journals.aps.org/prresearch/abstract/10.1103/PhysRevResearch.4.023221) 




**Applications of NV Center in diamond**

1. Quantum sensing
2. Bio medical and life science Imaging



**List of companies working in NV center in diamond and their work/ breakthrough**

1. **Quantum Brilliance**

[Quantum Brilliance](https://quantumbrilliance.com/) 


2. **Diatope**

[Diatope](https://diatope.com/) vision is to provide CVD diamond Made-in-Germany with NV centers for applications in magnetic imaging, nano-NMR and quantum computing.

3. **Quantum Diamond Tech**

The technology behind [Quantum Diamond Tech](https://qdti.com/) platform is that the NV centers are tiny defects in diamond crystal whose electronic states measure the local environment with very high sensitivity and spatial resolution .

4. **NVision**

[NVision](https://www.nvision-imaging.com/) works on new advances in diamond quantum physics (the transformative features of nitrogen vacancies in diamonds) . They developed a product called Polaris. They are fast, robust, and easy-to-use hyperpolarization technology for preclinical, clinical research and clinical applications. This technology transforms existing MRI's into powerful metabolic imagers at scale.

5. **Element Six**

[Element Six](https://www.e6.com/en/about/corporate-information) works in NV center quantum computing technology. Their synthetic diamond supermaterials are used in various industrial applications such as optics, power transmission, water treatment, semiconductor and sensors.

6. **XeedQ**
[XeedQ](https://xeedq.com/) has built the world's first multi-qubit mobile quantum processor. They delivered their **Baby Diamond** 5-qubit quantum computer to Goethe University, to enhance academic exploration in this field.

7. **SaxonQ**
[SaxonQ](https://www.saxonq.com/en/) mission is to develop high performance quantum computers working with NV technology under real-world conditions at room temperature.

8. **HIQUTE Diamond**

[HIQUTE Diamond](https://hiqute-diamond.com/) using NV center for Quantum sensing applications.



**Universities working in nv center in diamonds**

1. **Fraunhofer IAF** Working to build room-temperature based quantum computer. [Link to the article]( https://www.spinning-quantencomputing.de/en/news/development-successes-in-diamond-spin-photon-quantum-computers.html) 


2. **KIT Physikalisches Institut** Have developed a method to precisely control diamond tin-vacancy qubits. They used microwave control and superconducting waveguides for this method to control diamond qubits and its considered as a step toward scalable quantum computing and secure quantum communication systems. [Link to the paper](https://journals.aps.org/prx/abstract/10.1103/PhysRevX.14.031036)


3. **Cornell University** has enhanced diamond capabilties as one of the leading materials in quantum sensors. [Link to the paper](https://journals.aps.org/prapplied/abstract/10.1103/PhysRevApplied.22.024016)


4. **Okayama University** in their [recent work](https://pubs.acs.org/doi/10.1021/acsnano.4c03424) have developed quantum-grade nano-diamonds for Bioimaging and Quantum sensing applications.


5. **University of Tsukuba** developed a new method for implementing magnetic field measurements in a well-known quantum sensing system. [Link to the paper](https://pubs.aip.org/aip/app/article/7/6/066105/2835145/Ultrafast-opto-magnetic-effects-induced-by
)

In short, diamond qubits are preferred in more quantum sensing based applications. Because, diamond qubits have the advantage of existing in the solid phase, making them easier to work with than other quantum materials. 

 

**Some Insightful articles/ sources**

1. [Brief read about NV center -1](https://www.azoquantum.com/article.aspx?ArticleID=325)

2. [Brief read about NV center-2](https://euclidtechlabs.com/2025/01/15/the-quantum-potential-of-nitrogen-vacancy-diamonds/)

3. [Deep explanation about NV center]( https://www.cambridge.org/core/journals/mrs-bulletin/article/diamond-nv-centers-for-quantum-computing-and-quantum-networks/978A4B94242CF28F9C60F0D9E95E9CBD)

4.  [NV center in Science journal](https://www.science.org/doi/10.1126/science.1158340) -> This paper will be a good read if you have access to Science journals.

 



