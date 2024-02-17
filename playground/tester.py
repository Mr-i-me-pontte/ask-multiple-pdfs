import os
from PyPDF2 import PdfReader
from dotenv import load_dotenv
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain.output_parsers import CommaSeparatedListOutputParser

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
        text_splitter = CharacterTextSplitter(
            separator="\n", chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP, length_function=len)
        return text_splitter.split_text(text)

    def create_vector_store(self, text_chunks):
        embeddings = OpenAIEmbeddings()
        vector_store = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
        return vector_store

    def create_conversation_chain(self, vector_store):
        llm = ChatOpenAI(model="gpt-4", temperature=0, openai_api_key=self.openai_api_key)
        memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
        conversation_chain = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=vector_store.as_retriever(),
            memory=memory
        )
        return conversation_chain

    def process_pdf_and_question(self, pdf_paths, user_question):
        try:
            raw_text = ''.join([self.extract_text_from_pdf(pdf_path) for pdf_path in pdf_paths])
            text_chunks = self.split_text_into_chunks(raw_text)
            vector_store = self.create_vector_store(text_chunks)
            conversation_chain = self.create_conversation_chain(vector_store)

            human_message_template = "{text}"
            human_message_prompt = HumanMessagePromptTemplate.from_template(template=human_message_template)

            chat_prompt = ChatPromptTemplate.from_messages([human_message_prompt])

            response = conversation_chain(chat_prompt.format_prompt(text=user_question).to_messages())
            chat_history = response['chat_history']

            response_messages = [{
                "speaker": "User" if i % 2 == 0 else "Bot",
                "message": message.content
            } for i, message in enumerate(chat_history)]

            return response_messages
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
