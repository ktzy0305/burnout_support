# based on https://hckr.cc/hnr2024-ahrefs

import os
import telebot
import requests
from langchain_community.llms import HuggingFaceHub

from bot.llm import LLM


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
    llm = LLM()
except Exception as e:
    print(f"{e}")


def init_bot():
    @bot.message_handler(commands=['start'])
    def on_start(message):
        bot.send_message(message.chat.id, "Waking up! Give me a bit . . .")

    @bot.message_handler(commands=['newchat'])
    def on_new_chat(message):
        llm.chat = []
        bot.reply_to(message, "Hey there, welcome I am Samantha. How are you feeling right now?")

    @bot.message_handler(func=lambda msg: True)
    def on_message(message):
        print(f"Message received! {message}")
        # reply = ??? FIX ME
        reply = llm.get_reply(message.text)
        bot.reply_to(message, reply)

    return bot

bot = init_bot()
bot.infinity_poling()

