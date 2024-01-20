from langchain_community.llms import HuggingFaceHub
from langchain_community.vectorstores import FAISS
from transformers import AutoTokenizer

from prompts import therapist_system_fpv, therapist_system_prompt
from vector_store import VectorStore

class LLM:
    def __init__(self):
        # model_string = "mistralai/Mistral-7B-Instruct-v0.2"
        model_string = "mistralai/Mixtral-8x7B-Instruct-v0.1"
        # model_string = "01-ai/Yi-34B-Chat"
        # model_string = "HuggingFaceH4/zephyr-7b-alpha"
        # model_string = "openchat/openchat-3.5-0106"
        self.chat = [
            {
                "role": "user",
                "content": therapist_system_prompt
            },
            {
                "role": "assistant",
                "content": therapist_system_fpv
            }
        ]
        self.llm = HuggingFaceHub(
            repo_id=model_string, 
            model_kwargs={
                "temperature": 0.5, "max_length": 64, "max_new_tokens": 512
            }
        )
        self.tokeniser = AutoTokenizer.from_pretrained(model_string)
        vector_store = VectorStore()
        db = vector_store.get_db()
        self.retriever = db.as_retriever(
            search_type="similarity_score_threshold", 
            search_kwargs={"score_threshold": 0.3}
        )

    def __append_documents_to_instruction(self, message):
        instruction_with_documents = f'''Reply to the following text message, making use of the documents provided below if they are relevant. Do not use those documents and do not mention them if you deem that they do not contain any relevant information. Do not mention the id of the documents. If a document is relevant, add the source of the information by adding a link to the exact url that was used at the end of your reply. For that use the 'source' field of the relevant document.
        
        Do not directly mention the articles like according to etc, or sound overly scientific. You may use the documents to improve and inform your reply.
        Message: {message}
        
        '''

        # docs = FIXME How to get documents from the instruction?
        docs = self.retriever.get_relevant_documents(message)

        if len(docs) == 0:  # If there are no relevant documents, just return the original instruction
            return message

        instruction_with_documents += "Documents:\n"

        for i, doc in enumerate(docs):
            instruction_with_documents += f'''- {doc.metadata}
                Content: {doc.page_content}
            '''
        return instruction_with_documents

    def get_reply(self, instruction):
        instruction_with_context = self.__append_documents_to_instruction(
            instruction)
        self.chat.append({"role": "user", "content": instruction_with_context})

        prompt = self.tokeniser.apply_chat_template(self.chat, tokenize=False)
        reply = self.llm.invoke(prompt)
        self.chat.append({"role": "assistant", "content": reply})
        return reply
