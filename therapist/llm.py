from langchain_community.llms import HuggingFaceHub
from transformers import AutoTokenizer
from prompts import therapist_system_fpv, therapist_system_prompt

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
        self.llm = HuggingFaceHub(repo_id=model_string, model_kwargs={"temperature": 0.5, "max_length":64,"max_new_tokens":512})
        self.tokeniser = AutoTokenizer.from_pretrained(model_string)

    # def __append_prompt_to_instructions(self):


    def get_reply(self, instruction):
        self.chat.append({"role" : "user", "content" : instruction})
        
        prompt = self.tokeniser.apply_chat_template(self.chat, tokenize=False)
        reply = self.llm.invoke(prompt)
        self.chat.append({"role" : "assistant", "content" : reply})
        return reply
    