import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai.errors import ClientError
import os

# Load environment variables
load_dotenv()



# Gemini Client
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

st.header(" AI Chatbot")

# Load CSS styling
with open("style.css", "r") as css_file:
    st.markdown(f"<style>{css_file.read()}</style>", unsafe_allow_html=True)

# Memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

personality = st.sidebar.selectbox(
    "Choose Personality",
    [
        "Helpful Assistant",
        "Code Reviewer",
        "Study Tutor",
        "Sarcastic Friend"
    ]
)

system_prompts = {
    "Helpful Assistant":
        "You are a helpful assistant.",

    "Code Reviewer":
        "You are an expert Python code reviewer.",

    "Study Tutor":
        "You are a patient study tutor.",

    "Sarcastic Friend":
        "You are a funny sarcastic friend."
}
if st.sidebar.button("Clear Conversation"):
    st.session_state.messages = []
    st.rerun()

# User input
user_input = st.chat_input("Ask anything...")

if user_input:

    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    # Build conversation history
    conversation = ""

    for msg in st.session_state.messages:
        conversation += f"{msg['role']}: {msg['content']}\n"

    # Gemini Response
    try:
        response = client.models.generate_content_stream(
            model="gemini-2.5-flash",
            contents=conversation
        )

        full_response = ""

        with st.chat_message("assistant"):
            placeholder = st.empty()

            for chunk in response:
                full_response += chunk.text
                placeholder.markdown(full_response + "▌")

            placeholder.markdown(full_response)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": full_response
            }
        )
    except ClientError as e:
        st.error(f"Error: {e.message}")
    