import streamlit as st
import google.generativeai as genai
from groq import Groq
import PIL.Image
import urllib.parse

# 1. Page Config
st.set_page_config(page_title="Zenith AI Pro", page_icon="💠")

# 2. Normal Sidebar (Pehle jaisa)
with st.sidebar:
    st.title("💠 Zenith AI Pro")
    st.write("Creator: Shaikh Raja")
    uploaded_file = st.file_uploader("Photo upload karein...", type=['png', 'jpg', 'jpeg'])
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# API Connections
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"], transport='rest')
    vision_model = genai.GenerativeModel('models/gemini-1.5-flash')
    groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("API Key check karein!")

st.title("💠 Zenith AI")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("Baat karein ya photo ke baare mein puchein..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Vision Logic
        if uploaded_file:
            try:
                img = PIL.Image.open(uploaded_file)
                st.image(img, width=300)
                response = vision_model.generate_content([prompt, img])
                msg = response.text
            except:
                msg = "Photo read karne mein dikkat hui."
        
        # Image Gen Logic
        elif any(word in prompt.lower() for word in ["bnao", "image", "photo"]):
            encoded = urllib.parse.quote(prompt)
            url = f"https://pollinations.ai/p/{encoded}?width=1024&height=1024&nologo=true"
            st.image(url)
            msg = "Aapki photo taiyar hai!"
        
        # Normal Chat
        else:
            try:
                chat_res = groq_client.chat.completions.create(
                    messages=[{"role": "system", "content": "You are Zenith AI, created by Shaikh Raja."}] + st.session_state.messages,
                    model="llama-3.3-70b-versatile",
                )
                msg = chat_res.choices[0].message.content
            except:
                msg = "System busy hai."

        st.markdown(msg)
        st.session_state.messages.append({"role": "assistant", "content": msg})

