import streamlit as st
from groq import Groq

# Page configuration
st.set_page_config(page_title="Zenith AI", page_icon="💠", layout="centered")

# Custom CSS for styling
st.markdown("""
    <style>
    .stChatMessage { background-color: #f0f2f6; border-radius: 10px; padding: 10px; margin-bottom: 10px; }
    .stChatInput { border-radius: 20px; }
    </style>
    """, unsafe_allow_html=True)

# Sidebar Design
with st.sidebar:
    st.title("💠 Zenith AI")
    st.markdown("---")
    st.write("### Creator Details")
    st.info("👤 **Shaikh Raja**\n\nLead Developer of Zenith AI")
    st.markdown("---")
    st.write("Current Model: `Llama-3.3-70b`")

st.title("💠 Zenith AI")
st.caption("The Peak of Intelligence | Created by Shaikh Raja")

# API Key from Secrets
if "GROQ_API_KEY" in st.secrets:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
else:
    st.error("Secrets mein API Key nahi mili!")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Zenith se kuch bhi puchiye..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            response = client.chat.completions.create(
                messages=[{"role": "system", "content": "You are Zenith AI, a helpful assistant created by Shaikh Raja."}, *st.session_state.messages],
                model="llama-3.3-70b-versatile",
            )
            msg = response.choices[0].message.content
            st.markdown(msg)
            st.session_state.messages.append({"role": "assistant", "content": msg})
        except Exception as e:
            st.error(f"Error: {e}")


