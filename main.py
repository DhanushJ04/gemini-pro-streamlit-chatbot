import os
import time
import streamlit as st
from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()

# Configure Streamlit page
st.set_page_config(
    page_title="Chat with Gemini!",
    page_icon=":brain:",
    layout="centered",
)

# Get API Key
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]

# Create Gemini client (NEW WAY)
client = genai.Client(api_key=GOOGLE_API_KEY)

# Page title
st.title("🤖 Gemini ChatBot")

# Initialize chat history manually
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display chat history
for role, message in st.session_state.chat_history:
    with st.chat_message(role):
        st.markdown(message)

# User input
user_prompt = st.chat_input("Ask Gemini...")

if user_prompt:
    # Show user message
    st.chat_message("user").markdown(user_prompt)
    st.session_state.chat_history.append(("user", user_prompt))

    # Assistant response
    with st.chat_message("assistant"):
        with st.spinner("Gemini is thinking..."):

            response = None

            # Retry logic
            for attempt in range(2):
                try:
                    response = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=user_prompt,
                    )
                    break
                except Exception:
                    time.sleep(2)

            if response:
                reply = response.text
                st.markdown(reply)
                st.session_state.chat_history.append(("assistant", reply))
            else:
                st.error("⚠️ Gemini is currently unavailable. Please try again later.")
