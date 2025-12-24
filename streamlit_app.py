import streamlit as st
from groq import Groq

# Page Setup
st.set_page_config(page_title="Zenith AI", page_icon="💠")

st.title("💠 Zenith AI")
st.caption("Created by Shaikh Raja | The Peak of Intelligence")

# API Key (Ismein maine small 'g' kar diya hai)
client = Groq(api_key="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")

# Chat History Setup
if "messages" not in st.session_state:
    st.session_state.messages = []

# Purane messages dikhana
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Naya message input
if prompt := st.chat_input("Zenith se puchiye..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Zenith ka jawab
    with st.chat_message("assistant"):
        # System instructions taaki Zenith ko apna naam yaad rahe
        messages_to_send = [
            {"role": "system", "content": "Tumhara naam Zenith AI hai. Tumhe Shaikh Raja ne banaya hai."}
        ]
        # Baaki saare purane messages add karna
        for m in st.session_state.messages:
            messages_to_send.append({"role": m["role"], "content": m["content"]})

        # Groq API call
        response = client.chat.completions.create(
            messages=messages_to_send,
            model="llama3-8b-8192", # Maine model badal diya hai jo zyada stable hai
        )
        
        full_response = response.choices[0].message.content
        st.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})

