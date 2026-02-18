import streamlit as st
import google.generativeai as genai

# Clean UI for Mobile
st.set_page_config(page_title="Smile Finance AI", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: white; }
    .stChatMessage { font-size: 20px !important; color: #1f1f1f; font-family: sans-serif; }
    </style>
    """, unsafe_allow_index=True)

# System Prompt as per your instructions
SYSTEM_PROMPT = """Tum ek insaan ki tarah baat karne wale Financial Dost ho. 
Smile Finance Solution ke liye kaam karte ho. 
Wording hamesha saaf, badi aur clean rakho. 
Customer ki need analyze karo, shuru mein koi bank name mat lo. 
Zaroorat padne par hi landing page aur Amazon ID smileai24-21 use karo."""

# API Connection
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=SYSTEM_PROMPT)
else:
    st.error("Secrets mein GEMINI_API_KEY nahi mili!")

st.title("💰 Smile Finance AI")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Boliye dost, kya baat hai?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = model.generate_content(prompt)
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
