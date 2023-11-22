# # auth.py
# import streamlit as st
# import pandas as pd
# import hashlib
#
# class AuthHandler:
#     CSV_FILE_PATH = 'user_data.csv'
#
#     def load_user_data(self):
#         try:
#             user_data = pd.read_csv(self.CSV_FILE_PATH)
#             user_data = user_data.set_index('username').to_dict()['password']
#         except FileNotFoundError:
#             user_data = {}
#         return user_data
#
#     def save_user_data(self, user_data):
#         df = pd.DataFrame(list(user_data.items()), columns=['username', 'password'])
#         df.to_csv(self.CSV_FILE_PATH, index=False)
#
#     def hash_password(self, password):
#         sha256 = hashlib.sha256()
#         sha256.update(password.encode('utf-8'))
#         return sha256.hexdigest()
#
#     def authenticate(self, username, password):
#         user_data = self.load_user_data()
#         hashed_password = self.hash_password(password)
#         return username in user_data and user_data[username] == hashed_password
#
#     def show_auth_form(self):
#         st.sidebar.title("Authentication")
#         username = st.sidebar.text_input("Username")
#         password = st.sidebar.text_input("Password", type="password")
#
#         if st.sidebar.button("Login"):
#             if self.authenticate(username, password):
#                 st.session_state['authenticated'] = True
#                 st.session_state['username'] = username
#                 st.success("Login successful!")
#             else:
#                 st.error("Invalid username or password")
#
#         if st.sidebar.button("Register"):
#             user_data = self.load_user_data()
#             if username not in user_data:
#                 user_data[username] = self.hash_password(password)
#                 self.save_user_data(user_data)
#                 st.success("Registration successful! You can now log in.")
#             else:
#                 st.error("Username already exists. Please choose a different one.")


import hashlib

import pandas as pd
import streamlit as st


class AuthHandler:
    CSV_FILE_PATH = 'user_data.csv'

    def load_user_data(self):
        """
        Load user data from the CSV file into a dictionary.
        Returns a dictionary where keys are usernames and values are hashed passwords.
        """
        try:
            user_data = pd.read_csv(self.CSV_FILE_PATH)
            user_data = user_data.set_index('username').to_dict()['password']
        except FileNotFoundError:
            user_data = {}
        return user_data

    def save_user_data(self, user_data):
        """
        Save user data from the dictionary to the CSV file.
        """
        df = pd.DataFrame(list(user_data.items()), columns=['username', 'password'])
        df.to_csv(self.CSV_FILE_PATH, index=False)

    def hash_password(self, password):
        """
        Hash a password using SHA-256 and return the hexadecimal digest.
        """
        sha256 = hashlib.sha256()
        sha256.update(password.encode('utf-8'))
        return sha256.hexdigest()

    def authenticate(self, username, password):
        """
        Authenticate a user.
        """
        user_data = self.load_user_data()
        hashed_password = self.hash_password(password)
        return username in user_data and user_data[username] == hashed_password

    def show_auth_form(self):
        """
        Display the login and registration form in Streamlit's sidebar.
        """
        st.sidebar.title("Authentication")
        username = st.sidebar.text_input("Username")
        password = st.sidebar.text_input("Password", type="password")

        if st.sidebar.button("Login"):
            if self.authenticate(username, password):
                st.session_state['authenticated'] = True
                st.session_state['username'] = username
                st.success("Login successful!")
            else:
                st.error("Invalid username or password")

        if st.sidebar.button("Register"):
            user_data = self.load_user_data()
            if username not in user_data:
                user_data[username] = self.hash_password(password)
                self.save_user_data(user_data)
                st.success("Registration successful! You can now log in.")
            else:
                st.error("Username already exists. Please choose a different one.")
