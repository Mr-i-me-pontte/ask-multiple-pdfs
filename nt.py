import requests
import time
import hmac
import hashlib

def create_signature(secret_key, timestamp, method, request_path, body=''):
    """
    Create a signature for NovaDAX API request.
    """
    string_to_sign = f'{timestamp}{method}{request_path}{body}'
    hmac_key = hmac.new(secret_key.encode(), string_to_sign.encode(), hashlib.sha256)
    return hmac_key.hexdigest()

def get_account_balance(access_key, secret_key):
    """
    Retrieve account balance from NovaDAX API.
    """
    # Endpoint information
    base_url = "https://api.novadax.com"
    method = 'GET'
    request_path = '/v1/account/get'

    # Getting current timestamp
    timestamp = int(time.time() * 1000)

    # Creating the signature
    signature = create_signature(secret_key, timestamp, method, request_path)

    # Headers
    headers = {
        'X-Nova-Access-Key': access_key,
        'X-Nova-Signature': signature,
        'X-Nova-Timestamp': str(timestamp),
    }

    # Making the request
    response = requests.get(base_url + request_path, headers=headers)

    # Returning the response
    return response.json()

# User's API keys
access_key = '47322267-5855-4576-b006-a57993f6bf1c'
secret_key = 'A1YCRsSnIoyrfQy1f5YUUcNDIwoutR3i'

# Get account balance
balance_info = get_account_balance(access_key, secret_key)
print(balance_info)
