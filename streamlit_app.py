import streamlit as st
import google.generativeai as genai
from groq import Groq
import PIL.Image
import urllib.parse

# Page configuration
st.set_page_config(page_title="Zenith AI Pro", page_icon="💠", layout="wide")

# Sidebar
with st.sidebar:
    st.title("💠 Zenith AI Pro")
    st.info("👤 **Shaikh Raja**\n\nLead Developer")
    uploaded_file = st.file_uploader("Photo upload kijiye...", type=['png', 'jpg', 'jpeg'])
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# API Connections (The Perfect Setup)
try:
    # Gemini Setup with 'rest' transport to fix 404
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"], transport='rest')
    vision_model = genai.GenerativeModel('models/gemini-1.5-flash')
    
    # Groq Setup for fast chatting
    groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception as e:
    st.error(f"API Setup Error: {e}")

st.title("💠 Zenith AI")
st.caption("Powered by Gemini 1.5 & Nano Banana | Created by Shaikh Raja")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Main Logic
if prompt := st.chat_input("Baat karein, Photo upload karein ya Image banwayein..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # 1. VISION MODULE (GEMINI 1.5 FLASH)
        if uploaded_file:
            try:
                img = PIL.Image.open(uploaded_file)
                st.image(img, caption="Aapki Photo", width=300)
                response = vision_model.generate_content([prompt, img])
                msg = response.text
                st.markdown(msg)
            except Exception as e:
                st.error(f"Vision Error: {e}")
                msg = "Maaf kijiye, main ye photo abhi nahi dekh pa raha hoon."
        
        # 2. IMAGE GEN MODULE (NANO BANANA / POLLINATIONS)
        elif any(word in prompt.lower() for word in ["bnao", "image", "photo", "generate", "banana"]):
            encoded = urllib.parse.quote(prompt)
            # Nano Banana model logic inside Pollinations
            url = f"https://pollinations.ai/p/{encoded}?width=1024&height=1024&nologo=true&model=flux"
            st.image(url, caption=f"Nano Banana Art: {prompt}")
            msg = f"Maine aapke liye '{prompt}' ki image bana di hai!"
            st.markdown(msg)

        # 3. CHAT MODULE (LLAMA 3.3)
        else:
            try:
                chat_res = groq_client.chat.completions.create(
                    messages=[{"role": "system", "content": "You are Zenith AI Pro, a powerful assistant created by Shaikh Raja."}] + st.session_state.messages,
                    model="llama-3.3-70b-versatile",
                )
                msg = chat_res.choices[0].message.content
                st.markdown(msg)
            except Exception as e:
                st.error("Chat connection error!")
                msg = "Abhi baat karne mein thodi dikkat ho rahi hai."
        
        st.session_state.messages.append({"role": "assistant", "content": msg})

