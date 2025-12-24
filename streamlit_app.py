import streamlit as st
import google.generativeai as genai
from groq import Groq
import PIL.Image
import urllib.parse

# 1. Page Configuration
st.set_page_config(page_title="Zenith AI", page_icon="💠", layout="centered")

# 2. Gemini-Style Ultra Clean UI (Sidebar Hidden)
st.markdown("""
    <style>
        [data-testid="stSidebar"] {display: none;}
        .stDeployButton {display:none;}
        footer {visibility: hidden;}
        #MainMenu {visibility: hidden;}
        .block-container {padding-top: 1rem; max-width: 700px;}
        .stChatInputContainer {padding-bottom: 50px;}
        .developer-footer {
            text-align: center; 
            color: #888; 
            font-size: 14px; 
            margin-top: 20px;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

# API Connections
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"], transport='rest')
    vision_model = genai.GenerativeModel('models/gemini-1.5-flash')
    groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception as e:
    st.error("Connection Error!")

# Home Screen Branding
st.markdown("<h1 style='text-align: center; color: #4285F4;'>💠 Zenith AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #5f6368;'>Hello! I'm your AI assistant.</p>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 3. Plus Icon Style - Photo Upload
# Isse plus icon jaisa effect milega
st.markdown("---")
uploaded_file = st.file_uploader("➕ Upload Photo to Discuss", type=['png', 'jpg', 'jpeg'])

# Main Chat Input
if prompt := st.chat_input("Ask Zenith anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Photo Processing (Gemini)
        if uploaded_file:
            try:
                img = PIL.Image.open(uploaded_file)
                response = vision_model.generate_content([prompt, img])
                msg = response.text
                st.markdown(msg)
            except:
                msg = "Photo dekhne mein dikkat hui."
                st.markdown(msg)
        
        # Image Generation (Nano Banana Power)
        elif any(word in prompt.lower() for word in ["bnao", "image", "generate", "photo"]):
            encoded = urllib.parse.quote(prompt)
            url = f"https://pollinations.ai/p/{encoded}?width=1024&height=1024&nologo=true&model=flux"
            st.image(url)
            msg = "Maine aapki image bana di hai."
        
        # Fast Chat (Llama)
        else:
            try:
                chat_res = groq_client.chat.completions.create(
                    messages=[{"role": "system", "content": "You are Zenith AI, a professional assistant created by Shaikh Raja."}] + st.session_state.messages,
                    model="llama-3.3-70b-versatile",
                )
                msg = chat_res.choices[0].message.content
                st.markdown(msg)
            except:
                msg = "System busy hai."
                st.markdown(msg)
        
        st.session_state.messages.append({"role": "assistant", "content": msg})

# 4. Developer Credit (Home Screen par dikhega)
st.markdown("<div class='developer-footer'>Crafted with ❤️ by Shaikh Raja</div>", unsafe_allow_html=True)


