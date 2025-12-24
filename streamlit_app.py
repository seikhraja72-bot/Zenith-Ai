
import streamlit as st
import google.generativeai as genai
from groq import Groq
import PIL.Image
import urllib.parse

# Page Setup
st.set_page_config(page_title="Zenith AI", page_icon="💠", layout="wide")

# Sidebar Design
with st.sidebar:
    st.title("💠 Zenith AI")
    st.info("👤 **Shaikh Raja**\n\nLead Developer")
    st.success("✅ Llama + Gemini Active")
    # Vision Feature: Photo upload karne ka button
    uploaded_file = st.file_uploader("Photo upload kijiye...", type=['png', 'jpg', 'jpeg'])
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# API Connections
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    # Naya model name jo 100% chalega
    vision_model = genai.GenerativeModel('gemini-1.5-flash-latest')
    groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception as e:
    st.error(f"Galti: {e}")


st.title("💠 Zenith AI")
st.caption("The Peak of Intelligence | Created by Shaikh Raja")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Purani baatein dikhana (Memory)
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("Zenith se kuch bhi puchiye..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # 1. AGAR PHOTO UPLOAD HAI (VISION)
        if uploaded_file:
            try:
                img = PIL.Image.open(uploaded_file)
                st.image(img, caption="Aapki Photo", width=300)
                response = vision_model.generate_content([prompt, img])
                msg = response.text
                st.markdown(msg)
            except Exception as e:
                st.error(f"Vision Error: {e}")
                msg = "Maaf kijiye, photo dekhne mein dikkat hui."
        
        # 2. AGAR PHOTO BANWANI HAI (IMAGE GENERATION)
        elif any(word in prompt.lower() for word in ["bnao", "image", "photo", "generate"]):
            encoded = urllib.parse.quote(prompt)
            url = f"https://pollinations.ai/p/{encoded}?width=1024&height=1024&nologo=true"
            st.image(url, caption=f"Zenith ne banaya: {prompt}")
            msg = f"Maine aapke liye '{prompt}' ki image bana di hai!"
            st.markdown(msg)

        # 3. NORMAL CHAT (LLAMA)
        else:
            try:
                chat_res = groq_client.chat.completions.create(
                    messages=[{"role": "system", "content": "You are Zenith AI, a smart assistant created by Shaikh Raja."}] + st.session_state.messages,
                    model="llama-3.3-70b-versatile",
                )
                msg = chat_res.choices[0].message.content
                st.markdown(msg)
            except Exception as e:
                st.error("Groq Key Error! Check Secrets.")
                msg = "Chatting mein error aa rahi hai."
        
        st.session_state.messages.append({"role": "assistant", "content": msg})
