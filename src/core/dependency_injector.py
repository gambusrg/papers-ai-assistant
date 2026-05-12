import os

import chromadb
import httpx
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
from dotenv import load_dotenv
from groq import Groq

from src.adapters.output.chroma_vector_store import ChromaVectorStore
from src.adapters.output.groq_llm import GroqLLM

load_dotenv()

embedding_function = SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
chroma_client = chromadb.PersistentClient(path="chroma_db/")
papers_collection = chroma_client.get_or_create_collection(name="papers", embedding_function=embedding_function)
vector_store = ChromaVectorStore(collection=papers_collection)

llm = GroqLLM(client=Groq(api_key=os.getenv("GROQ_API_KEY"), http_client=httpx.Client(verify=False)))
