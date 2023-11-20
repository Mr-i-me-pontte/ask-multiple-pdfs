from flask import Flask, request, jsonify
import os
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain

app = Flask(__name__)

# Global variables to store PDF text and conversation chain
pdf_text = ""
conversation_chain = None

@app.route('/upload_pdf', methods=['POST'])
def upload_pdf():
    global pdf_text, conversation_chain
    file = request.files['file']
    pdf_text = ''.join(page.extract_text() for page in PdfReader(file).pages)

    text_chunks = get_text_chunks(pdf_text)
    vectorstore = get_vectorstore(text_chunks)
    conversation_chain = get_conversation_chain(vectorstore)

    return jsonify({"message": "PDF uploaded and processed successfully"})

@app.route('/ask', methods=['POST'])
def ask():
    global conversation_chain
    query = request.json.get('query', '')
    if not conversation_chain or not query:
        return jsonify({"response": "No PDF loaded or empty query"})

    response = conversation_chain.process_input(query)
    return jsonify({"response": response or "I'm sorry, I don't have enough information on that topic."})

def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(separator="\n", chunk_size=1000, chunk_overlap=200, length_function=len)
    return text_splitter.split_text(text)

def get_vectorstore(text_chunks):
    embeddings = OpenAIEmbeddings()
    return FAISS.from_texts(texts=text_chunks, embedding=embeddings)

def get_conversation_chain(vectorstore):
    memory = ConversationBufferMemory()
    return ConversationalRetrievalChain(vector_store=vectorstore, memory=memory)

if __name__ == "__main__":
    app.run(debug=True)
