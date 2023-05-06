import openai
import llama_index

# from unstructured.partition.auto import partition
from llama_index import download_loader, GPTVectorStoreIndex, ServiceContext, SimpleDirectoryReader, StorageContext, load_index_from_storage
from pathlib import Path
from dotenv import load_dotenv
from langchain import OpenAI
import os

load_dotenv()

#TODO figure out how to do this using GPT-4 instead of GPT-3, debatable whether it's necessary for constructing the index or nah


#Method to build a new index out of one file clean this up, I am just pumping in the raw 10-K, also haven't tested this with other stuff
def build_index(input_file_path: str):
    documents = SimpleDirectoryReader(input_files=[input_file_path]).load_data()
    index = GPTVectorStoreIndex.from_documents(documents)
    index.storage_context.persist(persist_dir=input_file_path+"_index")


#TODO: figure out how to integrate unstructured
def build_index_unstructured(input_file_path: str):
    UnstructuredReader = download_loader("UnstructuredReader", refresh_cache=True, use_gpt_index_import=True)
    loader = UnstructuredReader()
    docs = loader.load_data(file=Path(input_file_path));
    documents = SimpleDirectoryReader(input_files=[input_file_path]).load_data()
    index = GPTVectorStoreIndex.from_documents(documents)
    index.storage_context.persist(persist_dir=input_file_path+"_index")


build_index('./ira.pdf')