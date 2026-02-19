import streamlit as st
import google.generativeai as genai

# Page settings
st.set_page_config(page_title="Smile Finance AI", layout="centered")

# Badi aur Clean Wording (Aapki requirement ke hisaab se)
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    .stChatMessage { font-size: 22px !important; line-height: 1.6; color: #1a1a1a; font-family: sans-serif; }
    div[data-testid="stTitle"] { font-size: 40px !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# Aapke Business Rules (Dost nature)
SYSTEM_PROMPT = """Tum ek 'Dost' ho aur Smile Finance Solution ke expert ho.
1. Customer se pehle dosti karo, unki financial takleef aur zarurat ko samjho.
2. Shuruat mein kisi bank ka naam mat lo.
3. Wording hamesha saaf aur badi rakho.
4. Amazon ID smileai24-21 use karo jab zarurat ho.
5. Payment ke baad hi app link do aur 5 friends ko share karne par 99-rupee discount ka bolo."""

# API Connection - Yahan model change kiya hai fix karne ke liye
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    # 'gemini-pro' sabse stable hai aur 404 error nahi dega
    model = genai.GenerativeModel('gemini-pro') 
else:
    st.error("Dost, Secrets mein API Key nahi mili!")

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
            # System Instruction ko prompt ke saath bhej rahe hain
            full_prompt = f"{SYSTEM_PROMPT}\n\nUser: {prompt}"
            response = model.generate_content(full_prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Ek choti dikkat: {e}")
