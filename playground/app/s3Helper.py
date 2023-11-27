import boto3
from PyPDF2 import PdfReader
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS

# Constants
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
S3_BUCKET_NAME = "predictus-ocr134811-ocr"
S3_OBJECT_KEY = "public/pdfs/NUBANk/NUBANk.pdf"
LOCAL_PDF_PATH = "NUBANk.pdf"


def download_pdf_from_s3(bucket_name, object_key, local_path):
    try:
        s3 = boto3.client('s3')
        s3.download_file(bucket_name, object_key, local_path)
        print(f"Downloaded {object_key} to {local_path}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


def extract_text_from_pdf(pdf_path):
    try:
        pdf_reader = PdfReader(pdf_path)
        return ''.join([page.extract_text() or '' for page in pdf_reader.pages])
    except Exception as e:
        raise Exception(f"Error reading {pdf_path}: {e}")


def split_text_into_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n", chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP, length_function=len)
    return text_splitter.split_text(text)


def create_vector_store(text_chunks):
    embeddings = OpenAIEmbeddings()
    return FAISS.from_texts(texts=text_chunks, embedding=embeddings)


def create_conversation_chain(vector_store):
    llm = ChatOpenAI()
    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
    return ConversationalRetrievalChain.from_llm(
        llm=llm, retriever=vector_store.as_retriever(), memory=memory)


def process_pdf_and_question(pdf_paths, user_question):
    try:
        # Download the PDF from S3
        download_pdf_from_s3(S3_BUCKET_NAME, S3_OBJECT_KEY, LOCAL_PDF_PATH)

        # Extract text from the downloaded PDF
        raw_text = extract_text_from_pdf(LOCAL_PDF_PATH)
        text_chunks = split_text_into_chunks(raw_text)
        vector_store = create_vector_store(text_chunks)
        conversation_chain = create_conversation_chain(vector_store)

        response = conversation_chain({'question': user_question})
        return response['chat_history']
    except Exception as e:
        raise Exception(f"An error occurred: {e}")


if __name__ == "__main__":
    user_question = "What is this PDF about?"

    pdf_paths = [LOCAL_PDF_PATH]
    response = process_pdf_and_question(pdf_paths, user_question)
    print(response)
