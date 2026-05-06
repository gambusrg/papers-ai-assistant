import os

import chromadb
from google import genai

from src.adapters.output.chroma_vector_store import ChromaVectorStore
from src.adapters.output.google_llm import GoogleLLM

chroma_client = chromadb.PersistentClient(path="chroma_db/")
papers_collection = chroma_client.get_or_create_collection(name="papers")
vector_store = ChromaVectorStore(collection=papers_collection)

llm = GoogleLLM(client=genai.Client(api_key=os.getenv("GOOGLE_API_KEY")))
