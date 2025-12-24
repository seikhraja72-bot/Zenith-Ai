import streamlit as st
import google.generativeai as genai
from groq import Groq
import PIL.Image
import urllib.parse
import io

# 1. Page Config (Mere jaisa blue/white theme aur icon)
st.set_page_config(page_title="Zenith AI", page_icon="💠", layout="centered")

# CSS for a clean UI (Sidebar chupane ke liye)
st.markdown("""
    <style>
        [data-testid="stSidebar"] {display: none;}
        .stDeployButton {display:none;}
        footer {visibility: hidden;}
        #MainMenu {visibility: hidden;}
    </style>
""", unsafe_allow_stdio=True)

# API Connections
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"], transport='rest')
    vision_model = genai.GenerativeModel('models/gemini-1.5-flash')
    groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception as e:
    st.error("Connection Error!")

# Logo aur Title (Aapka custom naam yahan aayega)
st.markdown("<h2 style='text-align: center;'>💠 Zenith AI</h2>", unsafe_allow_stdio=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Chat History Display
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Photo Upload (Chat input ke upar)
uploaded_file = st.file_uploader("", type=['png', 'jpg', 'jpeg'], label_visibility="collapsed")

# User Input
if prompt := st.chat_input("Mujhse kuch bhi puchiye..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # 1. VISION (GEMINI)
        if uploaded_file:
            try:
                img = PIL.Image.open(uploaded_file)
                response = vision_model.generate_content([prompt, img])
                msg = response.text
                st.markdown(msg)
            except:
                msg = "Photo processing mein dikkat hui."
                st.markdown(msg)
        
        # 2. IMAGE GENERATION (Ab 'Nano Banana' likha nahi aayega)
        elif any(word in prompt.lower() for word in ["bnao", "image", "photo", "generate"]):
            encoded = urllib.parse.quote(prompt)
            url = f"https://pollinations.ai/p/{encoded}?width=1024&height=1024&nologo=true"
            st.image(url)
            msg = "Maine aapki image taiyar kar di hai."
        
        # 3. CHAT (LLAMA 3.3)
        else:
            try:
                chat_res = groq_client.chat.completions.create(
                    messages=[{"role": "system", "content": "You are Zenith AI, a smart assistant."}] + st.session_state.messages,
                    model="llama-3.3-70b-versatile",
                )
                msg = chat_res.choices[0].message.content
                st.markdown(msg)
            except:
                msg = "System busy hai."
                st.markdown(msg)
        
        st.session_state.messages.append({"role": "assistant", "content": msg})

