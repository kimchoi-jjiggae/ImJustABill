import openai
import llama_index

# from unstructured.partition.auto import partition
from llama_index import download_loader, GPTVectorStoreIndex, ServiceContext, SimpleDirectoryReader, StorageContext, load_index_from_storage
from pathlib import Path
from dotenv import load_dotenv
from langchain import OpenAI
import streamlit as st

import os

load_dotenv()


#bring in the stored index as context
def query():
    location = "ira.pdf_index"

    storage_context = StorageContext.from_defaults(persist_dir=location)
    index = load_index_from_storage(storage_context)

    #TODO what is this stuff? Pinecone, Weaviate, Chroma, Qdrant, 

    #query it
    query_engine = index.as_query_engine()
    response = query_engine.query("Write me a table of contents for this bill. With a brief one sentence summary of each section.")
    print(response)

    #TODO fix token limit

#TODO chatbot feature https://gpt-index.readthedocs.io/en/latest/guides/tutorials/building_a_chatbot.html

if __name__ == "__main__":
    st.set_page_config(
        initial_sidebar_state="expanded",
        page_title="QuizMeGPT Streamlit",
        layout="centered",
    )

    with st.sidebar:
        openai_api_key = st.text_input('Your OpenAI API KEY', type="password")

    st.title("WTF does this bill mean for me")
    text = st.text_area("Upload the bill", height=300)
    if text:
        quizflow(text, openai_api_key)
