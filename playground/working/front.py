import streamlit as st
import requests
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from threading import Thread

from process_pdf_and_chat import process_pdf_and_chat_handler


# FastAPI backend
class FastAPIBackend:
    def __init__(self):
        self.api = FastAPI()

        class Item(BaseModel):
            data: dict

        @self.api.post("/process_pdf")
        def process_pdf(item: Item):
            return process_pdf_and_chat_handler(item)

    def run(self):
        uvicorn.run(self.api, host="127.0.0.1", port=8000)


# Streamlit frontend
class StreamlitFrontend:
    def __init__(self, api_url):
        self.api_url = api_url

    def run(self):
        st.title("Streamlit with embedded FastAPI")

        # Modify the input type if necessary
        self.data = st.text_input("Enter some data")
        self.submit_button = st.button("Submit")

        if self.submit_button:
            response = self.send_post_request()
            self.handle_response(response)

    def send_post_request(self):
        try:
            response = requests.post(self.api_url, json={"data": self.data})
            return response
        except requests.exceptions.RequestException as e:
            st.error(f"Failed to connect to the server: {e}")

    def handle_response(self, response):
        if response and response.status_code == 200:
            st.success(f"Response from server: {response.json()}")
        else:
            st.error("Failed to get a valid response")


if __name__ == "__main__":
    backend = FastAPIBackend()
    Thread(target=backend.run, daemon=True).start()

    api_url = "http://localhost:8000/process_pdf"
    frontend = StreamlitFrontend(api_url)
    frontend.run()
