import telebot
import instaloader
import os
from flask import Flask
from threading import Thread

# Bot sozlamalari
TOKEN = '8618465943:AAGBQ9tKWAbcaG8J1taZb1TEKpiykldi28M'
bot = telebot.TeleBot(TOKEN)
L = instaloader.Instaloader()

app = Flask('')
@app.route('/')
def home(): return "Bot faol!"

def run():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Salom! Instagram Reels yoki Post linkini yuboring, men captionni olib beraman.")

@bot.message_handler(func=lambda message: 'instagram.com' in message.text)
def get_info(message):
    try:
        msg = bot.send_message(message.chat.id, "Ma'lumot qidirilmoqda... 🔎")
        link = message.text.strip()
        
        # Linkdan shortcode'ni aniqroq ajratib olish
        if '/reels/' in link or '/reel/' in link:
            shortcode = link.split('/reel/')[1].split('/')[0] if '/reel/' in link else link.split('/reels/')[1].split('/')[0]
        elif '/p/' in link:
            shortcode = link.split('/p/')[1].split('/')[0]
        else:
            bot.edit_message_text("Kechirasiz, linkni taniy olmadim. Faqat Reels yoki Post linkini yuboring.", message.chat.id, msg.message_id)
            return

        # Shortcode'dagi ortiqcha belgilarni tozalash (?igsh= kabi)
        shortcode = shortcode.split('?')[0].split('/')[0]

        post = instaloader.Post.from_shortcode(L.context, shortcode)
        caption = post.caption if post.caption else "Caption mavjud emas."
        
        bot.edit_message_text(f"✅ **Natija:**\n\n{caption}", message.chat.id, msg.message_id)
    except Exception as e:
        print(f"Xato: {e}")
        bot.edit_message_text("Xatolik! Instagram ma'lumot bermadi. Linkni tekshiring yoki birozdan so'ng urinib ko'ring.", message.chat.id, msg.message_id)

if __name__ == "__main__":
    Thread(target=run).start()
    bot.infinity_polling()
    
