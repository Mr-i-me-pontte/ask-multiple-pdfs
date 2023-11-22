# chat_handler.py
import streamlit as st

from htmlTemplates import user_template, bot_template


# %% ChatHandler:
class ChatHandler:
    def __init__(self):
        # Initialize session state variables if they don't exist
        if "conversation" not in st.session_state:
            st.session_state.conversation = None
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

    def run_chat_interface(self):
        user_question = st.text_input("Ask a question about your documents:")

        if user_question:
            self.handle_user_input(user_question)

        with st.sidebar:
            st.subheader("Your documents")
            pdf_docs = st.file_uploader("Upload your PDFs here and click on 'Process'", accept_multiple_files=True)

            if st.button("Process") and pdf_docs:
                with st.spinner("Processing"):
                    try:
                        # Processing logic here
                        st.success("PDFs processed successfully.")
                    except Exception as e:
                        st.error(f"An error occurred: {str(e)}")

    def handle_user_input(self, user_question):
        if st.session_state.conversation:
            response = st.session_state.conversation({'question': user_question})
            st.session_state.chat_history.extend(response['chat_history'])

            for i, message in enumerate(st.session_state.chat_history):
                if i % 2 == 0:
                    st.write(user_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
                else:
                    st.write(bot_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.error("Conversation model not initialized. Please upload PDFs and process them.")
