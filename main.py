import telebot
import os
from flask import Flask
from threading import Thread

# 1. Telegram Bot Tokeningizni yozing
TOKEN = '8618465943:AAGBQ9tKWAbcaG8J1taZb1TEKpiykldi28M'
bot = telebot.TeleBot(TOKEN)

# 2. Botingizni "tirik" saqlash uchun veb-server
app = Flask('')

@app.route('/')
def home():
    return "Bot tirik va ishlayapti!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# 3. Botingizning asosiy funksiyalari (Hashtag va Caption qismi)
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Salom! Instagram link yuboring, men caption va hashtaglarni olib beraman.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    # Bu yerga avvalgi yozgan Instagram skriptingizni qo'shamiz
    if "instagram.com" in message.text:
        bot.reply_to(message, "Xozir ma'lumotlarni yuklayapman...")
        # Instagramdan ma'lumot olish kodi shu yerda bo'ladi
    else:
        bot.reply_to(message, "Iltimos, faqat Instagram link yuboring.")

# Botni ishga tushirish
if __name__ == "__main__":
    keep_alive() # Veb-serverni ishga tushiradi
    print("Bot yoqildi...")
    bot.infinity_polling() # Botni to'xtovsiz ishlashga majbur qiladi
