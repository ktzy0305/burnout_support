import os
from langchain_community.document_loaders import PyPDFLoader, WebBaseLoader
from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.embeddings import CacheBackedEmbeddings
from langchain.storage import LocalFileStore
from langchain.text_splitter import RecursiveCharacterTextSplitter

BASE_DIR = os.getcwd()
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

text_splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP, length_function=len)

def load_pdf(vectorstore: any):
  pdf_path = os.path.join(BASE_DIR, "data", "pdf")
  chunks = None
  for file in os.listdir(pdf_path):
    curr_path = os.path.join(pdf_path, file)
    loader = PyPDFLoader(curr_path)
    if chunks is None:
      chunks = get_chunks(loader)
    else:
      chunks += get_chunks(loader)
  return chunks

def load_urls(vectorstore: any):
  url_path = os.path.join(BASE_DIR, "data", "html", "sources.txt")
  chunks = None
  with open(url_path, "r") as fp:
    while line := fp.readline():
      loader = WebBaseLoader(line)
      if chunks is None:
        chunks = get_chunks(loader)
      else:
        chunks += get_chunks(loader)
  print(chunks)
  return chunks

def get_chunks(loader):
  pages = loader.load_and_split()
  chunks = text_splitter.transform_documents(pages)
  return chunks
  