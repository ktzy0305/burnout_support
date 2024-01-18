from langchain_community.llms import HuggingFaceHub
from transformer import AutoTokenizer

class LLM:
    def __init__(self):
        model_string = "mistralai/Mistral-7B-Instruct-v0.2"
        self.chat = []
        self.llm = HuggingFaceHub(repo_id=model_string, model_kwargs={"temperature": 0.5, "max_length":64,"max_new_tokens":512})

    # def __append_prompt_to_instructions(self):


    def get_reply(self, instruction):
        self.chat.append({"role" : "user", "content" : instruction})

        reply = self.llm.invoke(instruction)
        self.chat.append({"role" : "assistant", "content" : reply})
        return reply
    