import telebot
import instaloader
import os
import re
import time
from flask import Flask
from threading import Thread

# 1. Bot sozlamalari (Yangi token bilan)
TOKEN = '8618465943:AAHvDczmAX3Nyr3-xAZp2T0qs-YoRzCqUAQ'
bot = telebot.TeleBot(TOKEN)
L = instaloader.Instaloader()

# 2. Render serveri
app = Flask('')
@app.route('/')
def home():
    return "Bot faol va yangi token bilan ishlamoqda!"

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
        
        # Shortcode'ni qidirib topish
        match = re.search(r'/(?:reels|reel|p)/([a-zA-Z0-9_-]+)', link)
        if match:
            shortcode = match.group(1)
            post = instaloader.Post.from_shortcode(L.context, shortcode)
            caption = post.caption if post.caption else "Matn mavjud emas."
            bot.edit_message_text(f"✅ **Natija:**\n\n{caption}", message.chat.id, msg.message_id)
        else:
            bot.edit_message_text("Xato! Bu Instagram Reels yoki Post linki emas.", message.chat.id, msg.message_id)
            
    except Exception as e:
        print(f"Xato: {e}")
        bot.send_message(message.chat.id, "Xatolik! Instagram ma'lumot bermadi. Profil yopiq bo'lishi mumkin.")

# 4. Ishga tushirish
if __name__ == "__main__":
    # Serverni alohida oqimda yurgizish
    server_thread = Thread(target=run_server)
    server_thread.start()
    
    print("Bot ulanmoqda...")
    while True:
        try:
            bot.polling(none_stop=True, interval=0, timeout=20)
        except Exception as e:
            print(f"Polling xatosi: {e}")
            time.sleep(5)
            
