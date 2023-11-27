
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

class PDFProcessor:
    def extract_text_from_pdfs(self, pdf_docs):
        '''Extracts and concatenates text from PDF documents.'''
        text = ""
        for pdf in pdf_docs:
            pdf_reader = PdfReader(pdf)
            for page in pdf_reader.pages:
                text += page.extract_text() or ''
        return text

    def split_text_into_chunks(self, text):
        '''Splits text into chunks for processing.'''
        text_splitter = CharacterTextSplitter(
            separator="\n",
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
            length_function=len
        )
        chunks = text_splitter.split_text(text)
        return chunks

    def create_vector_store(self, text_chunks):
        '''Creates a vector store from text chunks.'''
        embeddings = OpenAIEmbeddings()
        vector_store = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
        return vector_store

class ChatHandler:
    def __init__(self):
        self.conversation_chain = None
        self.chat_history = []

    def initialize_conversation_chain(self, vector_store):
        '''Creates a conversational chain with memory and vector store.'''
        llm = ChatOpenAI()
        memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
        self.conversation_chain = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=vector_store.as_retriever(),
            memory=memory
        )

    def handle_user_input(self, user_input):
        if self.conversation_chain:
            response = self.conversation_chain({'question': user_input})
            self.chat_history.extend(response['chat_history'])
            self.display_chat_history()
        else:
            st.error("Conversation model not initialized. Please upload PDFs and process them.")

    def display_chat_history(self):
        for i, message in enumerate(self.chat_history):
            if i % 2 == 0:
                st.write(user_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
            else:
                st.write(bot_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)

def main():
    load_dotenv()
    st.set_page_config(page_title="Chat with multiple PDFs", page_icon=":books:")
    st.write(css, unsafe_allow_html=True)

    pdf_processor = PDFProcessor()
    chat_handler = ChatHandler()

    st.header("Chat with multiple PDFs :books:")
    user_question = st.text_input("Ask a question about your documents:")

    if user_question:
        chat_handler.handle_user_input(user_question)

    with st.sidebar:
        st.subheader("Your documents")
        pdf_docs = st.file_uploader("Upload your PDFs here and click on 'Process'", accept_multiple_files=True)

        if st.button("Process") and pdf_docs:
            with st.spinner("Processing"):
                try:
                    # Get PDF text
                    raw_text = pdf_processor.extract_text_from_pdfs(pdf_docs)

                    # Get text chunks
                    text_chunks = pdf_processor.split_text_into_chunks(raw_text)

                    # Create vector store
                    vector_store = pdf_processor.create_vector_store(text_chunks)

                    # Initialize conversation chain
                    chat_handler.initialize_conversation_chain(vector_store)

                    st.success("PDFs processed successfully.")
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")

if __name__ == '__main__':
    main()
