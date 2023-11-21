from PyPDF2 import PdfReader
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS

# Constants for chunking
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200


class PDFChatProcessor:
    """
    A class to process PDF files and enable chat-based interactions with their contents.
    """

    def __init__(self, pdf_paths):
        self.pdf_paths = pdf_paths

    def extract_text_from_pdfs(self):
        """Extracts and concatenates text from multiple PDF files."""
        text = ""
        for pdf in self.pdf_paths:
            try:
                pdf_reader = PdfReader(pdf)
                text += ''.join([page.extract_text() or '' for page in pdf_reader.pages])
            except Exception as e:
                print(f"Error reading {pdf}: {e}")
        return text

    def process_pdf_and_question(self, user_question):
        """Processes PDFs and responds to a user question based on their contents."""
        try:
            raw_text = self.extract_text_from_pdfs()
            text_chunks = self._split_text_into_chunks(raw_text)
            vector_store = self._create_vector_store(text_chunks)
            conversation_chain = self._create_conversation_chain(vector_store)

            response = conversation_chain({'question': user_question})
            return response['chat_history']
        except Exception as e:
            print(f"An error occurred: {e}")
            return []

    def _split_text_into_chunks(self, text):
        text_splitter = CharacterTextSplitter(
            separator="\n", chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP, length_function=len)
        return text_splitter.split_text(text)

    def _create_vector_store(self, text_chunks):
        embeddings = OpenAIEmbeddings()
        return FAISS.from_texts(texts=text_chunks, embedding=embeddings)

    def _create_conversation_chain(self, vector_store):
        llm = ChatOpenAI()
        memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
        return ConversationalRetrievalChain.from_llm(
            llm=llm, retriever=vector_store.as_retriever(), memory=memory)
