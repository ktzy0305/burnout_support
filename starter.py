import openai
import os

from llama_index import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    load_index_from_storage,
)

# This will help for CI / CD deployment
openai.api_key = os.getenv("OPENAI_API_KEY")


# check if storage already exists
PERSIST_DIR = "./storage"
if not os.path.exists(PERSIST_DIR):
    # load the documents and create the index
    documents = SimpleDirectoryReader(input_dir="data", exclude="paul_graham_essay.txt").load_data()
    index = VectorStoreIndex.from_documents(documents)
    # store it for later (persist embeddings on disk)
    index.storage_context.persist(persist_dir=PERSIST_DIR)
else:
    # load the existing index
    storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
    index = load_index_from_storage(storage_context)

# Query Engine
query_engine = index.as_chat_engine()

# Get Response
tries = 0
while tries < 5:
    chat_input = str(input("> "))
    streaming_response = query_engine.stream_chat(chat_input)
    for token in streaming_response.response_gen:
        print(token, end="")
    print("\n")
    # print(f"Response: {response}")
    tries += 1
