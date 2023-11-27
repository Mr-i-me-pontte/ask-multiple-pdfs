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


def process_pdf_and_chat_handler(event, context):
    load_dotenv()

    user_question = event.get("user_question", "list transactions")
    s3_object_key = event.get("s3_object_key")

    if not s3_object_key:
        logger.error("s3_object_key not provided in the event")
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "s3_object_key not provided in the event"})
        }

    try:
        s3_helper = S3Helper()
        pdf_bytes = s3_helper.download_file(s3_object_key)
        pdf_text_chunks = process_pdf(pdf_bytes)
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
