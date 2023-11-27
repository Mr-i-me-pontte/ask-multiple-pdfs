import streamlit as st


# Function to handle chatbot logic
def get_bot_response(user_input):
    # Your chatbot logic here (replace with your actual chatbot logic)
    return f"You said: {user_input}"


# Initialize the session state for page navigation and login status
if 'page' not in st.session_state:
    st.session_state['page'] = 'login'
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False


# Define the Login page content
def login_page():
    st.title("Login Page")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        # You can implement actual authentication logic here
        if username == "your_username" and password == "your_password":
            st.session_state['logged_in'] = True
            st.session_state['page'] = 'home'
        else:
            st.warning("Invalid username or password")


# Define the Home page content
def home_page():
    st.title("Home Page")
    st.write("Welcome to the Home page!")
    if st.button("Go to Chat"):
        st.session_state['page'] = 'chat'


# Define the Chat page content
def chat_page():
    st.title("Chat Page")
    user_input = st.text_input("Type your message here:")
    if st.button("Send"):
        bot_response = get_bot_response(user_input)
        st.text_area("Bot says:", value=bot_response, height=100)
    if st.button("Back to Home"):
        st.session_state['page'] = 'home'


# Display content based on the current page and login status
if st.session_state['page'] == 'login':
    login_page()
elif st.session_state['logged_in']:
    if st.session_state['page'] == 'home':
        home_page()
    elif st.session_state['page'] == 'chat':
        chat_page()
else:
    st.warning("You must log in to access this app.")
