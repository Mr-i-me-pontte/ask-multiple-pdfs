import os
import getpass
from PyPDF2 import PdfReader
from nltk.tokenize import sent_tokenize
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain

# Set up the OpenAI API Key
os.environ['OPENAI_API_KEY'] = getpass.getpass('OpenAI API Key:')

def load_pdf(file_path):
    """ Load a PDF file and return its text content. """
    try:
        with open(file_path, 'rb') as file:
            reader = PdfReader(file)
            return ''.join(page.extract_text() for page in reader.pages)
    except Exception as e:
        print(f"Failed to load {file_path}: {e}")
        return ""

def get_text_chunks(text):
    """ Split the text into manageable chunks. """
    text_splitter = CharacterTextSplitter(separator="\n", chunk_size=1000, chunk_overlap=200, length_function=len)
    return text_splitter.split_text(text)

def get_vectorstore(text_chunks):
    """ Create a vector store from the given text chunks. """
    embeddings = OpenAIEmbeddings()
    return FAISS.from_texts(texts=text_chunks, embedding=embeddings)

def get_conversation_chain(vectorstore):
    """ Create and return a ConversationalRetrievalChain with the given vector store. """
    memory = ConversationBufferMemory()
    return ConversationalRetrievalChain(vector_store=vectorstore, memory=memory)

def main():
    file_path = '../../data/input.pdf'  # Replace with actual file path
    pdf_text = load_pdf(file_path)
    if not pdf_text:
        return

    text_chunks = get_text_chunks(pdf_text)
    vectorstore = get_vectorstore(text_chunks)
    conversation_chain = get_conversation_chain(vectorstore)

    # Start chat
    print("Welcome to MultiPDF Chat App. Ask me anything about the loaded PDFs!")
    while True:
        query = input("You: ").strip()
        if query.lower() == 'exit':
            print("Exiting the chat.")
            break
        response = conversation_chain.process_input(query)
        print("MultiPDF Chat App:", response or "I'm sorry, I don't have enough information on that topic.")

if __name__ == "__main__":
    main()
