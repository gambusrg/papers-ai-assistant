import os

import chromadb
import httpx
from dotenv import load_dotenv
from groq import Groq

from src.adapters.output.chroma_vector_store import ChromaVectorStore
from src.adapters.output.groq_llm import GroqLLM

load_dotenv()

chroma_client = chromadb.PersistentClient(path="chroma_db/")
papers_collection = chroma_client.get_or_create_collection(name="papers")
vector_store = ChromaVectorStore(collection=papers_collection)

llm = GroqLLM(client=Groq(api_key=os.getenv("GROQ_API_KEY"), http_client=httpx.Client(verify=False)))
