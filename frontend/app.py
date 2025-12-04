import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

url = f"https://ragyoutuber.azurewebsites.net/rag/query?code={os.getenv('AZURE_FUNCTION_KEY')}"

def layout():
    st.markdown("# The Youtuber")
    st.markdown("Ask me something you are interested in about data engineering")
    input = st.text_input(label="Write your question/message below", max_chars=150, key="user_input")


    if st.button("Send question/message") and input.strip() != "":
        response = requests.post(
            url, json={"prompt": input}
        )
    
        data = response.json()

        st.markdown(data["answer"])



if __name__ == "__main__":
    layout()