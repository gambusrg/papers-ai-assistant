import chromadb

from src.adapters.output.chroma_vector_store import ChromaVectorStore
from src.adapters.output.mock_llm import MockLLM

chroma_client = chromadb.PersistentClient(path="chroma_db/")
papers_collection = chroma_client.get_or_create_collection(name="papers")
vector_store = ChromaVectorStore(collection=papers_collection)

llm = MockLLM()
