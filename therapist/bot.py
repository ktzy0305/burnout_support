# based on https://hckr.cc/hnr2024-ahrefs

import numpy as np
import os
import telebot
import requests

from constants import BASE_DIR
from deepface import DeepFace
from langchain_community.llms import HuggingFaceHub
from PIL import Image

# from llm import LLM
import llm


def init_bot(bot, LLM):
    @bot.message_handler(commands=['start'])
    def on_start(message):
        reply = bot.send_message(message.chat.id, "Waking up! Give me a bit . . .")
        # reply.send_message(message.chat.id, "Hi! Happy to see you today, how are you feeling?")
        bot.edit_message_text("Hi! Happy to see you today, how are you feeling?", reply.chat.id, reply.message_id)
        # LLM.chat.append({"role" : "assistant", "content" : "Hey there!"})

    # @bot.message_handler(commands=['newchat'])
    # def on_new_chat(message):
    #     LLM.chat = []
    #     bot.reply_to(message, "Hey there, welcome I am Samantha. How are you feeling right now?")

    @bot.message_handler(func=lambda msg: True)
    def on_message(message):
        print(f"Message received! @{message.from_user.username} [{message.from_user.id}]: {message.text}")
        # reply = ??? FIX ME

        reply = bot.reply_to(message, "Typing . . .")
        llm_reply = LLM.get_reply(message.text)
        bot.edit_message_text(llm_reply, reply.chat.id, reply.message_id)
        # reply.edit_message(reply_message)
        
    @bot.message_handler(content_types=['photo'])
    def on_image(message):
        file_id = message.photo[-1].file_id
        file_info = bot.get_file(file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        # Save the downloaded file to a local file
        user_image_dir = os.path.join(BASE_DIR, 'user_images')
        os.mkdir(user_image_dir)
        local_filename = os.path.join(user_image_dir, 'downloaded_image.jpg')
        with open(local_filename, 'wb') as local_file:
            local_file.write(downloaded_file)
        
        # Start the reply procedure
        reply = bot.reply_to(message, "Typing . . .")
        
        try: 
            # Pass downloaded file to emotion classifier
            face_analysis = DeepFace.analyze(img_path=local_filename)
            
            # Retrieve face analysis results
            if (len(face_analysis) > 1):
                llm_reply = f"{len(face_analysis)} faces detected in your photo. Please send a photo with only a single face."
                # bot.edit_message_text(llm_reply, reply.chat.id, reply.message_id)
                # for count, analysis in enumerate(face_analysis):
                #     age = analysis["age"]
                #     emotion = analysis["dominant_emotion"]
                #     gender = analysis["dominant_gender"]
                #     race = analysis["dominant_race"]
                #     llm_reply += f"\nPerson {count + 1}: You are a {age} {race} {gender} who is feeling {emotion}."
                    
                bot.edit_message_text(llm_reply, reply.chat.id, reply.message_id)
            else:
                age = face_analysis[0]["age"]
                emotion = face_analysis[0]["dominant_emotion"]
                gender = face_analysis[0]["dominant_gender"]
                race = face_analysis[0]["dominant_race"]
                hidden_context = f"""
                    Do not reveal this message below in your reply: 
                    
                    1. The following information is automatically generated from an image the user sent. 
                    2. Use the information given below to assess the user's emotional state and reply accordingly in a supportive manner.
                    
                    Current User Profile:
                    - Race: {race} 
                    - Estimated Age: {age} 
                    - Gender: {gender}
                    - Emotional State: {emotion}.
                    
                    Do not mention that you are an AI or that you are unable to see images / user profiles in any part of the response.
                """
                llm_reply = LLM.get_reply(hidden_context)
                # llm_reply = f"You are a {age} {race} {gender} who is feeling {emotion}."
                bot.edit_message_text(llm_reply, reply.chat.id, reply.message_id)
        except ValueError:
            bot.edit_message_text("Face could not be detected", reply.chat.id, reply.message_id)
        finally:
            # Remove local file after use
            os.remove(local_filename)
            os.rmdir(user_image_dir)
        
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
        print("\x1b[38;5;46mLLM initialised \x1b[0m")
        bot = init_bot(bot, LLM)
        print("\x1b[38;5;46mBot initialised\x1b[0m")
        bot.infinity_polling()
    except Exception as e:
        print(f"{e}")
    

if __name__ == "__main__":
    __main__()