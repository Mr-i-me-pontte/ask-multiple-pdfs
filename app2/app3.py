import PyPDF2
from PyPDF2 import PdfReader
import nltk
from nltk.tokenize import sent_tokenize
from langchain.embeddings import HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain

class MultiPDFChatApp:
    def __init__(self):
        self.documents = {}
        self.chunks = []
        self.embeddings_model = HuggingFaceInstructEmbeddings()
        self.chain = self.initialize_chain()

    def initialize_chain(self):
        # Initialize the necessary components for FAISS vector store
        # These should be tailored to your specific needs and data
        index = ...  # Initialize or load your FAISS index here
        docstore = ...  # Initialize or load your document store here
        index_to_docstore_id = ...  # Initialize your mapping from index IDs to document IDs here

        vector_store = FAISS(self.embeddings_model, index, docstore, index_to_docstore_id)
        memory = ConversationBufferMemory()
        return ConversationalRetrievalChain(vector_store=vector_store, memory=memory)

    def load_pdf(self, filename):
        try:
            with open(filename, 'rb') as file:
                reader = PdfReader(file)
                self.documents[filename] = ''.join(page.extract_text() for page in reader.pages if page.extract_text())
        except Exception as e:
            print(f"Failed to load {filename}: {e}")

    def process_documents(self):
        self.chunks = [sentence for content in self.documents.values() for sentence in sent_tokenize(content)]
        for chunk in self.chunks:
            self.chain.vector_store.add(chunk)

    def chat(self):
        print("Welcome to MultiPDF Chat App. Ask me anything about the loaded PDFs!")
        while True:
            query = input("You: ").strip()
            if query.lower() == 'exit':
                print("Exiting the chat.")
                break
            response = self.chain.process_input(query)
            print("MultiPDF Chat App:", response or "I'm sorry, I don't have enough information on that topic.")

if __name__ == "__main__":
    nltk.download('punkt')  # Ensure NLTK data is available

    chat_app = MultiPDFChatApp()

    # Load multiple PDFs
    pdf_files = ['/path/to/your/pdf1.pdf', '/path/to/your/pdf2.pdf', ...]  # Add your PDF file paths here
    for pdf_file in pdf_files:
        chat_app.load_pdf(pdf_file)

    chat_app.process_documents()
    chat_app.chat()
