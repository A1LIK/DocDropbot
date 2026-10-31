import os
import telebot
from flask import Flask, request

# Твой токен бота от BotFather
TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN, threaded=False)

app = Flask(__name__)


@bot.message_handler(commands=['start'])
def send_welcome(message):
  bot.reply_to(
      message,
      'Привет! Я твой карманный бот-утилита.\n'
      'Здесь можно конвертировать файлы, сжимать их и делать QR-коды из ссылок!\n\n'
      'Чтобы разблокировать все функции, пригласи друга по своей ссылке: '
      f'https://t.me/{(bot.get_me()).username}?start={message.from_user.id}',
  )


# Обработка ссылок для генерации QR-кода
@bot.message_handler(func=lambda message: message.text and message.text.startswith('http'))
def generate_qr(message):
  url = message.text.strip()
  # Используем бесплатный публичный API для генерации QR-кода в виде картинки
  qr_api_url = (
      f'https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={url}'
  )

  bot.send_photo(
      message.chat.id,
      qr_api_url,
      caption=(
          'Вот твой QR-код! 📲\nСоздано в боте [Твое Название]'
      ),
  )


# Вебхук-эндпоинт для Vercel
@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
  json_string = request.get_data().decode('utf-8')
  update = telebot.types.Update.de_json(json_string)
  bot.process_new_updates([update])
  return '!', 200


@app.route('/')
def index():
  return 'Bot is running on Vercel!', 200
