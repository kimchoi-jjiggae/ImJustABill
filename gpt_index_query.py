import openai
import llama_index

from unstructured.partition.auto import partition
from llama_index import download_loader, GPTVectorStoreIndex, ServiceContext, SimpleDirectoryReader, StorageContext, load_index_from_storage,LLMPredictor
from pathlib import Path
from dotenv import load_dotenv
from langchain import OpenAI
import os

load_dotenv()


#bring in the stored index as context

location = "ira.pdf_index_unstructured"
llm_predictor = LLMPredictor(llm=OpenAI(temperature=0, model_name="text-davinci-003", max_tokens=2000))
service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor)


storage_context = StorageContext.from_defaults(persist_dir=location)
index = load_index_from_storage(storage_context, service_context=service_context)

#TODO what is this stuff? Pinecone, Weaviate, Chroma, Qdrant, 

#query it
query_engine = index.as_query_engine()
response = query_engine.query("Write me a medium blog post summarizing this bill.")
print(response)

#TODO fix token limit

#TODO chatbot feature