import threading
import time
from flask import Flask
import telebot
import schedule
import os
from dotenv import load_dotenv

from scheduler import get_today_schedule
from ai_needs import get_politician_response
from kemsu import request_to_kemsu

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
CHANEL_CHAT_ID = int(os.getenv("DISCUSSION_CHAT_ID"))
CHAT_ID = -1003673299188

app = Flask(__name__)

@app.route('/ping')
def home():
    return "pong"

def run_flask():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)

flask_thread = threading.Thread(target=run_flask, daemon=True)
flask_thread.start()
print("Веб-сервер запущен на порту", os.environ.get('PORT', 8080))

bot = telebot.TeleBot(BOT_TOKEN)

def send_every_day_schedule():
    print("рассылка расписания")
    message = get_today_schedule()
    if message != None:
        bot.send_message(chat_id = CHAT_ID, text=message)

def send_subject_stat():
    array = request_to_kemsu()
    message = ""
    for i in range(len(array)):
        message += array[i]
    bot.send_message(chat_id = CHAT_ID, text=message)

@bot.message_handler(func=lambda message: True, content_types=['photo','text']) 
def handle_comment(message):
    if message.is_automatic_forward and message.forward_origin:
        print(f"{message.from_user.first_name}: {message.text}")
        text_to_respond = message.caption or message.text
        if not text_to_respond or len(text_to_respond.strip()) == 0:
            print("Пустая подпись - игнорирую")
            return 
        bot.send_chat_action(message.chat.id, 'typing')
        reply = get_politician_response(message.caption or message.text)
        
        if not reply or len(reply.strip()) == 0:
            reply = "Всё, я устала. Пока."
        
        bot.reply_to(message, reply)
    elif message.chat.id == CHAT_ID and "расписание" in message.text:
        send_every_day_schedule()
    elif message.chat.id == CHAT_ID and "оценки" in message.text:
        send_subject_stat()
    else:
        print(f"Игнорирую сообщение от {message.from_user.id}")

print("Бот запущен! Жду комментарии...")

def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)

threading.Thread(target=run_schedule, daemon=True).start()

schedule.every().day.at("00:00").do(send_every_day_schedule)

while True:
    try:
        bot.infinity_polling(timeout=10, long_polling_timeout=5)
    except Exception as e:
        print(f"Ошибка: {e}")
        time.sleep(5)