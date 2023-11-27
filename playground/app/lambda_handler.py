import io
import json
import logging
import boto3
from PyPDF2 import PdfReader
from botocore.exceptions import BotoCoreError, ClientError
from dotenv import load_dotenv
from langchain import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain.text_splitter import CharacterTextSplitter

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize S3 client
s3_client = boto3.client('s3')


class S3Helper:
    def __init__(self, bucket_name):
        self.bucket_name = bucket_name
        self.s3_client = boto3.client('s3')

    def download_file(self, object_key):
        try:
            response = self.s3_client.get_object(Bucket=self.bucket_name, Key=object_key)
            return response['Body'].read()
        except (BotoCoreError, ClientError) as e:
            logger.error(f"Error downloading file: {e}")
            raise


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


class LangchainHandler:
    def __init__(self, text_chunks):
        self.text_chunks = text_chunks

    def create_vector_store(self):
        embeddings = OpenAIEmbeddings()
        return FAISS.from_texts(texts=self.text_chunks, embedding=embeddings)

    def create_conversation_chain(self, vector_store):
        llm = ChatOpenAI()
        memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
        return ConversationalRetrievalChain.from_llm(llm=llm, retriever=vector_store.as_retriever(), memory=memory)


def process_pdf(s3_bucket_name, s3_object_key):
    try:
        s3_helper = S3Helper(s3_bucket_name)
        pdf_bytes = s3_helper.download_file(s3_object_key)
        pdf_processor = PDFProcessor(pdf_bytes)
        extracted_text = pdf_processor.extract_text()
        text_chunks = pdf_processor.split_text_into_chunks(extracted_text)
        return text_chunks
    except Exception as e:
        logger.error(f"PDF processing error: {e}")
        raise


def process_chat(text_chunks, user_question):
    try:
        langchain_handler = LangchainHandler(text_chunks)
        vector_store = langchain_handler.create_vector_store()
        conversation_chain = langchain_handler.create_conversation_chain(vector_store)
        response = conversation_chain({'question': user_question})
        return response['chat_history']
    except Exception as e:
        logger.error(f"Chat processing error: {e}")
        raise


def lambda_handler(event, context):
    try:
        load_dotenv()

        user_question = event.get("user_question", "list transactions")
        s3_bucket_name = event.get("s3_bucket_name")
        s3_object_key = event.get("s3_object_key")

        if not s3_bucket_name or not s3_object_key:
            logger.error("s3_bucket_name or s3_object_key not provided in the event")
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "s3_bucket_name or s3_object_key not provided in the event"})
            }

        # Download PDF from S3
        pdf_text_chunks = process_pdf(s3_bucket_name, s3_object_key)

        # Process Chat
        chat_response = process_chat(pdf_text_chunks, user_question)
        logger.info(f"Chat response: {chat_response}")

        return {
            "statusCode": 200,
            "pdf_text_chunks": pdf_text_chunks,
            "chat_response": chat_response
        }

    except Exception as e:
        logger.error(f"Error in lambda_handler function: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }


if __name__ == "__main__":
    event = {
        "user_question": "What is this PDF about?",
        "s3_object_key": "public/pdfs/NUBANk/input_onepage.pdf",
        "s3_bucket_name": "predictus-ocr134811-ocr"
    }

    result = lambda_handler(event, None)
    print(result)
