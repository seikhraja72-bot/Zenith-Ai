import streamlit as st
import google.generativeai as genai
from groq import Groq
import PIL.Image
import urllib.parse

# 1. Page Config
st.set_page_config(page_title="Zenith AI", page_icon="💠", layout="centered")

# 2. Advanced CSS for Gemini Interface (Sidebar Hidden)
st.markdown("""
    <style>
        /* Hide default Streamlit elements */
        [data-testid="stSidebar"], .stDeployButton, footer, #MainMenu {display: none;}
        
        /* Main Container setup */
        .block-container {padding-top: 1rem; max-width: 750px;}

        /* Bottom Creator Branding (Fixed at bottom) */
        .footer {
            position: fixed;
            bottom: 5px;
            left: 0;
            width: 100%;
            text-align: center;
            color: #70757a;
            font-size: 11px;
            background-color: white;
            padding: 5px 0;
            z-index: 100;
            border-top: 1px solid #f1f3f4;
        }

        /* Styling for Upload Icon area */
        .upload-section {
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 5px;
        }
    </style>
""", unsafe_allow_html=True)

# API Connections
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"], transport='rest')
    vision_model = genai.GenerativeModel('models/gemini-1.5-flash')
    groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("API Key missing!")

# Branding at the Bottom
st.markdown('<div class="footer">Zenith AI • Crafted by Shaikh Raja</div>', unsafe_allow_html=True)

# Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 3. Plus Icon (File Uploader) and Input Bar
# Dono ko ek sath dikhane ke liye layout
with st.container():
    col1, col2 = st.columns([0.15, 0.85])
    with col1:
        # Isse Plus icon jaisa effect aayega
        uploaded_file = st.file_uploader("➕", type=['png', 'jpg', 'jpeg'], label_visibility="collapsed")
    with col2:
        prompt = st.chat_input("Zenith se puchiye...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Image Analysis Logic
        if uploaded_file:
            try:
                img = PIL.Image.open(uploaded_file)
                response = vision_model.generate_content([prompt, img])
                msg = response.text
                st.markdown(msg)
            except:
                msg = "Photo processing error!"
                st.markdown(msg)
        
        # Image Generation Logic
        elif any(word in prompt.lower() for word in ["bnao", "image", "photo", "generate"]):
            encoded = urllib.parse.quote(prompt)
            url = f"https://pollinations.ai/p/{encoded}?width=1024&height=1024&nologo=true&model=flux"
            st.image(url)
            msg = "Maine aapki image bana di hai."
        
        # General Chat Logic
        else:
            try:
                chat_res = groq_client.chat.completions.create(
                    messages=[{"role": "system", "content": "You are Zenith AI, created by Shaikh Raja."}] + st.session_state.messages,
                    model="llama-3.3-70b-versatile",
                )
                msg = chat_res.choices[0].message.content
                st.markdown(msg)
            except:
                msg = "System is busy."
                st.markdown(msg)
        
        st.session_state.messages.append({"role": "assistant", "content": msg})

