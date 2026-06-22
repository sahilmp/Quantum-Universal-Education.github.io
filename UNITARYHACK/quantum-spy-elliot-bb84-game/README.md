# 🔵 Elliot the Electron: The Safety Passage

An interactive educational quantum game teaching the **BB84 protocol**, **quantum cryptography**, and the **No-Cloning Theorem**.

Built for [Quantum Universal Education](https://github.com/Quantum-Universal-Education/Quantum-Universal-Education.github.io) — **unitaryHACK 2026**  
**Bounty:** Program a Quantum Game ($200) | **Issue:** #54

---

## 🎮 About the Game

You are **Elliot**, an electron traveling through a quantum communication network. Your best friend is **Flash** ⚡, a photon messenger helping transmit quantum information between Alice and Bob.

But **Eve** the eavesdropper is hiding in the network, attempting to intercept the secret quantum key.

Your only defense: the **BB84 protocol**.

Choose the correct quantum shield. If Eve measures using the wrong basis, the quantum state changes and her presence can be detected.

**Every round shows live Qiskit output** — you watch the physics happen in real time as each qubit is transmitted.

---

## 🧠 What Players Learn

| Concept | Description |
|---------|-------------|
| **Superposition** | A qubit can exist in a combination of basis states |
| **Measurement** | Observing a quantum state changes the system |
| **No-Cloning Theorem** | Unknown quantum states cannot be perfectly copied |
| **Diagonal Basis States** | The \|+⟩ and \|−⟩ states help reveal eavesdropping |
| **BB84 Protocol** | Quantum key distribution secured by quantum physics |
| **Entanglement** | Quantum systems exhibit correlations stronger than classical systems |

---

## 🔬 Live Qiskit Demonstration — Every Round

Each round includes a **mini Qiskit simulation** showing what happens when Eve's CNOT "copy" attempt is applied to Alice's actual qubit:

- **\|0⟩ and \|1⟩ (Z-basis):** CNOT appears to copy — but only because these are orthogonal (classical) states. The No-Cloning Theorem permits this.
- **\|+⟩ and \|−⟩ (X-basis):** CNOT fails. Instead of a copy, the qubits become **entangled** (Bell state). The measurement statistics reveal the difference.

This live feedback builds intuition across all 8 rounds.

---

## 🔒 Full No-Cloning Demo (Unlocked After Game Completion)

After completing all 8 rounds, the **🔬 Cloning Demo** button unlocks. This provides:

- A detailed Qiskit simulation of CNOT failing on \|+⟩
- A complete explanation of the **mathematical proof** via linearity and unitarity
- The inner product derivation: ⟨ψ\|φ⟩ = ⟨ψ\|φ⟩²
- Why only orthogonal or identical states can be copied

**Important Scientific Note:** The circuit demonstration is educational, not a formal proof. The actual proof follows from the linearity of quantum mechanics.

---

## ▶️ How to Play

1. Open `elliot_game.ipynb` in Google Colab or Jupyter Notebook
2. Run all notebook cells
3. Click **📖 Menu** to read the story and gameplay rules
4. Use **🛡️ Z-Shield** or **🛡️ X-Shield** during each round
5. Watch the live Qiskit output showing the cloning attempt result
6. Observe whether Eve is detected during transmission
7. After 8 rounds, review your quantum communication results
8. Click **🔬 Cloning Demo** to explore the full No-Cloning demonstration

---

## 👤 Characters

| Character | Role |
|-----------|------|
| 🔵 **Elliot** | The electron messenger |
| ⚡ **Flash** | The photon communication partner |
| 📡 **Alice** | Sender of quantum states |
| 📡 **Bob** | Receiver and measurement operator |
| 👤 **Eve** | The eavesdropper attempting to intercept the quantum key |

---

## 🎯 Target Audience

- Beginners in quantum computing
- High school and undergraduate students
- STEM outreach programs
- Self-learners exploring Qiskit and BB84
- Educators introducing quantum information concepts

---

## 📦 Dependencies

- Python 3.7+
- `ipywidgets`
- `qiskit`
- `qiskit-aer`

Install dependencies:

```bash
pip install ipywidgets qiskit qiskit-aer
````

## 🤖 AI Usage Disclosure

In accordance with unitaryHACK's Ethical AI policy:

- **AI Tool Used:** DeepSeek
- **AI Assistance:** Python code structure suggestions, HTML/CSS interface styling, and markdown formatting based on the project's original educational concept and gameplay design.
- **Human-Created:** The game concept (Elliot the Electron, BB84 Safety Passage), all quantum physics explanations, character narrative, educational structure, and gameplay design are entirely original work. All code was manually tested and verified on Google Colab.

---

## 🚀 My Quantum Journey

I entered quantum computing through a nontraditional path. With a background in English Literature and diplomas in Computer Science, Teaching, and Data Analysis, I later taught myself quantum mechanics, Python, and Qiskit through MIT OpenCourseWare, Stanford Online, and hands-on experimentation.

Today I contribute to quantum education and outreach as:

- **IBM Qiskit Advocate** (2025)
- **Friend of OQI**, Open Quantum Institute at CERN (2026)
- **Member, IEEE GRSS QUEST Technical Committee**
- **Mentor, Qiskit Advocate Mentorship Program (QAMP)**
- **Only participant from Pakistan to pass IBM QGSS** under anti-LLM conditions

I believe quantum education should be accessible to learners from both STEM and nontraditional backgrounds. This project was created to teach quantum concepts through storytelling, interaction, and play.

---

## 📂 Repository Structure
- **elliot_game.ipynb** — Main interactive notebook
- **README.md** — Project documentation
 

---

## 📄 License

MIT License

---

## 🔗 Links

- **GitHub:** [learningdungeon](https://github.com/learningdungeon)
- **Sentinel Framework DOI:** [10.5281/zenodo.20464416](https://doi.org/10.5281/zenodo.20464416)
- **YouTube Demo:** [https://www.youtube.com/watch?v=pCbDTv2Wl2I](https://www.youtube.com/watch?v=pCbDTv2Wl2I)
- **Quantum Universal Education:** [Repo](https://github.com/Quantum-Universal-Education/Quantum-Universal-Education.github.io)

---

*"Physics protects our secrets. The No-Cloning Theorem is undefeated."* — 🔵 Elliot
