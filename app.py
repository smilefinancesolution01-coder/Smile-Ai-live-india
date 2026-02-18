import streamlit as st
import google.generativeai as genai

# Mobile Friendly UI
st.set_page_config(page_title="Smile Finance AI", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    .stChatMessage { font-size: 110%; line-height: 1.6; }
    </style>
    """, unsafe_allow_index=True)

# Aapke Rules (Human-like Nature)
SYSTEM_PROMPT = """Tum ek insaan ki tarah baat karne wale Financial Dost ho. 
Smile Finance Solution ke liye kaam karte ho. 
Wording hamesha saaf, badi aur bina faltu symbols ke rakho. 
Customer ki need analyze karo, shuru mein koi bank name mat lo. 
Baad mein landing page dikhao aur Amazon ID smileai24-21 use karo."""

# API Key Connection
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=SYSTEM_PROMPT)
else:
    st.error("Please add GEMINI_API_KEY in Streamlit Secrets!")

st.title("💰 Smile Finance AI")
st.write("Aapka apna financial dost. Bataiye, kya pareshani hai?")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if prompt := st.chat_input("Kaise madad karoon?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        response = model.generate_content(prompt)
        st.write(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
