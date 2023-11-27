import streamlit as st
import requests
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from threading import Thread

# FastAPI backend
class FastAPIBackend:
    def __init__(self):
        self.api = FastAPI()

        # Define a Pydantic model
        class Item(BaseModel):
            data: str

        # Define a FastAPI route
        @self.api.post("/submit")
        def submit(item: Item):
            # event = {
            #     "user_question": "What is this PDF about?",
            #     "s3_object_key": "public/pdfs/NUBANk/input_onepage.pdf"
            # }
            return {"received_data": item.data}

    def run(self):
        uvicorn.run(self.api, host="127.0.0.1", port=8000)

# Streamlit frontend
class StreamlitFrontend:
    def __init__(self, api_url):
        self.api_url = api_url

    def run(self):
        st.title("Streamlit with embedded FastAPI")

        self.data = st.text_input("Enter some data")
        self.submit_button = st.button("Submit")

        # Sending POST request from Streamlit to FastAPI
        if self.submit_button:
            response = self.send_post_request()
            self.handle_response(response)

    def send_post_request(self):
        try:
            response = requests.post(self.api_url, json={"data": self.data})
            return response
        except requests.exceptions.RequestException as e:
            st.error(f"Failed to connect to the server: {e}")
            return None

    def handle_response(self, response):
        if response and response.status_code == 200:
            st.success(f"Response from server: {response.json()}")
        else:
            st.error("Failed to get a valid response")

if __name__ == "__main__":
    # Start FastAPI backend in a separate thread
    backend = FastAPIBackend()
    Thread(target=backend.run, daemon=True).start()

    # Define the FastAPI server URL
    api_url = "http://localhost:8000/submit"

    # Create and run the Streamlit frontend
    frontend = StreamlitFrontend(api_url)
    frontend.run()
