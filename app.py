import streamlit as st
import google.generativeai as genai

# Page Config
st.set_page_config(page_title="Smile Finance AI", layout="centered")

# Badi aur Clean Wording (CSS)
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    .stChatMessage { font-size: 22px !important; color: #1a1a1a; font-family: sans-serif; }
    div[data-testid="stTitle"] { font-size: 40px !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# System Prompt (Aapka Business Logic)
SYSTEM_PROMPT = """Tum ek 'Dost' ho aur Smile Finance Solution ke expert ho.
1. Pehle customer ki financial zarurat aur takleef ko samjho.
2. Shuruat mein bank ka naam mat lo.
3. Wording saaf aur badi rakho.
4. Amazon ID smileai24-21 use karo.
5. Payment ke baad hi app link do aur 5 friends ko share karne par 99-rupee discount ka bolo."""

# API Connection Fix
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    # Sabse stable model use kar rahe hain
    model = genai.GenerativeModel('gemini-1.5-flash') 
else:
    st.error("Secrets mein API Key nahi mili!")

st.title("💰 Smile Finance AI")
st.write("Aapka apna financial dost. Bataiye, kya pareshani hai?")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Yahan likhiye..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # System Instruction ko content ke saath bhej rahe hain for better results
            full_prompt = f"System Instruction: {SYSTEM_PROMPT}\n\nUser: {prompt}"
            response = model.generate_content(full_prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Ek choti dikkat: {e}")
