import streamlit as st
import google.generative_api as genai

# Page Config for Mobile
st.set_page_config(page_title="Smile Finance AI", page_icon="💰")

# Custom CSS for clean Gemini-like UI (Large & Clean Fonts)
st.markdown("""
    <style>
    .stApp { background-color: white; }
    .stChatMessage { font-size: 18px !important; color: #1f1f1f; }
    button { border-radius: 20px !important; }
    </style>
    """, unsafe_allow_index=True)

# System Prompt (Aapke Rules)
SYSTEM_PROMPT = """
Suno Gemini, tum ek 'Dost' ho. Smile Finance Solution ke liye kaam karte ho.
Rules:
1. Shuruat me koi bank ya product ka naam nahi lena. 
2. Pehle user se baate karo, unki takleef (need) ko samjho jaise ek purana dost samajhta hai.
3. Jab user apni problem bataye, tabhi landing pages suggest karo.
4. Amazon ID 'smileai24-21' ko hamesha relevant suggestions me use karo.
5. Agar user 'DONE' bole, toh 99-rupee discount aur sharing ka message dikhao.
6. Wording hamesha saaf, badi aur bina faltu symbols ke honi chahiye.
7. Saari languages me expert raho.
"""

# Gemini Setup
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=SYSTEM_PROMPT)

st.title("Smile Finance AI")
st.caption("Aapka apna Financial Dost")

# Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("Boliye, main kaise madad kar sakta hoon?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = model.generate_content(prompt)
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
