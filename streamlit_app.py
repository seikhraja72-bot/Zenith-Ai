import streamlit as st
from groq import Groq

st.set_page_config(page_title="Zenith AI", page_icon="💠")
st.title("💠 Zenith AI")
st.caption("Created by Shaikh Raja")

# Hum key ko "Secrets" se uthayenge
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("Please add the API Key in Streamlit Secrets!")
    st.stop()

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
            messages=[{"role": "system", "content": "You are Zenith AI, built by Shaikh Raja."}, *st.session_state.messages],
            model="llama3-8b-8192",
        )
        msg = response.choices[0].message.content
        st.markdown(msg)
        st.session_state.messages.append({"role": "assistant", "content": msg})

