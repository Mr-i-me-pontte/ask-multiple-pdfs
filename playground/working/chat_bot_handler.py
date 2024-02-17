import json
import logging
from pprint import PrettyPrinter

from dotenv import load_dotenv

from helpers.langchain_handler import process_chat
from helpers.pdf_processor import process_pdf
from helpers.s3_helper import S3Helper

pp = PrettyPrinter(indent=4).pprint
# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
def process_pdf_and_chat_handler(event, context):
    load_dotenv()

    user_question = event.get("user_question", "hello")

    try:
        s3_helper = S3Helper()
        chat_response = process_chat(pdf_text_chunks, user_question)
        logger.info(f"Chat response: {chat_response}")
        response_messages = []
        for i, message in enumerate(chat_response):
            speaker = "User" if i % 2 == 0 else "Bot"
            response_messages.append({
                "speaker": speaker,
                "message": message.content
            })

    except Exception as e:
        logger.error(f"Error in main function: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }

    return {

        "body": {
            "statusCode": 200,
            "pdf_text_chunks": pdf_text_chunks,
            "chat_response": chat_response,
            "chat_history": json.dumps({"chat_history": response_messages})
        }
    }


if __name__ == "__main__":
    event = {
        "user_question": "What is this PDF about?",
        "s3_object_key": "public/pdfs/NUBANk/input_onepage.pdf"
    }
    x = process_pdf_and_chat_handler(event, None)
    pp(x)
