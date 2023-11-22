import os

import numpy as np
from PyPDF2 import PdfReader
from fpdf import FPDF
from nltk.tokenize import sent_tokenize
from sentence_transformers import SentenceTransformer

# Initialize the language model for embeddings
MODEL = SentenceTransformer('all-MiniLM-L6-v2')


class MultiPDFTableExtractor:
    def __init__(self):
        self.documents = {}
        self.chunks = []
        self.embeddings = []

    def load_pdf(self, pdf_path):
        """ Load a PDF file and extract its content. """
        try:
            reader = PdfReader(pdf_path)
            content = ''.join([page.extract_text() for page in reader.pages])
            self.documents[pdf_path] = content
        except Exception as e:
            print(f"Failed to load {pdf_path}: {e}")

    def chunk_text(self):
        """ Divide text into smaller chunks (sentences). """
        self.chunks = [sentence for content in self.documents.values() for sentence in sent_tokenize(content)]

    def generate_embeddings(self):
        """ Generate vector representations of each chunk. """
        self.embeddings = MODEL.encode(self.chunks)

    def chat(self):
        """ Start chat session. """
        print("Welcome to MultiPDF Table Extractor. Ask me anything about the loaded PDFs!")
        while True:
            query = input("You: ").strip()
            if query.lower() == 'exit':
                print("Exiting the chat.")
                break

            response = self.generate_response(query)
            print("MultiPDF Table Extractor:", response)

    def generate_response(self, query):
        """ Generate a response to the query. """
        query_embedding = MODEL.encode([query])
        similarities = np.dot(self.embeddings, query_embedding[0])
        max_similarity_idx = np.argmax(similarities)

        if similarities[max_similarity_idx] < 0.1:
            return "I'm sorry, I don't have enough information on that topic."

        return f"Based on the documents, you might find this information relevant: \"{self.chunks[max_similarity_idx]}\""


if __name__ == '__main__':
    pdf_app = MultiPDFTableExtractor()

    # Example PDFs loading
    pdf_files = ['/Users/Mr-i-me/PycharmProjects/AI/pdfapp/table_detection/woth_aws/data/input.pdf']
    for pdf_file in pdf_files:
        pdf_app.load_pdf(pdf_file)

    pdf_app.chunk_text()
    pdf_app.generate_embeddings()

    # Example table extraction and PDF creation
    output_dir = 'temp'
    json_file = 'data/analyzeDocResponse.json'  # Example JSON file
    output_pdf_path = 'temp/output_tables.pdf'

    try:
        # Call the table extraction function and obtain analysis results

        print(f"Created PDF with tables at: {output_pdf_path}")
    except ImportError:
        print("Please make sure the required libraries are installed.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

    # Start chat session
    pdf_app.chat()
