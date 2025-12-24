import streamlit as st
import google.generativeai as genai
from groq import Groq
import PIL.Image
import urllib.parse

# Page configuration
st.set_page_config(page_title="Zenith AI", page_icon="💠", layout="wide")

# Sidebar setup
with st.sidebar:
    st.title("💠 Zenith AI")
    st.info("👤 **Shaikh Raja**\n\nLead Developer")
    st.success("✅ Llama + Gemini Active")
    uploaded_file = st.file_uploader("Photo upload kijiye...", type=['png', 'jpg', 'jpeg'])
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# API Connections with Fixes
try:
    # transport='rest' dalne se 404 error solve ho jayegi
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"], transport='rest')
    vision_model = genai.GenerativeModel('models/gemini-1.5-flash')
    groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception as e:
    st.error(f"API Key Error: {e}")

st.title("💠 Zenith AI")
st.caption("The Peak of Intelligence | Created by Shaikh Raja")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input Logic
if prompt := st.chat_input("Zenith se kuch bhi puchiye..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # 1. VISION FEATURE (GEMINI)
        if uploaded_file:
            try:
                img = PIL.Image.open(uploaded_file)
                st.image(img, caption="Aapki Photo", width=300)
                response = vision_model.generate_content([prompt, img])
                msg = response.text
                st.markdown(msg)
            except Exception as e:
                st.error(f"Vision Connection Error: {e}")
                msg = "Photo dekhne mein dikkat ho rahi hai, dobara koshish karein."
        
        # 2. IMAGE GENERATION (POLLINATIONS)
        elif any(word in prompt.lower() for word in ["bnao", "image", "photo", "generate"]):
            encoded = urllib.parse.quote(prompt)
            url = f"https://pollinations.ai/p/{encoded}?width=1024&height=1024&nologo=true"
            st.image(url, caption=f"Zenith Creation: {prompt}")
            msg = f"Maine '{prompt}' ki image bana di hai!"
            st.markdown(msg)

        # 3. CHAT LOGIC (GROQ/LLAMA)
        else:
            try:
                chat_res = groq_client.chat.completions.create(
                    messages=[{"role": "system", "content": "You are Zenith AI, created by Shaikh Raja."}] + st.session_state.messages,
                    model="llama-3.3-70b-versatile",
                )
                msg = chat_res.choices[0].message.content
                st.markdown(msg)
            except Exception as e:
                st.error("Groq key authentication failed!")
                msg = "Chat system abhi kaam nahi kar raha."
        
        st.session_state.messages.append({"role": "assistant", "content": msg})

