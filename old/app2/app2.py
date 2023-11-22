import os

from nltk import sent_tokenize
from pdf2image import convert_from_path
from fpdf import FPDF
import torch
from transformers import BertTokenizer, BertForQuestionAnswering
import pytesseract
from PIL import Image

class MultiPDFTableExtractor:
    def __init__(self):
        self.documents = {}
        self.chunks = []
        self.embeddings = []
        self.table_images = []
        self.table_texts = []

    def load_pdf(self, pdf_path):
        """ Load a PDF file and extract its content. """
        try:
            images = convert_from_path(pdf_path)
            self.documents[pdf_path] = []
            for i, image in enumerate(images):
                image_path = f'{pdf_path}_page_{i + 1}.png'
                image.save(image_path, 'PNG')
                self.documents[pdf_path].append(image_path)
        except Exception as e:
            print(f"Failed to load {pdf_path}: {e}")

    def chunk_text(self):
        """ Divide text into smaller chunks (sentences). """
        for pdf_images in self.documents.values():
            for image_path in pdf_images:
                text = pytesseract.image_to_string(Image.open(image_path))
                self.chunks.extend(sent_tokenize(text))

    def extract_tables(self, min_table_width=1000, min_table_height=100):
        for pdf_images in self.documents.values():
            for image_path in pdf_images:
                image = Image.open(image_path)
                width, height = image.size
                if width >= min_table_width and height >= min_table_height:
                    self.table_images.append(image_path)
                    text = pytesseract.image_to_string(image)
                    self.table_texts.append(text)

    def create_pdf_from_images(self, output_pdf_path):
        pdf = FPDF()
        for image_path in self.table_images:
            pdf.add_page()
            pdf.image(image_path, x=10, y=8, w=190)
        pdf.output(output_pdf_path, "F")

    def initialize_question_answering(self):
        model_name = "bert-large-uncased-whole-word-masking-finetuned-squad"
        self.tokenizer = BertTokenizer.from_pretrained(model_name)
        self.model = BertForQuestionAnswering.from_pretrained(model_name)

    def answer_question(self, question):
        inputs = self.tokenizer(self.table_texts, question, return_tensors="pt", padding=True, truncation=True)
        start_positions, end_positions = self.model(**inputs)
        start_index = torch.argmax(start_positions)
        end_index = torch.argmax(end_positions)
        answer = self.table_texts[start_index:end_index+1]
        return answer

    def chat(self):
        """ Start chat session. """
        print("Welcome to MultiPDF Table Extractor. Ask me anything about the loaded PDFs!")
        while True:
            question = input("You: ").strip()
            if question.lower() == 'exit':
                print("Exiting the chat.")
                break

            answer = self.answer_question(question)
            print("MultiPDF Table Extractor:", answer)

if __name__ == '__main__':
    pdf_app = MultiPDFTableExtractor()

    # Example PDFs loading
    pdf_files = ['/Users/Mr-i-me/code/Mr-i-me-pontte/ai/ask-multiple-pdfs/input.pdf']
    for pdf_file in pdf_files:
        pdf_app.load_pdf(pdf_file)

    pdf_app.chunk_text()
    pdf_app.extract_tables()

    # Create PDF from the extracted tables
    output_pdf_path = 'output_tables.pdf'
    pdf_app.create_pdf_from_images(output_pdf_path)

    # Initialize question-answering model
    pdf_app.initialize_question_answering()

    # Start chat session
    pdf_app.chat()
