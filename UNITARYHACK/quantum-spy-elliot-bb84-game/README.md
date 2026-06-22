# 🔵 Elliot the Electron: The Safety Passage

An interactive educational quantum game teaching the BB84 protocol, quantum cryptography, and the No-Cloning Theorem.

Built for Quantum Universal Education — unitaryHACK 2026
Bounty: Program a Quantum Game ($200)

---

# 🎮 About the Game

You are Elliot, an electron traveling through a quantum communication network. Your best friend is Flash ⚡, a photon messenger helping transmit quantum information between Alice and Bob.

But Eve the eavesdropper is hiding in the network, attempting to intercept the secret quantum key.

Your only defense: the BB84 protocol.

Choose the correct quantum shield. If Eve measures using the wrong basis, the quantum state changes and her presence can be detected.

Over many rounds, players learn how the laws of quantum mechanics make secure quantum communication possible.

---

# 🧠 What Players Learn

| Concept               | Description                                                              |
| --------------------- | ------------------------------------------------------------------------ |
| Superposition         | A qubit can exist in a combination of basis states                       |
| Measurement           | Observing a quantum state changes the system                             |
| No-Cloning Theorem    | Unknown quantum states cannot be perfectly copied                        |
| Diagonal Basis States | The |+\⟩ and |−⟩ states help reveal eavesdropping                        |
| BB84 Protocol         | Quantum key distribution secured by quantum physics                      |
| Entanglement          | Quantum systems can exhibit correlations stronger than classical systems |

---

# 🔬 Qiskit Demonstration of the No-Cloning Principle

The game includes a Qiskit circuit demonstrating why arbitrary quantum states cannot be copied using standard quantum operations.

## Circuit Overview

* An H gate prepares the superposition state |+\⟩
* A CNOT operation attempts to duplicate the state onto a second qubit
* Instead of producing two independent copies, the circuit creates an entangled Bell state

Measurement results reveal strong quantum correlations characteristic of entanglement rather than cloning.

## Why This Matters

This experiment demonstrates that operations capable of copying classical bits do not generally clone arbitrary quantum states.

That limitation is one of the key ideas behind the No-Cloning Theorem and forms part of the security foundation of the BB84 quantum key distribution protocol.

## Important Scientific Note

This notebook provides an educational demonstration, not a formal mathematical proof of the No-Cloning Theorem.

A full proof follows from the linearity and unitarity of quantum mechanics, which show that no universal operation can perfectly clone arbitrary unknown quantum states.

---

# 📘 Mathematical Idea Behind No-Cloning

Suppose a universal cloning operation U could copy any quantum state:

U(|ψ⟩|0⟩) = |ψ⟩|ψ⟩

and also:

U(|φ⟩|0⟩) = |φ⟩|φ⟩

Because quantum operations preserve inner products:

⟨ψ|φ⟩ = ⟨ψ|φ⟩²

This equation is only satisfied when states are identical or orthogonal.

Therefore, no universal quantum operation can perfectly clone arbitrary unknown quantum states.

---

# ▶️ How to Play

1. Open `elliot_game.ipynb` in Google Colab or Jupyter Notebook
2. Run all notebook cells
3. Click 📖 Menu to read the story and gameplay rules
4. Use 🛡️ Z-Shield or 🛡️ X-Shield during each round
5. Observe whether Eve is detected during transmission
6. After 8 rounds, review your quantum communication results
7. Run the Qiskit demonstration to explore the no-cloning principle interactively

---

# 👤 Characters

| Character | Role                                                     |
| --------- | -------------------------------------------------------- |
| 🔵 Elliot | The electron messenger                                   |
| ⚡ Flash   | The photon communication partner                         |
| 📡 Alice  | Sender of quantum states                                 |
| 📡 Bob    | Receiver and measurement operator                        |
| 👤 Eve    | The eavesdropper attempting to intercept the quantum key |

---

# 🎯 Target Audience

* Beginners in quantum computing
* High school and undergraduate students
* STEM outreach programs
* Self-learners exploring Qiskit and BB84
* Educators introducing quantum information concepts

---

# 📦 Dependencies

* Python 3.7+
* ipywidgets
* qiskit
* qiskit-aer

Install dependencies:

pip install ipywidgets qiskit qiskit-aer

---

# 🤖 AI Usage Disclosure

In accordance with unitaryHACK's Ethical AI policy:

AI Tool Used: DeepSeek

AI assistance was used for Python code structure suggestions, interface styling support, and markdown formatting based on the project's original educational concept and gameplay design.

The game concept, characters, educational structure, scientific explanations, and quantum learning framework are original work created and directed by the author.

All code was manually tested and reviewed for correctness. The quantum concepts and explanations were independently verified and refined by the author.

---

# 🚀 My Quantum Journey

I entered quantum computing through a nontraditional path. With a background in English Literature and diplomas in Computer Science, Teaching, and Data Analysis, I later taught myself quantum mechanics, Python, and Qiskit through MIT OpenCourseWare, Stanford Online, and hands-on experimentation.

Today I contribute to quantum education and outreach as:

* IBM Qiskit Advocate (2025)
* Friend of OQI, Open Quantum Institute at CERN (2026)
* Mentor, Qiskit Advocate Mentorship Program (QAMP)

I believe quantum education should be accessible to learners from both STEM and nontraditional backgrounds.

This project was created to teach quantum concepts through storytelling, interaction, and play.

---

# 📂 Repository Structure

elliot_game.ipynb   — Main interactive notebook
README.md           — Project documentation
LICENSE             — MIT License

---

# 📄 License

MIT License

---

# 🔗 Links

GitHub: learningdungeon

Sentinel Framework DOI: 10.5281/zenodo.20464416

YouTube Demo: https://www.youtube.com/watch?v=pCbDTv2Wl2I
