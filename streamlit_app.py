import streamlit as st
import google.generativeai as genai
from groq import Groq
import PIL.Image
import urllib.parse
import base64

# 1. Page Config
st.set_page_config(page_title="Zenith AI", page_icon="💠", layout="centered")

# 2. Gemini Style UI Injection (Plus icon and Bottom Credit)
st.markdown("""
    <style>
        [data-testid="stSidebar"] {display: none;}
        .stDeployButton {display:none;}
        footer {visibility: hidden;}
        #MainMenu {visibility: hidden;}
        
        /* Main Container */
        .block-container {padding-top: 2rem; max-width: 800px;}
        
        /* Bottom Creator Name */
        .footer-text {
            position: fixed;
            bottom: 10px;
            left: 0;
            width: 100%;
            text-align: center;
            color: #5f6368;
            font-size: 12px;
            z-index: 100;
        }

        /* Styling for the Plus/Upload area */
        .upload-box {
            border: 1px solid #ddd;
            border-radius: 20px;
            padding: 10px;
            margin-bottom: 10px;
            background: #f8f9fa;
        }
    </style>
    <div class="footer-text">Zenith AI | Created by Shaikh Raja</div>
""", unsafe_allow_html=True)

# API Connections
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"], transport='rest')
    vision_model = genai.GenerativeModel('models/gemini-1.5-flash')
    groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception as e:
    st.error("API Key missing!")

# Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 3. Dynamic Plus Icon & Input Area
st.markdown("<div class='upload-box'><b>➕ Options:</b> Photo upload karke puchiye</div>", unsafe_allow_html=True)
uploaded_file = st.file_uploader("", type=['png', 'jpg', 'jpeg'], label_visibility="collapsed")

if prompt := st.chat_input("Zenith se puchiye..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Image Processing
        if uploaded_file:
            try:
                img = PIL.Image.open(uploaded_file)
                response = vision_model.generate_content([prompt, img])
                msg = response.text
                st.markdown(msg)
            except:
                msg = "Photo read karne mein error aayi."
                st.markdown(msg)
        
        # Image Generation
        elif any(word in prompt.lower() for word in ["bnao", "image", "photo", "generate"]):
            encoded = urllib.parse.quote(prompt)
            url = f"https://pollinations.ai/p/{encoded}?width=1024&height=1024&nologo=true&model=flux"
            st.image(url)
            msg = "Aapki image taiyar hai."
        
        # Chat
        else:
            try:
                chat_res = groq_client.chat.completions.create(
                    messages=[{"role": "system", "content": "You are Zenith AI, created by Shaikh Raja."}] + st.session_state.messages,
                    model="llama-3.3-70b-versatile",
                )
                msg = chat_res.choices[0].message.content
                st.markdown(msg)
            except:
                msg = "System busy hai."
                st.markdown(msg)
        
        st.session_state.messages.append({"role": "assistant", "content": msg})


