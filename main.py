import telebot
import instaloader
import os
import re
from flask import Flask
from threading import Thread

# Bot sozlamalari
TOKEN = '8618465943:AAGBQ9tKWAbcaG8J1taZb1TEKpiykldi28M'
bot = telebot.TeleBot(TOKEN)
L = instaloader.Instaloader()

app = Flask('')
@app.route('/')
def home(): return "Bot 24/7 faol!"

def run():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Salom! Instagram linkini yuboring, men matnini olib beraman.")

@bot.message_handler(func=lambda message: True)
def get_info(message):
    if 'instagram.com' not in message.text:
        return

    try:
        msg = bot.send_message(message.chat.id, "Yuklanmoqda... 🔎")
        link = message.text.strip()
        
        # Shortcode'ni har qanday linkdan qidirib topish
        match = re.search(r'/(?:reels|reel|p)/([a-zA-Z0-9_-]+)', link)
        if match:
            shortcode = match.group(1)
            post = instaloader.Post.from_shortcode(L.context, shortcode)
            caption = post.caption if post.caption else "Matn mavjud emas."
            bot.edit_message_text(f"✅ **Natija:**\n\n{caption}", message.chat.id, msg.message_id)
        else:
            bot.edit_message_text("Xato! Bu Instagram Reels yoki Post linki emas.", message.chat.id, msg.message_id)
            
    except Exception as e:
        bot.send_message(message.chat.id, "Xatolik! Instagram ma'lumot bermadi. Link noto'g'ri bo'lishi mumkin.")

if __name__ == "__main__":
    Thread(target=run).start()
    bot.infinity_polling()
    
