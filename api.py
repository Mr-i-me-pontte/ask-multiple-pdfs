import json
import os
from PyPDF2 import PdfReader
from dotenv import load_dotenv
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain

# Constants for chunking
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

class PDFChatProcessor:
    def __init__(self, pdf_paths):
        self.pdf_paths = pdf_paths

    def extract_text_from_pdfs(self):
        text = ""
        for pdf in self.pdf_paths:
            text += self._extract_text_from_pdf(pdf)
        return text

    def _extract_text_from_pdf(self, pdf_path):
        try:
            pdf_reader = PdfReader(pdf_path)
            return ''.join([page.extract_text() or '' for page in pdf_reader.pages])
        except Exception as e:
            raise Exception(f"Error reading {pdf_path}: {e}")

    def process_pdf_and_question(self, user_question):
        try:
            raw_text = self.extract_text_from_pdfs()
            text_chunks = self._split_text_into_chunks(raw_text)
            vector_store = self._create_vector_store(text_chunks)
            conversation_chain = self._create_conversation_chain(vector_store)

            response = conversation_chain({'question': user_question})
            return response['chat_history']
        except Exception as e:
            raise Exception(f"An error occurred: {e}")

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

def lambda_handler(event, context):
    try:
        load_dotenv()
        user_question = event.get("user_question", "list transactions")
        pdf_paths = event.get("pdf_paths", [])

        if not pdf_paths:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "pdf_paths not provided in the event"})
            }

        processor = PDFChatProcessor(pdf_paths)
        chat_history = processor.process_pdf_and_question(user_question)

        response_messages = []
        for i, message in enumerate(chat_history):
            speaker = "User" if i % 2 == 0 else "Bot"
            response_messages.append({
                "speaker": speaker,
                "message": message.content
            })

        return {
            "statusCode": 200,
            "body": json.dumps({"chat_history": response_messages})
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }

if __name__ == '__main__':
    # For local testing
    user_question = "list transactions"
    pdf_paths = ["/Users/Mr-i-me/code/Mr-i-me-pontte/ai/ask-multiple-pdfs/data/input_onepage.pdf"]

    event = {
        "user_question": user_question,
        "pdf_paths": pdf_paths
    }

    result = lambda_handler(event, None)
    print(result)
