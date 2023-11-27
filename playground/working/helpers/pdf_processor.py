import io
import logging

from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PDFProcessor:
    def __init__(self, pdf_bytes):
        self.pdf_bytes = pdf_bytes

    def extract_text(self):
        try:
            pdf_buffer = io.BytesIO(self.pdf_bytes)
            pdf_reader = PdfReader(pdf_buffer)
            return ''.join([page.extract_text() or '' for page in pdf_reader.pages])
        except Exception as e:
            logger.error(f"Error reading PDF: {e}")
            raise

    def split_text_into_chunks(self, text):
        text_splitter = CharacterTextSplitter(separator="\n", chunk_size=1000, chunk_overlap=100, length_function=len)
        return text_splitter.split_text(text)


def process_pdf(pdf_bytes):
    try:

        pdf_processor = PDFProcessor(pdf_bytes)
        extracted_text = pdf_processor.extract_text()
        text_chunks = pdf_processor.split_text_into_chunks(extracted_text)
        return text_chunks
    except Exception as e:
        logger.error(f"PDF processing error: {e}")
        raise
