# quantum-spy-elliot-bb84-game
Elliot the Electron:  BB84 Quantum Educational Game.  Teaches No-Cloning Theorem &amp; Quantum Cryptography.  Built for unitaryHACK 2026. Includes Qiskit proof on real hardware.
# 🔵 Elliot the Electron: The Safety Passage

**An educational quantum game teaching BB84, the No-Cloning Theorem, and Quantum Cryptography.**

Built for [Quantum Universal Education](https://github.com/Quantum-Universal-Education) — unitaryHACK 2026  
**Bounty:** Program a Quantum Game ($200) | **Issue:** #54

---

## 🎮 About the Game

You are **Elliot**, an electron living inside a quantum wire. Your best friend is **Flash** ⚡ — a photon who carries you at the speed of light. Together, you deliver secret messages between Alice and Bob.

But **Eve** the eavesdropper is hiding in the wire, trying to steal your secrets. Your only weapon: the **BB84 protocol**.

Choose the right quantum shield. If Eve guesses wrong — you catch her. If she guesses right — she steals the secret. But over many rounds, physics guarantees she always leaves a trace.

---

## 🧠 What Players Learn

| Concept | Description |
|---------|-------------|
| Superposition | A qubit can be 0 AND 1 at the same time |
| Measurement | Observing a quantum state destroys it |
| No-Cloning Theorem | You CANNOT copy an unknown quantum state |
| Diagonal States | The + and − states are the trap that exposes Eve |
| BB84 Protocol | Quantum Key Distribution — security guaranteed by physics |

---

## 🔬 Real Quantum Hardware Proof

The game includes a **Qiskit circuit** that proves the No-Cloning Theorem:

- H gate on qubit 0 creates |+⟩
- CNOT(q0,q1) attempts to copy
- Result: Bell state (entanglement), NOT a copy
- Only 00 and 11 appear — 01 and 10 never appear

This is why BB84 works. This is not a game mechanic. This is **physics**.

---

## ▶️ How to Play

1. Open `elliot_game.ipynb` in Google Colab or Jupyter
2. Run all cells
3. Click **📖 Menu** to read the story and rules
4. Click **🛡️ Z-Shield** or **🛡️ X-Shield** to play each round
5. After 8 rounds, see your results
6. Click **🔬 Run Qiskit Proof** to see the No-Cloning Theorem on real quantum hardware

---

## 👤 Characters

| Character | Role |
|-----------|------|
| 🔵 **Elliot** | You! An electron messenger |
| ⚡ **Flash** | Your photon best friend. Speed of light. Maximum loyalty. |
| 📡 **Alice** | Sends secret qubits |
| 📡 **Bob** | Receives and measures |
| 👤 **Eve** | The eavesdropper. She never wins in the long run. |

---

## 📦 Dependencies

- Python 3.7+
- `ipywidgets` — interactive GUI
- `qiskit` — quantum circuit simulation
- `qiskit-aer` — Qiskit simulator backend

Install: `pip install ipywidgets qiskit qiskit-aer`

---

## 🤖 AI Usage Disclosure

In accordance with unitaryHACK's Ethical AI policy:

- **AI Tool Used:** DeepSeek
- **AI Assistance:** DeepSeek helped generate Python code structure, HTML/CSS styling for the Colab GUI, and markdown formatting based on my game concept, quantum explanations, and design direction.
- **Human-Created:** The game concept (Elliot the Electron, BB84 Safety Passage), all quantum physics explanations, character narrative, educational structure, and gameplay design are entirely my original work based on my study of MIT 8.04 Quantum Physics, the No-Cloning Theorem, and the BB84 protocol. I directed all code generation, manually tested all outputs, and verified correctness.
- **Verification:** All code manually tested on Google Colab. I understand every quantum concept presented and can explain each line of code to a maintainer if asked.

---

## 🚀 My Quantum Journey

I came to quantum computing through an unconventional path.

I hold an MA in English Literature. With Computer Science Diplomas and Teaching with Data Analysis. I could not study sciences when I was young for family responsibilities came first. Years later, I returned to my passion. I taught myself quantum mechanics from MIT OCW 8.04 and Stanford Online. I learned Python, Qiskit, and NetSquid from scratch.

Today I am:
- **IBM Qiskit Advocate** (2025)
- **Friend of OQI**, Open Quantum Institute at CERN (2026)
- **Member, IEEE GRSS QUEST Technical Committee**
- **Mentor, Qiskit Advocate Mentorship Program (QAMP)**
- **Only participant from Pakistan to pass IBM QGSS** under anti-LLM conditions

I built **RAQT**, a quantum network protocol for anonymous transmission, tested on IBM Quantum and Origin Wuyuan. I published the **Sentinel Framework**, a national quantum curriculum for Pakistan.

I call my path **STEAM** — with an A for Arts added to STEM.

This game is my way of teaching quantum concepts the way I wish someone had taught me: with stories, with play, and with heart.

---

## 📄 License

MIT License — see [LICENSE](LICENSE) file.

---

## 🔗 Links

- **GitHub:** [learningdungeon](https://github.com/learningdungeon)
- **Sentinel Framework DOI:** [10.5281/zenodo.20464416](https://doi.org/10.5281/zenodo.20464416)
- **Quantum Universal Education:** [Repo](https://github.com/Quantum-Universal-Education/Quantum-Universal-Education.github.io)

---

*"Physics protects our secrets. The No-Cloning Theorem is undefeated."* — 🔵 Elliot
