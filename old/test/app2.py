import PyPDF2
from PyPDF2 import PdfReader
import nltk
from nltk.tokenize import sent_tokenize
from sentence_transformers import SentenceTransformer
import numpy as np

# Initialize the language model for embeddings
MODEL = SentenceTransformer('all-MiniLM-L6-v2')

class MultiPDFChatApp:
    def __init__(self):
        self.documents = {}
        self.chunks = []
        self.embeddings = []

    def load_pdf(self, filename):
        """ Load a PDF file and extract its content. """
        try:
            with open(filename, 'rb') as file:
                reader = PdfReader(file)
                content = ''.join([page.extract_text() for page in reader.pages])
                self.documents[filename] = content
        except Exception as e:
            print(f"Failed to load {filename}: {e}")

    def chunk_text(self):
        """ Divide text into smaller chunks (sentences). """
        self.chunks = [sentence for content in self.documents.values() for sentence in sent_tokenize(content)]

    def generate_embeddings(self):
        """ Generate vector representations of each chunk. """
        self.embeddings = MODEL.encode(self.chunks)

    def chat(self):
        """ Start chat session. """
        print("Welcome to MultiPDF Chat App. Ask me anything about the loaded PDFs!")
        while True:
            query = input("You: ").strip()
            if query.lower() == 'exit':
                print("Exiting the chat.")
                break

            response = self.generate_response(query)
            print("MultiPDF Chat App:", response)

    def generate_response(self, query):
        """ Generate a response to the query. """
        query_embedding = MODEL.encode([query])
        similarities = np.dot(self.embeddings, query_embedding[0])
        max_similarity_idx = np.argmax(similarities)

        if similarities[max_similarity_idx] < 0.1:
            return "I'm sorry, I don't have enough information on that topic."

        return f"Based on the documents, you might find this information relevant: \"{self.chunks[max_similarity_idx]}\""

if __name__ == "__main__":
    chat_app = MultiPDFChatApp()

    # Example PDFs loading
    pdf_files = ['//Users/Mr-i-me/code/Mr-i-me-pontte/ai/ask-multiple-pdfs/input_onepage.pdf']
    for pdf_file in pdf_files:
        chat_app.load_pdf(pdf_file)

    chat_app.chunk_text()
    chat_app.generate_embeddings()
    chat_app.chat()
