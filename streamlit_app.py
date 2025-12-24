import streamlit as st
from groq import Groq

# Page setup
st.set_page_config(page_title="Zenith AI", page_icon="💠")

st.title("💠 Zenith AI")
st.caption("Created by Shaikh Raja | The Peak of Intelligence")

# Yahan maine 'g' ko small kar diya hai
client = Groq(api_key="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")

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
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "Tumhara naam Zenith AI hai. Tumhe Shaikh Raja ne banaya hai. Tum bahut intelligent ho."},
                *st.session_state.messages
            ],
            model="llama-3.1-70b-versatile",
        )
        full_response = response.choices[0].message.content
        st.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})

