import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.embeddings import CacheBackedEmbeddings
from langchain.storage import LocalFileStore
from langchain.text_splitter import RecursiveCharacterTextSplitter

BASE_DIR = os.getcwd()
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

text_splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)

def load_pdf(vectorstore: any):
  pdf_path = os.path.join(BASE_DIR, "data", "pdf")
  for file in os.listdir(pdf_path):
    curr_path = os.path.join(pdf_path, file)
    chunks = get_chunks(curr_path)
    vectorstore.add_documents(chunks)
    print(file)

def get_chunks(file_path):
  loader = PyPDFLoader(file_path)
  pages = loader.load_and_split()
  chunks = text_splitter.transform_documents(pages)
  return chunks
