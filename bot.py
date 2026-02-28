import threading
import time
from flask import Flask
import telebot
import schedule
import os
from dotenv import load_dotenv

from scheduler import get_week_parity, get_today_schedule
from ai_needs import get_politician_response

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
print("🌐 Веб-сервер запущен на порту", os.environ.get('PORT', 8080))


bot = telebot.TeleBot(BOT_TOKEN)

elite = [2074919463, 136817688, 1087968824, 534645597, 777000]
chats = [1002610474557, CHANEL_CHAT_ID]
# 1002610474557
def send_every_day_schedule():
    print("рассылка расписания")
    message = get_today_schedule()
    if message != None:
        bot.send_message(chat_id = CHAT_ID, text=message)

@bot.message_handler(func=lambda message: True, content_types=['photo','text']) 
def handle_comment(message):
    #if message.chat.id == CHANEL_CHAT_ID:
    if message.is_automatic_forward and message.forward_origin:
        print(f"{message.from_user.first_name}: {message.text}")
        
        bot.send_chat_action(message.chat.id, 'typing')
        #print(message)
        reply = get_politician_response(message.caption or message.text)
        
        if not reply or len(reply.strip()) == 0:
            reply = "Всё, я устала. Пока."
        
        bot.reply_to(message, reply)
        #print(f"Бот: {reply}") 136817688 - канал , 1087968824 - чат
    elif message.chat.id == CHAT_ID:
        send_every_day_schedule()
    else:
        print(f"Игнорирую сообщение от {message.from_user.id}")

print("Бот запущен! Жду комментарии...")

def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)

threading.Thread(target=run_schedule, daemon=True).start()

schedule.every().day.at("06:00").do(send_every_day_schedule)

while True:
    try:
        bot.infinity_polling(timeout=10, long_polling_timeout=5)
    except Exception as e:
        print(f"Ошибка: {e}")
        time.sleep(5)