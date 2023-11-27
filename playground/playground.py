import streamlit as st
import requests
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from threading import Thread

# Define a FastAPI app
api = FastAPI()

# Define a Pydantic model
class Item(BaseModel):
    data: str

# Define a FastAPI route
@api.post("/submit")
def submit(item: Item):
    return {"received_data": item.data}

# Function to run FastAPI with Uvicorn
def run_api():
    uvicorn.run(api, host="127.0.0.1", port=8000)

# Start FastAPI in a separate thread
Thread(target=run_api, daemon=True).start()

# Streamlit interface
st.title("Streamlit with embedded FastAPI")

data = st.text_input("Enter some data")
submit_button = st.button("Submit")

# Sending POST request from Streamlit to FastAPI
if submit_button:
    response = requests.post("http://localhost:8000/submit", json={"data": data})
    if response.status_code == 200:
        st.success(f"Response from server: {response.json()}")
    else:
        st.error("Failed to get response")
