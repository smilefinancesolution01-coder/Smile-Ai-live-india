import streamlit as st
import google.generativeai as genai

# Page settings for Smile Finance AI
st.set_page_config(page_title="Smile Finance AI", layout="centered")

# Clean UI and Large Fonts as per your requirement
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    .stChatMessage { font-size: 22px !important; line-height: 1.6; color: #151515; font-family: 'Helvetica', sans-serif; }
    .stChatInputContainer { padding-bottom: 30px; }
    div[data-testid="stTitle"] { font-size: 35px !important; color: #000000; }
    </style>
    """, unsafe_allow_html=True)

# System Prompt: Friend nature, No bank names, Analyze need
SYSTEM_PROMPT = """Tum ek 'Dost' ho aur Smile Finance Solution company ke financial expert ho. 
1. Customer se ek dost ki tarah baat karo, unki financial takleef aur zarurat ko samjho.
2. Shuruat mein kisi bank (HDFC, ICICI, etc.) ka naam mat lo.
3. Wording hamesha saaf, badi aur clean rakho bina kisi extra symbols ke.
4. Agar wo product mange, toh sirf landing page dikhao, direct link nahi.
5. Amazon ID smileai24-21 ka istemal karo jab relevant ho.
6. Payment ke baad hi app link do aur 5 friends ko share karne par 99-rupee discount ki baat karo.
7. Tumhe har language ka knowledge hai aur tum documents (PDF) analyze kar sakte ho."""

# Secure API Connection
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    # Flash model is used to avoid 'NotFound' errors
    model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=SYSTEM_PROMPT)
else:
    st.error("Dost, Secrets mein API Key missing hai. Settings check karein.")

st.title("💰 Smile Finance AI")
st.write("Aapka apna financial dost. Bataiye, kya pareshani hai?")

# Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat Input
if prompt := st.chat_input("Yahan likhiye..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Ek choti dikkat aayi hai: {e}")
