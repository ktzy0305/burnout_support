import os
from langchain_community.document_loaders import PyPDFLoader, WebBaseLoader
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter

BASE_DIR = os.getcwd()
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP, length_function=len
)


def load_pdf():
    pdf_dir = os.path.join(BASE_DIR, "data", "pdf")
    document_chunks = []
    files = os.listdir(pdf_dir)
    total_num_files = len(files)
    for count, file in enumerate(files):
        curr_path = os.path.join(pdf_dir, file)
        loader = PyPDFLoader(curr_path)
        pages = loader.load_and_split()
        chunks = text_splitter.transform_documents(pages)
        document_chunks.append(chunks)

        # Loading Status
        print(f"Loaded chunks from {count + 1} out of {total_num_files} pdf files.")

    # Return a list of document chunks
    return document_chunks

def load_urls():
    url_path = os.path.join(BASE_DIR, "data", "html", "sources.txt")
    chunks = None
    count = 0
    with open(url_path, "r") as fp:
        while line := fp.readline():
            loader = WebBaseLoader(line).load()
            if chunks is None:
                chunks = text_splitter.transform_documents(loader)
            else:
                chunks += text_splitter.transform_documents(loader)
                        # Loading Status
            count += 1
            print(f"Loaded chunks from {count} urls.")
    return chunks
