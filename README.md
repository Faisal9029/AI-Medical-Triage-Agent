
# 🧑‍⚕️ AI Medical Triage Agent

An AI-powered medical triage assistant built with **Python**, **Streamlit**, and **Groq API**. This app allows users to describe their symptoms using **text or voice**, then intelligently:

- Detects the **medical issue**
- Suggests the **relevant doctor/specialist**
- Provides **basic advice**
- Supports **multiple languages**
- Remembers chat history during a session
- Offers a toggle for **dark/light themes**

---

## 🚀 Demo

![Demo Screenshot](doctor_avatar.png) <!-- Add your screenshot here -->
> "I'm feeling shortness of breath and chest tightness."
>  
> 🧑‍⚕️ AI Doctor: "These symptoms may indicate a cardiac issue. Please consult a **cardiologist**..."

---

## 🛠️ Features

- ✅ Text + Voice input
- ✅ Language auto-detection + bilingual replies
- ✅ Specialist detection (e.g., neurologist, cardiologist, etc.)
- ✅ Streamlit interface with avatar-based UI
- ✅ Theme toggle (dark/light)
- ✅ Chat history memory
- ✅ Clean UX for mobile & desktop

---

## 📦 Tech Stack

- `Python`
- `Streamlit`
- `Groq API (LLaMA3)`
- `LangDetect`
- `SpeechRecognition (optional)`
- `Pydub`
- `OpenAI-compatible client`

---

## 🔧 Installation

```bash
git clone https://github.com/Faisal9029/ai-medical-triage-agent.git
cd ai-medical-triage-agent
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
"# AI-Medical-Triage-Agent" 
