import hashlib

import pandas as pd
import streamlit as st
from dotenv import load_dotenv

from app import extract_and_process_pdfs
from htmlTemplates import user_template, bot_template
from auth import AuthHandler

# Constants
CSV_FILE_PATH = 'user_data.csv'
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
LOGIN_SUCCESS = True
LOGIN_FAILURE = False




def display_login_page(auth_handler):
    with st.sidebar:
        st.title("Authentication")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if auth_handler.authenticate(username, password):
                st.session_state['authenticated'] = LOGIN_SUCCESS
                st.success("Login successful!")
            else:
                st.error("Invalid username or password")

        if st.button("Register"):
            if auth_handler.register(username, password):
                st.success("Registration successful! You can now log in.")
            else:
                st.error("Username already exists. Please choose a different one.")


def main_app():
    load_dotenv()
    st.markdown("""<style>.main-section {background-color: #f5f5f5; padding: 20px; border-radius: 10px;}</style>""",
                unsafe_allow_html=True)
    st.title("My Streamlit App")

    if not st.session_state.get('authenticated', LOGIN_FAILURE):
        display_login_page(AuthHandler(CSV_FILE_PATH))
    else:
        if 'conversation' not in st.session_state:
            st.session_state.conversation = None
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []

        extract_and_process_pdfs()
        user_question = st.text_input("Ask a question about your documents:")
        if user_question:
            handle_user_input(user_question)


def handle_user_input(user_question):
    if st.session_state.conversation:
        response = st.session_state.conversation({'question': user_question})
        st.session_state.chat_history.extend(response['chat_history'])

        for i, message in enumerate(st.session_state.chat_history):
            template = user_template if i % 2 == 0 else bot_template
            st.markdown(template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
    else:
        st.error("Conversation model not initialized. Please upload PDFs and process them.")


if __name__ == "__main__":
    main_app()
