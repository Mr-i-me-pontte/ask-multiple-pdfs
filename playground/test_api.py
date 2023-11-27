# %%
import requests

API_URL = "http://localhost:8000/submit"  # Replace with the actual URL of your API

def test_hello_api():
    try:
        response = requests.post(API_URL)
        print(response)

        if response.status_code == 200:
            data = response.json()
            print("API Response:")
            print(data)
        else:
            print(f"API returned status code {response.status_code}")
    except Exception as e:
        print("Error occurred while fetching data from the API.")
        print(str(e))

if __name__ == "__main__":
    test_hello_api()
