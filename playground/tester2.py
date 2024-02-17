import os
from PyPDF2 import PdfReader
from dotenv import load_dotenv
from langchain.prompts.chat import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate, AIMessage
from langchain.prompts.message import MessagePromptTemplate
from langchain.prompts.prompt import PromptTemplate
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import chat

# Constants for chunking
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

class PDFChatProcessor:
    def __init__(self, openai_api_key):
        self.openai_api_key = openai_api_key

    def extract_text_from_pdf(self, pdf_path):
        try:
            pdf_reader = PdfReader(pdf_path)
            return ''.join([page.extract_text() or '' for page in pdf_reader.pages])
        except Exception as e:
            raise Exception(f"Error reading {pdf_path}: {e}")

    def split_text_into_chunks(self, text):
        text_chunks = [text[i:i + CHUNK_SIZE] for i in range(0, len(text), CHUNK_SIZE - CHUNK_OVERLAP)]
        return text_chunks

    def create_vector_store(self, text_chunks):
        embeddings = OpenAIEmbeddings()
        vector_store = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
        return vector_store

    def create_conversation_chain(self, vector_store):
        system_message_template = "You are a helpful assistant that extracts information from PDFs."
        system_message_prompt = SystemMessagePromptTemplate.from_template(template=system_message_template)

        user_message_template = "{text}"
        user_message_prompt = HumanMessagePromptTemplate.from_template(template=user_message_template)

        chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, user_message_prompt])

        llm = chat(openai_api_key=self.openai_api_key)
        memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
        conversation_chain = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=vector_store.as_retriever(),
            memory=memory
        )
        return conversation_chain

    def process_pdf_and_question(self, pdf_paths, user_question):
        try:
            raw_text = ""
            for pdf_path in pdf_paths:
                raw_text += self.extract_text_from_pdf(pdf_path)

            text_chunks = self.split_text_into_chunks(raw_text)
            vector_store = self.create_vector_store(text_chunks)
            conversation_chain = self.create_conversation_chain(vector_store)

            formatted_prompt = conversation_chain.format_prompt(text=user_question)
            chat_completion = chat(formatted_prompt.to_messages())
            ai_response = chat_completion[0].content

            return ai_response
        except Exception as e:
            raise Exception(f"An error occurred: {e}")

if __name__ == '__main__':
    # For local testing
    load_dotenv()
    openai_api_key = os.getenv("OPENAI_API_KEY")

    pdf_paths = ["/Users/Mr-i-me/code/Mr-i-me-pontte/ai/ask-multiple-pdfs/data/input_onepage.pdf"]
    user_question = "list transactions"

    pdf_chat_processor = PDFChatProcessor(openai_api_key)
    result = pdf_chat_processor.process_pdf_and_question(pdf_paths, user_question)
    print(result)
