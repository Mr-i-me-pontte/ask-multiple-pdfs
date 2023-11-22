# pdf_processor.py

from PyPDF2 import PdfReader
import streamlit as st
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS

# Constants for chunking
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

from htmlTemplates import user_template, bot_template


class PDFProcessor:
    def __init__(self):
        self.conversation_chain = None

    def initialize_conversation_chain(self):
        if not self.conversation_chain:
            embeddings = OpenAIEmbeddings()
            vector_store = FAISS.from_texts(texts=[], embedding=embeddings)

            llm = ChatOpenAI()
            memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)

            self.conversation_chain = ConversationalRetrievalChain.from_llm(
                llm=llm,
                retriever=vector_store.as_retriever(),
                memory=memory
            )

    def process_user_input(self, user_question):
        if not self.conversation_chain:
            st.error("Conversation model not initialized. Please upload PDFs and process them.")
            return

        response = self.conversation_chain({'question': user_question})
        st.session_state.chat_history.extend(response['chat_history'])

        for i, message in enumerate(st.session_state.chat_history):
            template = user_template if i % 2 == 0 else bot_template
            st.write(template.replace("{{MSG}}", message.content), unsafe_allow_html=True)


def extract_text_from_pdfs(pdf_docs):
    """Extracts and concatenates text from PDF documents."""
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text() or ''
    return text


def split_text_into_chunks(text):
    """Splits text into chunks for processing."""
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks
