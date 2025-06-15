import streamlit as st
from dotenv import load_dotenv
import os
from groq import Groq
import speech_recognition as sr
from langdetect import detect
from datetime import datetime

# Load env
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Theme toggle state
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

st.set_page_config(
    page_title="🩺 AI Medical Triage Agent",
    layout="centered"
)

# Sidebar theme switch
theme = st.sidebar.toggle("🌗 Dark Mode", value=st.session_state.dark_mode)
st.session_state.dark_mode = theme

if st.session_state.dark_mode:
    st.markdown("""
        <style>
        body { background-color: #0e1117; color: white; }
        </style>
    """, unsafe_allow_html=True)

# Title
st.title("🩺 AI Medical Triage Agent")
st.markdown("Type or record your symptoms to get instant triage advice and doctor recommendation.")

# Session memory
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful medical triage assistant. Based on the user's symptoms, identify possible conditions, "
                "recommend a relevant doctor (e.g., cardiologist, neurologist), rate urgency (Low/Medium/Emergency), and provide basic advice. "
                "Always respond in English first, then translate the same reply to the user's language if it's not English."
            )
        }
    ]

# Display past conversation
st.markdown("### 💬 Conversation")
for msg in st.session_state.messages[1:]:
    role = "👤 User" if msg["role"] == "user" else "🧠 AI"
    st.markdown(f"**{role}:** {msg['content']}")

# Input method
st.markdown("🎤 Or press to record:")
if st.button("🎙️ Start Voice Input"):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening...")
        audio_data = recognizer.listen(source, phrase_time_limit=5)
        try:
            voice_text = recognizer.recognize_google(audio_data)
            st.success(f"Recognized: {voice_text}")
            st.session_state.voice_input = voice_text
        except sr.UnknownValueError:
            st.error("Sorry, couldn't understand audio.")
        except sr.RequestError as e:
            st.error(f"API error: {e}")

# Text input
user_input = st.chat_input("Type your symptoms...")

# Final input selection
if "voice_input" in st.session_state and st.session_state.voice_input:
    final_input = st.session_state.voice_input
    del st.session_state.voice_input
elif user_input:
    final_input = user_input
else:
    final_input = None

# Urgency evaluator
def get_urgency_rating(text):
    critical = ["chest pain", "unconscious", "bleeding", "difficulty breathing", "severe headache"]
    medium = ["fever", "rash", "vomiting", "infection", "swelling"]
    text_lower = text.lower()
    if any(word in text_lower for word in critical):
        return "🚨 Emergency"
    elif any(word in text_lower for word in medium):
        return "⚠️ Medium"
    return "✅ Low"

# Response generation
if final_input:
    st.session_state.messages.append({"role": "user", "content": final_input})
    with st.spinner("Analyzing..."):
        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=st.session_state.messages
        )
        reply = response.choices[0].message.content

        detected_lang = detect(final_input)
        if detected_lang != "en":
            reply += f"\n\n🌐 Translation ({detected_lang.upper()}): [Translation feature coming soon]"

        urgency = get_urgency_rating(final_input)
        reply += f"\n\n**Urgency Level:** {urgency}"

        st.session_state.messages.append({"role": "assistant", "content": reply})
    st.rerun()

# Reset
if st.button("🔁 Reset Chat"):
    st.session_state.messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful medical triage assistant. Based on the user's symptoms, identify possible conditions, "
                "recommend a relevant doctor (e.g., cardiologist, neurologist), rate urgency (Low/Medium/Emergency), and provide basic advice. "
                "Always respond in English first, then translate the same reply to the user's language if it's not English."
            )
        }
    ]
    st.rerun()

# Export chat
def export_chat():
    chat = ""
    for msg in st.session_state.messages[1:]:
        role = "User" if msg["role"] == "user" else "AI"
        chat += f"{role}: {msg['content']}\n\n"
    return chat

st.download_button("📤 Export Chat", data=export_chat(), file_name=f"chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
