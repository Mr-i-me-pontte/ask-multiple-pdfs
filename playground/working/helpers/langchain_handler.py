import logging

from langchain import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.memory import ConversationBufferMemory

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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
