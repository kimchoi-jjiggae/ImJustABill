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
def query(input_text):
    location = "ira.pdf_index"
    storage_context = StorageContext.from_defaults(persist_dir=location)

    # PINECONE_API_KEY = os.getenv("PINECONE_API_KEY", "")
    # if PINECONE_API_KEY:
    #     if can_import("extensions.pinecone_storage"):
    #         PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT", "")
    #         assert (
    #             PINECONE_ENVIRONMENT
    #         ), "\033[91m\033[1m" + "PINECONE_ENVIRONMENT environment variable is missing from .env" + "\033[0m\033[0m"
    #         from extensions.pinecone_storage import PineconeResultsStorage
    #         results_storage = PineconeResultsStorage(OPENAI_API_KEY, PINECONE_API_KEY, PINECONE_ENVIRONMENT, LLM_MODEL, LLAMA_MODEL_PATH, RESULTS_STORE_NAME, OBJECTIVE)
    #         print("\nReplacing results storage: " + "\033[93m\033[1m" +  "Pinecone" + "\033[0m\033[0m")


    #TODO what is this stuff? Pinecone, Weaviate, Chroma, Qdrant, 

    #query it
    index = load_index_from_storage(storage_context)

    query_engine = index.as_query_engine()
    response = query_engine.query(input_text)

        # "Write me a table of contents for this bill. With a brief one sentence summary of each section.")
    # print(response)
    with Message(label="Answer") as m:
        m.write("### Response")
        m.write(response)

    #TODO fix token limit

class Message:
    # ai_icon = "./img/robot.png"

    def __init__(self, label: str, expanded: bool = True):
        self.label = label
        self.expanded = expanded

    def __enter__(self):
        message_area, icon_area = st.columns([10, 1])
        # icon_area.image(self.ai_icon, caption="QuizMeGPT")

        self.expander = message_area.expander(label=self.label, expanded=self.expanded)

        return self

    def __exit__(self, ex_type, ex_value, trace):
        pass

    def write(self, content):
        self.expander.markdown(content)

#TODO chatbot feature https://gpt-index.readthedocs.io/en/latest/guides/tutorials/building_a_chatbot.html

if __name__ == "__main__":
    st.set_page_config(
        initial_sidebar_state="expanded",
        page_title="I'm Just a Bill",
        layout="centered",
    )

    with st.sidebar:
        openai_api_key = st.text_input('Your OpenAI API KEY', type="password")

    st.title("WTF does this bill mean for me")
    text = st.text_area("What's your question?", height=300)
    if text:
        query(text)
