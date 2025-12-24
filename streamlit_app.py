import streamlit as st
from groq import Groq
import PIL.Image
import base64
import io

# Page Config
st.set_page_config(page_title="Zenith AI Pro", page_icon="💠", layout="wide")

# API Setup
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception as e:
    st.error("Groq Key missing in Secrets!")

# Sidebar
with st.sidebar:
    st.title("💠 Zenith AI Pro")
    st.info("Creator: Shaikh Raja")
    uploaded_file = st.file_uploader("Photo upload karein...", type=['png', 'jpg', 'jpeg'])

# Image processing function
def encode_image(image_file):
    return base64.b64encode(image_file.read()).decode('utf-8')

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Baat karein ya photo ke baare mein puchein..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            if uploaded_file:
                # VISION MODEL (Llama-3.2-11b-Vision)
                base64_image = encode_image(uploaded_file)
                response = client.chat.completions.create(
                    model="llama-3.2-11b-vision-preview",
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": prompt},
                                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                            ]
                        }
                    ]
                )
                msg = response.choices[0].message.content
            else:
                # NORMAL CHAT MODEL
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "system", "content": "You are Zenith AI Pro, created by Shaikh Raja."}] + st.session_state.messages
                )
                msg = response.choices[0].message.content
            
            st.markdown(msg)
            st.session_state.messages.append({"role": "assistant", "content": msg})
        except Exception as e:
            st.error(f"Error: {e}")

