# main.py
import streamlit as st
from dotenv import load_dotenv
from auth import AuthHandler
from pdf_processor import PDFProcessor
from chat_handler import ChatHandler

# Initialize classes
auth_handler = AuthHandler()
pdf_processor = PDFProcessor()
chat_handler = ChatHandler()

def main():
    load_dotenv()
    st.set_page_config(page_title="Chat with multiple PDFs", page_icon=":books:")

    if "authenticated" not in st.session_state:
        st.session_state['authenticated'] = False

    if not st.session_state['authenticated']:
        auth_handler.show_auth_form()
    else:
        st.write(f"Logged in as: {st.session_state['username']}")
        run_app()
        if st.button("Logout"):
            st.session_state['authenticated'] = False
            st.session_state['username'] = None

def run_app():
    st.markdown("<link href='https://cdn.jsdelivr.net/npm/bootstrap@5.1.0/dist/css/bootstrap.min.css' rel='stylesheet'>", unsafe_allow_html=True)
    st.header("Chat with multiple PDFs :books:")
    chat_handler.run_chat_interface()

if __name__ == '__main__':
    main()
