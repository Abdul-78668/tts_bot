# main.py
from flask import Flask, request
from gtts import gTTS
from io import BytesIO
from langdetect import detect
import re
import telebot
import os

app = Flask(__name__)

# Telegram bot token from environment variable
TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

def smart_detect(text):
    if re.search(r'[\u0900-\u097F]', text):
        return 'hi'
    elif re.search(r'[\u0600-\u06FF]', text):
        return 'ur'
    else:
        try:
            lang = detect(text)
            return lang if lang in ['en', 'hi', 'ur'] else 'en'
        except:
            return 'en'

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "👋 Welcome! Send me any text and I'll reply with audio in that language.")

@bot.message_handler(func=lambda message: True)
def tts_reply(message):
    text = message.text
    lang = smart_detect(text)
    tts = gTTS(text=text, lang=lang)
    voice = BytesIO()
    tts.write_to_fp(voice)
    voice.seek(0)
    bot.send_voice(message.chat.id, voice)

@app.route('/')
def home():
    return "Bot is running", 200

if __name__ == '__main__':
    from threading import Thread

    def run_flask():
        app.run(host='0.0.0.0', port=8080)

    def run_telegram():
        bot.infinity_polling()

    Thread(target=run_flask).start()
    Thread(target=run_telegram).start()
