import argparse
from dotenv import load_dotenv
from PyPDF2 import PdfReader
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
        self.user_question = None

    def extract_text_from_pdfs(self):
        text = ""
        for pdf in self.pdf_paths:
            pdf_reader = PdfReader(pdf)
            for page in pdf_reader.pages:
                text += page.extract_text() or ''
        return text

    def split_text_into_chunks(self, text):
        text_splitter = CharacterTextSplitter(
            separator="\n",
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
            length_function=len
        )
        return text_splitter.split_text(text)

    def create_vector_store(self, text_chunks):
        embeddings = OpenAIEmbeddings()
        return FAISS.from_texts(texts=text_chunks, embedding=embeddings)

    def create_conversation_chain(self, vector_store):
        llm = ChatOpenAI()
        memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
        return ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=vector_store.as_retriever(),
            memory=memory
        )

    def process_pdf_and_question(self):
        try:
            raw_text = self.extract_text_from_pdfs()
            text_chunks = self.split_text_into_chunks(raw_text)
            vector_store = self.create_vector_store(text_chunks)
            conversation_chain = self.create_conversation_chain(vector_store)

            response = conversation_chain({'question': self.user_question})
            chat_history = response['chat_history']

            for i, message in enumerate(chat_history):
                speaker = "User" if i % 2 == 0 else "Bot"
                print(f"{speaker}: {message.content}")

        except Exception as e:
            print(f"An error occurred: {str(e)}")

def main():
    load_dotenv()
    parser = argparse.ArgumentParser(description="Chat with PDFs")
    parser.add_argument("pdf_paths", nargs='+', help="Paths to PDF files to process")
    parser.add_argument("user_question", help="Question to ask about the documents")
    args = parser.parse_args()

    processor = PDFChatProcessor(args.pdf_paths)
    processor.user_question = args.user_question
    processor.process_pdf_and_question()

if __name__ == '__main__':
    main()
