import streamlit as st
import google.generativeai as genai
from groq import Groq
import PIL.Image
import urllib.parse

st.set_page_config(page_title="Zenith AI", page_icon="💠", layout="wide")

# Sidebar
with st.sidebar:
    st.title("💠 Zenith AI")
    st.info("👤 **Shaikh Raja** (Creator)")
    st.success("✅ Vision, Image & Memory Active")
    # File Uploader for Vision
    uploaded_file = st.file_uploader("Photo dikhaiye...", type=['png', 'jpg', 'jpeg'])

# Setup APIs
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
vision_model = genai.GenerativeModel('gemini-1.5-flash')
groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"])

st.title("💠 Zenith AI")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("Baat kijiye ya image banwaiye..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # 1. VISION LOGIC (Agar photo upload hai)
        if uploaded_file:
            img = PIL.Image.open(uploaded_file)
            st.image(img, caption="Aapki Photo", width=300)
            response = vision_model.generate_content([prompt, img])
            msg = response.text
            st.markdown(msg)
        
        # 2. IMAGE GENERATION LOGIC
        elif any(word in prompt.lower() for word in ["bnao", "image", "photo"]):
            encoded = urllib.parse.quote(prompt)
            url = f"https://pollinations.ai/p/{encoded}?width=1024&height=1024&nologo=true"
            st.image(url, caption=f"Zenith ne banaya: {prompt}")
            msg = "Maine aapke liye photo bana di hai!"
            st.markdown(msg)

        # 3. NORMAL CHAT LOGIC
        else:
            chat_res = groq_client.chat.completions.create(
                messages=[{"role": "system", "content": "You are Zenith AI, created by Shaikh Raja."}] + st.session_state.messages,
                model="llama-3.3-70b-versatile",
            )
            msg = chat_res.choices[0].message.content
            st.markdown(msg)
        
        st.session_state.messages.append({"role": "assistant", "content": msg})

