# based on https://hckr.cc/hnr2024-ahrefs

import os
import telebot
import requests
from langchain_community.llms import HuggingFaceHub

# from llm import LLM
import llm


def init_bot(bot, LLM):
    @bot.message_handler(commands=['start'])
    def on_start(message):
        bot.send_message(message.chat.id, "Waking up! Give me a bit . . .")
        bot.send_message(message.chat.id, "Hey there! ")
        LLM.chat.append({"role" : "assistant", "content" : "Hey there!"})

    # @bot.message_handler(commands=['newchat'])
    # def on_new_chat(message):
    #     LLM.chat = []
    #     bot.reply_to(message, "Hey there, welcome I am Samantha. How are you feeling right now?")

    @bot.message_handler(func=lambda msg: True)
    def on_message(message):
        print(f"Message received! @{message.from_user.username} [{message.from_user.id}]: {message.text}")
        # reply = ??? FIX ME
        reply = LLM.get_reply(message.text)
        bot.reply_to(message, reply)

    return bot


def __main__():
    try:
        # telegram_bot_token = 
        print("Getting telegram_bot_token from os.environ")
        TELEGRAM_API_KEY = os.environ["telegram_bot_token"]
        print("Getting telegram_bot_token from os.environ")
        os.environ["HUGGINGFACEHUB_API_TOKEN"]
        bot = telebot.TeleBot(TELEGRAM_API_KEY)
        bot.get_me()
    except Exception as e:
        # unknown error
        print(f"Error: {e}")
        raise e

    print("Initialising LLM .  .   .")
    try:
        LLM = llm.LLM()
        bot = init_bot(bot, LLM)
        bot.infinity_polling()
    except Exception as e:
        print(f"{e}")
    

if __name__ == "__main__":
    __main__()