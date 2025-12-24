import streamlit as st
from groq import Groq

# Page Setup
st.set_page_config(page_title="Zenith AI", page_icon="💠", layout="wide")

# Styling for better look
st.markdown("""
    <style>
    .stChatMessage { border-radius: 15px; padding: 15px; }
    .stChatInput { border: 2px solid #007bff; }
    </style>
    """, unsafe_allow_html=True)

# Sidebar with Voice Feature info
with st.sidebar:
    st.title("💠 Zenith AI")
    st.info("👤 **Shaikh Raja** (Creator)")
    st.success("✅ **Features Active:** Chat History & Voice")
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

st.title("💠 Zenith AI")
st.caption("The Peak of Intelligence | Enhanced by Shaikh Raja")

# API Key Connection
if "GROQ_API_KEY" in st.secrets:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
else:
    st.error("Secrets missing!")
    st.stop()

# Memory (Chat History) Setup
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chats
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if prompt := st.chat_input("Zenith se baat kijiye..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # AI logic with full history
            response = client.chat.completions.create(
                messages=[{"role": "system", "content": "You are Zenith AI, a smart assistant created by Shaikh Raja. Always remember user context."}] + st.session_state.messages,
                model="llama-3.3-70b-versatile",
            )
            msg = response.choices[0].message.content
            st.markdown(msg)
            
            # Voice Button (Browser TTS)
            st.session_state.messages.append({"role": "assistant", "content": msg})
            
            # Simple JS for Voice
            st.components.v1.html(f"""
                <script>
                var msg = new SpeechSynthesisUtterance("{msg.replace('"', "'")}");
                window.speechSynthesis.speak(msg);
                </script>
            """, height=0)
            
        except Exception as e:
            st.error(f"Error: {e}")

