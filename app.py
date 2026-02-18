import streamlit as st
import google.generativeai as genai

# Mobile ke liye screen aur font adjust karna
st.set_page_config(page_title="Smile Finance AI", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    .stChatMessage { font-size: 20px !important; line-height: 1.6; color: #1f1f1f; }
    .stChatInputContainer { padding-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# Aapka Bataya hua Gemini Nature (System Instruction)
SYSTEM_PROMPT = """Tum ek 'Dost' ho aur Smile Finance Solution ke liye kaam karte ho. 
1. Tumhe Gemini ki tarah samajhdaar aur human-like baate karni hai. 
2. Shuruat mein kisi bank ya product ka naam nahi lena. 
3. Pehle customer se dosti karo, unki financial zarurat ko samjho. 
4. Jab zarurat ho, tabhi landing page suggest karo aur Amazon ID smileai24-21 use karo.
5. Wording hamesha saaf, badi aur clean rakho (No extra symbols). 
6. Tumhe duniya ka saara knowledge hai aur tum har language jaante ho."""

# Gemini API Connection
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=SYSTEM_PROMPT)
else:
    st.error("Dost, Settings (Secrets) mein GEMINI_API_KEY daalna bhul gaye ho!")

st.title("💰 Smile Finance AI")
st.write("Aapka apna financial dost. Bataiye, aaj main aapki kaise madad kar sakta hoon?")

# Chat History maintain karna
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input (Mic aur Send button automatic android me adjust ho jayega)
if prompt := st.chat_input("Yahan likhiye..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = model.generate_content(prompt)
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
