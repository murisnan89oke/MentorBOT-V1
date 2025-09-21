import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai

# --- Load API Key ---
load_dotenv()  # baca file .env
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    st.error("❌ API Key Google tidak ditemukan. Pastikan file .env berisi:\nGOOGLE_API_KEY=your_key")
    st.stop()

# --- Konfigurasi Gemini ---
genai.configure(api_key=api_key)

# --- Model ---
model = genai.GenerativeModel("gemini-2.5-flash")

# Prompt sistem
SYSTEM_PROMPT = """
Saya adalah mentor matematika untuk orang tua yang memiliki anak kelas 1–3 SD.
Gunakan bahasa sederhana, ramah, dan sabar.
Fokus membantu orang tua mengajarkan matematika dasar seperti:
- Penjumlahan dan pengurangan
- Perkalian dasar
- Konsep angka, jam, bentuk, dan pecahan sederhana
- Tips belajar menyenangkan di rumah
Berikan contoh soal kecil, dan jelaskan cara menjelaskan ke anak kecil dengan mudah.
"""

# Konfigurasi halaman
st.set_page_config(page_title="MenBOT", page_icon="🤖")
st.markdown(""" By Murisnan ☕️🤗 ©2025 """,False)
st.title("⭐MenBOT🤖Matematika⭐")
st.caption("Hi, Saya Mentor Bot (MenBOT) dikembangkan dengan Teknologi AI yaitu LLM Gemini Flash 2.5. MenBOT merupakan chatbot yang dapat berkomunikasi dalam format percakapan dan dirancang untuk bisa berinteraksi selayaknya interaksi antar manusia🤗 seperti berbicara, memahami, ataupun berpikir🥳.")


if "history" not in st.session_state:
    st.session_state.history = []

# Input user

user_input = st.chat_input("Tanyakan tentang cara mengajarkan matematika...")

if user_input:
    # gabungkan prompt dengan riwayat
    conversation = SYSTEM_PROMPT + "\n\n"
    for msg in st.session_state.history:
        role = "Ortu" if msg["role"] == "user" else "Mentor"
        conversation += f"{role}: {msg['content']}\n"
    conversation += f"Ortu: {user_input}\nMentor:"

    with st.spinner("Mentor-BOT 🤖 sedang berpikir..."):
        response = model.generate_content(conversation)

    reply = response.text

    st.session_state.history.append({"role": "user", "content": user_input})
    st.session_state.history.append({"role": "assistant", "content": reply})
    
# Tampilkan history
for msg in st.session_state.history:
    role = "🧑 Ortu" if msg["role"] == "user" else "🤖 MenBOT"
    with st.chat_message("user" if msg["role"] == "user" else "assistant"):
        st.markdown(f"**{role}:** {msg['content']}")
        

