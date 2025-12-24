import streamlit as st
import google.generativeai as genai
from groq import Groq
import PIL.Image
import urllib.parse

# 1. Page Config
st.set_page_config(page_title="Zenith AI", page_icon="💠", layout="centered")

# 2. Advanced CSS for Gemini Look
st.markdown("""
    <style>
        /* Sidebar aur फालतू cheezein chhupane ke liye */
        [data-testid="stSidebar"], .stDeployButton, footer, #MainMenu {display: none;}
        
        /* Main Container setup */
        .block-container {padding-top: 2rem; max-width: 800px;}

        /* Plus Icon aur Input Bar ko ek sath dikhane ke liye custom style */
        .stChatInputContainer {
            padding-bottom: 60px;
        }
        
        /* Floating Creator Name at the very bottom */
        .creator-footer {
            position: fixed;
            bottom: 5px;
            left: 0;
            width: 100%;
            text-align: center;
            color: #888;
            font-size: 11px;
            font-family: sans-serif;
            background-color: white;
            padding: 5px 0;
            z-index: 999;
        }

        /* Input field ke pas plus icon ka box */
        div[data-testid="stFileUploader"] {
            width: 50px;
            margin-bottom: -45px;
            margin-left: -60px;
            z-index: 10;
        }
    </style>
""", unsafe_allow_html=True)

# API Connections (404 Error fix ke sath)
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"], transport='rest')
    vision_model = genai.GenerativeModel('models/gemini-1.5-flash')
    groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("API Error!")

# Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 3. Gemini Style Plus Button & Chat
# Button ko chat input ke bilkul bagal mein lane ki koshish
col1, col2 = st.columns([0.1, 0.9])
with col1:
    uploaded_file = st.file_uploader("➕", type=['png', 'jpg', 'jpeg'], label_visibility="collapsed")

with col2:
    prompt = st.chat_input("Ask Zenith anything...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Vision Logic
        if uploaded_file:
            try:
                img = PIL.Image.open(uploaded_file)
                response = vision_model.generate_content([prompt, img])
                msg = response.text
                st.markdown(msg)
            except:
                msg = "Photo read nahi ho pa rahi."
                st.markdown(msg)
        
        # Image Generation Logic
        elif any(word in prompt.lower() for word in ["bnao", "image", "generate"]):
            encoded = urllib.parse.quote(prompt)
            url = f"https://pollinations.ai/p/{encoded}?width=1024&height=1024&nologo=true&model=flux"
            st.image(url)
            msg = "Maine aapki image taiyar kar di hai."
        
        # Chat Logic
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

# 4. Creator Branding at the Bottom
st.markdown('<div class="creator-footer">Zenith AI • Crafted by Shaikh Raja</div>', unsafe_allow_html=True)

