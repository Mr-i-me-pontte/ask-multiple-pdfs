
import hashlib

import pandas as pd
import streamlit as st

class AuthHandler:
    def __init__(self, csv_file_path):
        self.csv_file_path = csv_file_path
        self.user_data = self.load_user_data()

    def load_user_data(self):
        try:
            df = pd.read_csv(self.csv_file_path)
            return {row['username']: row['password'] for _, row in df.iterrows()}
        except FileNotFoundError:
            return {}

    def save_user_data(self):
        pd.DataFrame(self.user_data.items(), columns=['username', 'password']).to_csv(self.csv_file_path, index=False)

    def hash_password(self, password):
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

    def authenticate(self, username, password):
        return self.user_data.get(username) == self.hash_password(password)

    def register(self, username, password):
        if username in self.user_data:
            return False
        self.user_data[username] = self.hash_password(password)
        self.save_user_data()
        return True
