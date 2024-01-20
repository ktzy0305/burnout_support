import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.embeddings import CacheBackedEmbeddings
from langchain.storage import LocalFileStore
from langchain.text_splitter import RecursiveCharacterTextSplitter

from constants import BASE_DIR

class VectorStore:
  def __init__(self):
    self.store = LocalFileStore(os.path.join(BASE_DIR, "cache"))
    self.core_embeddings_model = HuggingFaceInferenceAPIEmbeddings(
      api_key = os.environ.get("HUGGINGFACEHUB_API_TOKEN"),
      model_name="sentence-transformers/all-MiniLM-l6-v2"
    )
    self.embedder = CacheBackedEmbeddings.from_bytes_store(self.core_embeddings_model, self.store)
  
  def get_instance():
    # if ./cache does not exist
    # instantiate new vector store
    # else
    # read from ./cache
    return
  
