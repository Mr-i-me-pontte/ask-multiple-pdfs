import streamlit as st
from dotenv import load_dotenv

from helpers import extract_text_from_pdfs, split_text_into_chunks, create_vector_store, create_conversation_chain
from htmlTemplates import css, bot_template, user_template
from auth_app.auth import AuthHandler

# Path to the CSV file storing user data
CSV_FILE_PATH = 'user_data.csv'

def run_app():
    load_dotenv()
    # st.set_page_config(page_title="Chat with multiple PDFs", page_icon=":books:")
    st.write(css, unsafe_allow_html=True)
    st.markdown("""
                <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.0/dist/css/bootstrap.min.css" rel="stylesheet">
            """, unsafe_allow_html=True)
    st.markdown('<button class="btn btn-primary">Click me!</button>', unsafe_allow_html=True)

    # Initialize session state variables
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    st.header("Chat with multiple PDFs :books:")
    user_question = st.text_input("Ask a question about your documents:")

    if user_question:
        handle_user_input(user_question)

    with st.sidebar:
        st.subheader("Your documents")
        pdf_docs = st.file_uploader(
            "Upload your PDFs here and click on 'Process'", accept_multiple_files=True)

        if st.button("Process") and pdf_docs:
            with st.spinner("Processing"):
                try:
                    # Get PDF text
                    raw_text = extract_text_from_pdfs(pdf_docs)

                    # Get text chunks
                    text_chunks = split_text_into_chunks(raw_text)

                    # Create vector store
                    vector_store = create_vector_store(text_chunks)

                    # Create conversation chain
                    st.session_state.conversation = create_conversation_chain(vector_store)

                    st.success("PDFs processed successfully.")
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")


def handle_user_input(user_question):
    if st.session_state.conversation:
        response = st.session_state.conversation({'question': user_question})
        st.session_state.chat_history.extend(response['chat_history'])

        for i, message in enumerate(st.session_state.chat_history):
            if i % 2 == 0:
                st.write(user_template.replace(
                    "{{MSG}}", message.content), unsafe_allow_html=True)
            else:
                st.write(bot_template.replace(
                    "{{MSG}}", message.content), unsafe_allow_html=True)
    else:
        st.error("Conversation model not initialized. Please upload PDFs and process them.")


def main():
    # Create an instance of AuthHandler
    auth_handler = AuthHandler()

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


# Streamlit app entry point
if __name__ == '__main__':
    main()
