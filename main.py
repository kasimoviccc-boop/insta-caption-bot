import telebot
import instaloader
import os
from flask import Flask
from threading import Thread

# Bot sozlamalari
TOKEN = '8618465943:AAGBQ9tKWAbcaG8J1taZb1TEKpiykldi28M'
bot = telebot.TeleBot(TOKEN)
L = instaloader.Instaloader()

# Render uchun oddiy server
app = Flask('')
@app.route('/')
def home(): return "Bot faol!"

def run():
    # Render avtomatik port beradi, bo'lmasa 10000 ishlatamiz
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

@bot.message_handler(commands=['start'])
def start(message):
    # reply_to o'rniga oddiy send_message ishlatamiz (xato bermasligi uchun)
    bot.send_message(message.chat.id, "Salom! Instagram Reels yoki Post linkini yuboring.")

@bot.message_handler(func=lambda message: 'instagram.com' in message.text)
def get_info(message):
    try:
        msg = bot.send_message(message.chat.id, "Ma'lumot qidirilmoqda... 🔎")
        url_parts = message.text.strip().split('/')
        
        # Shortcode ajratish
        if 'reels' in url_parts:
            shortcode = url_parts[url_parts.index('reels') + 1]
        elif 'p' in url_parts:
            shortcode = url_parts[url_parts.index('p') + 1]
        else:
            bot.edit_message_text("Faqat Reels yoki Post linkini yuboring.", message.chat.id, msg.message_id)
            return

        post = instaloader.Post.from_shortcode(L.context, shortcode.split('?')[0])
        caption = post.caption if post.caption else "Caption mavjud emas."
        
        bot.edit_message_text(f"✅ **Natija:**\n\n{caption}", message.chat.id, msg.message_id)
    except Exception as e:
        bot.send_message(message.chat.id, "Xatolik! Instagram ma'lumot bermadi yoki link noto'g'ri.")

if __name__ == "__main__":
    Thread(target=run).start()
    print("Bot ulanmoqda...")
    bot.infinity_polling()
    
