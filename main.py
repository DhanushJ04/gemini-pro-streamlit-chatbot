import os
import time
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai


# Load environment variables
load_dotenv()

# Configure Streamlit page settings
st.set_page_config(
    page_title="Chat with Gemini-Pro!",
    page_icon=":brain:",
    layout="centered",
)

# Get API Key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Configure Gemini
gen_ai.configure(api_key=GOOGLE_API_KEY)

model = gen_ai.GenerativeModel(
    model_name="gemini-2.5-flash",
    generation_config={
        "temperature": 0.5,
        "max_output_tokens": 256
    }
)

# Translate role names
def translate_role_for_streamlit(user_role):
    if user_role == "model":
        return "assistant"
    return user_role


# Initialize chat session
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])


# Page title
st.title("🤖 Gemini Pro - ChatBot")


# Display chat history
for message in st.session_state.chat_session.history:
    with st.chat_message(translate_role_for_streamlit(message.role)):
        st.markdown(message.parts[0].text)


# User input
user_prompt = st.chat_input("Ask Gemini-Pro...")

if user_prompt:
    # Show user message
    st.chat_message("user").markdown(user_prompt)

    # Assistant response area
    with st.chat_message("assistant"):
        with st.spinner("Gemini is thinking..."):

            response = None

            # 🔁 RETRY LOGIC (Step 3)
            for attempt in range(2):
                try:
                    response = st.session_state.chat_session.send_message(user_prompt)
                    break
                except Exception:
                    time.sleep(2)  # wait 2 seconds and retry

            # If successful
            if response:
                st.markdown(response.text)
            else:
                st.error("⚠️ Gemini is currently unavailable. Please try again later.")
