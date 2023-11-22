import streamlit as st
css = '''
<style>
.chat-message {
    padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem; display: flex
}
.chat-message.user {
    background-color: #2b313e
}
.chat-message.bot {
    background-color: #475063
}
.chat-message .avatar {
  width: 20%;
}
.chat-message .avatar img {
  max-width: 78px;
  max-height: 78px;
  border-radius: 50%;
  object-fit: cover;
}
.chat-message .message {
  width: 80%;
  padding: 0 1.5rem;
  color: #fff;
}
'''

bot_template = '''
<div class="chat-message bot">
    <div class="avatar">
        <img src="https://i.ibb.co/cN0nmSj/Screenshot-2023-05-28-at-02-37-21.png" style="max-height: 78px; max-width: 78px; border-radius: 50%; object-fit: cover;">
    </div>
    <div class="message">$MSG</div>
</div>
'''

user_template = '''
<div class="chat-message user">
    <div class="avatar">
        <img src="https://i.ibb.co/rdZC7LZ/Photo-logo-1.png">
    </div>    
    <div class="message">$MSG</div>
</div>
'''

class UIClass:
    def __init__(self):
        # Initialize any necessary variables
        # For example, settings for different UI elements
        self.title = "Chat with PDFs"
        self.page_icon = ":books:"

    def setup_page(self):
        # Configure page settings
        st.set_page_config(page_title=self.title, page_icon=self.page_icon)

    def render_header(self):
        # Render the header of the page
        st.header(self.title)

    def render_chat_message(self, user_type, message):
        # Render a chat message
        if user_type == 'bot':
            st.markdown(f"<div class='bot-message'>{message}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='user-message'>{message}</div>", unsafe_allow_html=True)

    def render_auth_form(self):
        # Render an authentication form
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            # Handle login logic
            self.handle_login(username, password)

    def handle_login(self, username, password):
        # Add logic to handle login
        # This is just a placeholder function
        pass

    # You can add more methods to handle other UI elements like sidebars, footers, etc.
