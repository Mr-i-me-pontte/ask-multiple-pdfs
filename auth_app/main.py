import streamlit as st
from PyPDF2 import PdfReader
from dotenv import load_dotenv
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS

from htmlTemplates import css, bot_template, user_template

# Constants for chunking
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200


class Ui:
    def __init__(self):
        self.initialize_session_state()
        self.setup_page_config()

    def initialize_session_state(self):
        if "conversation" not in st.session_state:
            st.session_state.conversation = None
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

    def setup_page_config(self):
        load_dotenv()
        st.set_page_config(page_title="Chat with multiple PDFs", page_icon=":books:")
        st.markdown(css, unsafe_allow_html=True)
        st.markdown(
            '<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.0/dist/css/bootstrap.min.css" rel="stylesheet">',
            unsafe_allow_html=True)

    def render_header(self):
        st.header("Chat with multiple PDFs :books:")

    def get_user_input(self):
        return st.text_input("Ask a question about your documents:")

    def render_sidebar(self, process_function):
        with st.sidebar:
            pdf_docs = st.file_uploader("Upload your PDFs here and click on 'Process'", accept_multiple_files=True)
            if st.button("Process") and pdf_docs:
                process_function(pdf_docs)

    def display_chat_history(self):
        for i, message in enumerate(st.session_state.chat_history):
            template = user_template if i % 2 == 0 else bot_template
            st.markdown(template.replace("{{MSG}}", message.content), unsafe_allow_html=True)

    def show_message(self, message, message_type="info"):
        if message_type == "success":
            st.success(message)
        elif message_type == "error":
            st.error(message)
        elif message_type == "warning":
            st.warning(message)
        else:
            st.info(message)


def extract_text_from_pdfs(pdf_docs, ui):
    text = ""
    for pdf in pdf_docs:
        try:
            pdf_reader = PdfReader(pdf)
            text += ''.join(page.extract_text() or '' for page in pdf_reader.pages)
        except Exception as e:
            ui.show_message(f"Failed to read PDF document: {e}", "warning")
            return ""
    return text


def split_text_into_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        length_function=len
    )
    return text_splitter.split_text(text)


def create_vector_store(text_chunks):
    embeddings = OpenAIEmbeddings()
    vector_store = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vector_store


def create_conversation_chain(vector_store):
    llm = ChatOpenAI()
    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
    return ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vector_store.as_retriever(),
        memory=memory
    )


def handle_user_input(user_question, ui):
    if st.session_state.conversation:
        response = st.session_state.conversation({'question': user_question})
        st.session_state.chat_history.extend(response['chat_history'])
        ui.display_chat_history()
    else:
        ui.show_message("Conversation model not initialized. Please upload PDFs and process them.", "error")


def process_pdf_documents(pdf_docs, ui):
    with st.spinner("Processing"):
        raw_text = extract_text_from_pdfs(pdf_docs, ui)
        if raw_text:
            text_chunks = split_text_into_chunks(raw_text)
            vector_store = create_vector_store(text_chunks)
            st.session_state.conversation = create_conversation_chain(vector_store)
            ui.show_message("PDFs processed successfully.", "success")
        else:
            ui.show_message("Failed to process PDFs.", "error")


def main():
    ui = Ui()
    ui.render_header()
    user_question = ui.get_user_input()

    if user_question:
        handle_user_input(user_question, ui)

    ui.render_sidebar(lambda pdf_docs: process_pdf_documents(pdf_docs, ui))


if __name__ == '__main__':
    main()
