import os

from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.embeddings import CacheBackedEmbeddings
from langchain.storage import LocalFileStore

from constants import BASE_DIR
from source_loader import load_pdf, load_urls

class VectorStore:
    def __init__(self):
        self.store = LocalFileStore(os.path.join(BASE_DIR, "cache"))
        self.core_embeddings_model = HuggingFaceInferenceAPIEmbeddings(
            api_key=os.environ.get("HUGGINGFACEHUB_API_TOKEN"),
            model_name="sentence-transformers/all-MiniLM-l6-v2"
        )
        self.embedder = CacheBackedEmbeddings.from_bytes_store(
            self.core_embeddings_model, self.store)
        self.db = None

    def get_db(self):
        saved_index_dir = os.path.join(BASE_DIR, "saved_index")
        
        # If the cache directory does not exist
        if not os.path.exists(saved_index_dir):
            website_chunks = load_urls()
            self.db = FAISS.from_documents(website_chunks, self.embedder)
            pdf_chunks = load_pdf()
            for chunk in pdf_chunks:
                self.db.add_documents(chunk)
            self.db.save_local(os.path.join(BASE_DIR, "saved_index"))
        else:   
            self.db = FAISS.load_local(os.path.join(BASE_DIR, "saved_index"), self.embedder)
        
        # Return instance of db
        return self.db
