
import streamlit as st
from groq import Groq

# Simple Page Setup
st.set_page_config(page_title="Zenith AI")

st.title("💠 Zenith AI")
st.write("Created by Shaikh Raja")

# API Connection
client = Groq(api_key="Gsk_yVPzT6aZ1PwYu62nMRqbWGdyb3FYkSiOurOKCcJspnlq0r2ZQwWE")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Puchiye..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "Tumhara naam Zenith AI hai. Shaikh Raja ne tumhe banaya hai."},
                *st.session_state.messages
            ],
            model="llama-3.1-70b-versatile",
        )
        msg = response.choices[0].message.content
        st.markdown(msg)
        st.session_state.messages.append({"role": "assistant", "content": msg})
