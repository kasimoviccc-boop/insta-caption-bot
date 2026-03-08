import telebot
import instaloader
import os
import re
import time
from flask import Flask
from threading import Thread

# 1. Yangi Bot Tokeningiz
TOKEN = '8618465943:AAHvDczmAX3Nyr3-xAZp2T0qs-YoRzCqUAQ'
bot = telebot.TeleBot(TOKEN)
L = instaloader.Instaloader()

# 2. Render uchun server
app = Flask('')
@app.route('/')
def home(): return "Bot 24/7 faol va yangi token bilan ishlamoqda!"

def run_server():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# 3. Bot buyruqlari
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Salom! Men yangi token bilan ishga tushdim 🚀. Instagram Reels yoki Post linkini yuboring.")

@bot.message_handler(func=lambda message: True)
def get_info(message):
    if 'instagram.com' not in message.text:
        return

    try:
        msg = bot.send_message(message.chat.id, "Yuklanmoqda... 🔎")
        link = message.text.strip()
        
        # Har qanday linkdan shortcode'ni
        
