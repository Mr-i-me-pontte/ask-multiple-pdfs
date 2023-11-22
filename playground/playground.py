import streamlit as st
import streamlit.components.v1 as components

# Read the content of your index.html file
with open('index.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# Render the HTML content using components.html
st.markdown("## Rendered HTML from index.html")
components.html(html_content, width=800, height=600, scrolling=True)
