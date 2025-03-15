import streamlit as st
# Streamlit chat UI to interact with Yuna
import subprocess
from yuna_personality_behavioral_system import YunaPersonalityBehavioralStructuring  # New import

# Set up Streamlit UI
st.set_page_config(page_title="Yuna Chat", page_icon="🤖", layout="wide")

st.title("Chat with Yuna")
st.write("💬 Type your message below and start chatting with Yuna!")

# Store chat history in session state
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display chat history
for message in st.session_state["messages"]:
    role, text = message
    st.chat_message(role).write(text)

# User input
user_input = st.chat_input("Type your message here...")

if user_input:
    # Display user message
    st.chat_message("user").write(user_input)
    
    # Send the message to Yuna via Ollama
    response = subprocess.run(["ollama", "run", "yuna", user_input], capture_output=True, text=True)
    ai_response = response.stdout.strip()
    
    # Display Yuna's response
    st.chat_message("assistant").write(ai_response)

    # Save to session state (chat history)
    st.session_state["messages"].append(("user", user_input))
    st.session_state["messages"].append(("assistant", ai_response))
