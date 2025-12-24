import streamlit as st
from groq import Groq
import urllib.parse

st.set_page_config(page_title="Zenith AI", page_icon="💠")

with st.sidebar:
    st.title("💠 Zenith AI")
    st.info("👤 **Shaikh Raja** (Creator)")
    st.success("✅ Voice & Image Active")

st.title("💠 Zenith AI")

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Zenith se kuch banwaiye..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Image Logic
        if "bnao" in prompt.lower() or "image" in prompt.lower() or "photo" in prompt.lower():
            encoded = urllib.parse.quote(prompt)
            url = f"https://pollinations.ai/p/{encoded}?width=1024&height=1024&nologo=true"
            st.image(url, caption=f"Zenith ne banaya: {prompt}")
            st.session_state.messages.append({"role": "assistant", "content": f"Maine photo bana di hai!"})
        else:
            # Chat Logic
            response = client.chat.completions.create(
                messages=[{"role": "system", "content": "You are Zenith AI, created by Shaikh Raja. You can generate images if asked."}] + st.session_state.messages,
                model="llama-3.3-70b-versatile",
            )
            msg = response.choices[0].message.content
            st.markdown(msg)
            st.session_state.messages.append({"role": "assistant", "content": msg})

  
