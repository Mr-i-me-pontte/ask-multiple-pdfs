import pandas as pd
import hashlib
import streamlit as st

# Path to the CSV file storing user data
CSV_FILE_PATH = 'user_data.csv'

def load_user_data():
    """
    Load user data from the CSV file into a dictionary.
    Returns a dictionary where keys are usernames and values are hashed passwords.
    """
    try:
        user_data = pd.read_csv(CSV_FILE_PATH)
        user_data = user_data.set_index('username').to_dict()['password']
    except FileNotFoundError:
        # Return an empty dictionary if the file does not exist
        user_data = {}
    return user_data

def save_user_data(user_data):
    """
    Save user data from the dictionary to the CSV file.
    The user_data argument is a dictionary with usernames as keys and hashed passwords as values.
    """
    df = pd.DataFrame(list(user_data.items()), columns=['username', 'password'])
    df.to_csv(CSV_FILE_PATH, index=False)

def hash_password(password):
    """
    Hash a password using SHA-256 and return the hexadecimal digest.
    """
    sha256 = hashlib.sha256()
    sha256.update(password.encode('utf-8'))
    return sha256.hexdigest()

def authenticate(username, password):
    """
    Authenticate a user. Returns True if the username exists and the password matches, False otherwise.
    """
    user_data = load_user_data()
    hashed_password = hash_password(password)
    return username in user_data and user_data[username] == hashed_password

def show_auth_form():
    """
    Display the login and registration form in Streamlit's sidebar.
    Handles user login and registration.
    """
    st.sidebar.title("Authentication")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")

    if st.sidebar.button("Login"):
        if authenticate(username, password):
            st.session_state['authenticated'] = True
            st.session_state['username'] = username
            st.success("Login successful!")
        else:
            st.error("Invalid username or password")

    if st.sidebar.button("Register"):
        user_data = load_user_data()
        if username not in user_data:
            user_data[username] = hash_password(password)
            save_user_data(user_data)
            st.success("Registration successful! You can now log in.")
        else:
            st.error("Username already exists. Please choose a different one.")

def main():
    if "authenticated" not in st.session_state:
        st.session_state['authenticated'] = False

    if not st.session_state['authenticated']:
        show_auth_form()
    else:
        st.write(f"Logged in as: {st.session_state['username']}")
        if st.button("Logout"):
            st.session_state['authenticated'] = False
            st.session_state['username'] = None

# Streamlit app entry point
if __name__ == '__main__':
    main()
