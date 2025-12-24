import streamlit as st
from groq import Groq

st.set_page_config(page_title="Zenith AI", page_icon="💠")
st.title("💠 Zenith AI")
st.caption("Created by Shaikh Raja")

# Ye line Streamlit ke "Secrets" se key uthayegi
if "GROQ_API_KEY" in st.secrets:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
else:
    st.error("Opps! Streamlit Secrets mein API Key nahi mili.")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Zenith se puchiye..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            response = client.chat.completions.create(
                messages=[{"role": "system", "content": "You are Zenith AI, built by Shaikh Raja."}, *st.session_state.messages],
                model="llama-3.3-70b-versatile",
            )
            msg = response.choices[0].message.content
            st.markdown(msg)
            st.session_state.messages.append({"role": "assistant", "content": msg})
        except Exception as e:
            st.error(f"Dikkat hui: {e}")

