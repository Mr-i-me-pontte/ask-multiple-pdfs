# auth.py

import pandas as pd
import hashlib
import streamlit as st

# Path to the CSV file storing user data
CSV_FILE_PATH = 'user_data.csv'

def load_user_data():
    """Load user data from the CSV file into a dictionary."""
    try:
        user_data = pd.read_csv(CSV_FILE_PATH)
        user_data = user_data.set_index('email').to_dict()['password']
    except FileNotFoundError:
        user_data = {}
    return user_data

def save_user_data(user_data):
    """Save user data from the dictionary to the CSV file."""
    df = pd.DataFrame(list(user_data.items()), columns=['email', 'password'])
    df.to_csv(CSV_FILE_PATH, index=False)

def hash_password(password):
    """Hash a password using SHA-256."""
    sha256 = hashlib.sha256()
    sha256.update(password.encode('utf-8'))
    return sha256.hexdigest()

def authenticate(email, password):
    """Authenticate the user."""
    user_data = load_user_data()
    hashed_password = hash_password(password)
    return email in user_data and user_data[email] == hashed_password

def show_login_form():
    """Display the login and registration form in Streamlit."""
    email = st.sidebar.text_input("Email")
    password = st.sidebar.text_input("Password", type="password")

    if st.sidebar.button("Login"):
        if authenticate(email, password):
            st.session_state['authenticated'] = True
            st.session_state['email'] = email
            st.success("Login successful!")
        else:
            st.error("Invalid email or password")

    if st.sidebar.button("Register"):
        user_data = load_user_data()
        if email not in user_data:
            user_data[email] = hash_password(password)
            save_user_data(user_data)
            st.success("Registration successful! You can now log in.")
        else:
            st.error("Email already exists. Please use a different one.")

def show_logout_form():
    """Display the logout form in Streamlit."""
    st.sidebar.write(f"Logged in as: {st.session_state['email']}")
    if st.sidebar.button("Logout"):
        st.session_state['authenticated'] = False
        st.session_state['email'] = None
        st.experimental_rerun()  # Rerun the app to reset the sidebar
