import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import requests
from flask import Flask
from threading import Thread
import os

API_TOKEN = '8618465943:AAGBQ9tKWAbcaG8J1taZb1TEKpiykldi28M'
logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

app = Flask('')
@app.route('/')
def home():
    return "Bot yoniq!"

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

@dp.message_handler(content_types=['web_app_data'])
async def handle_webapp_data(message: types.Message):
    url = message.web_app_data.data
    await message.answer("🔍 Qidirilmoqda...")
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(f"{url.split('?')[0].rstrip('/')}/?__a=1&__d=dis", headers=headers, timeout=10)
        if response.status_code == 200:
            caption = response.json()['items'][0]['caption']['text']
            await message.answer(f"✅ **Caption:**\n\n`{caption}`", parse_mode="Markdown")
        else:
            await message.answer("❌ Instagram ma'lumot bermadi.")
    except Exception:
        await message.answer("❌ Xatolik yuz berdi.")

if __name__ == '__main__':
    Thread(target=run).start()
    executor.start_polling(dp, skip_updates=True)
          
