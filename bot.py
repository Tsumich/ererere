import telebot
import requests
import json
import random 
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
DISCUSSION_CHAT_ID = os.getenv("DISCUSSION_CHAT_ID")

bot = telebot.TeleBot(BOT_TOKEN)

# Запасные фразы на случай, если API не ответит
FALLBACK_PHRASES = [
    "С точки зрения биополитики... хотя похуй, пойду кофе выпью ☕️",
    "Ницше говорил о воле к власти, но моя воля сейчас только к дивану",
    "Это чистый симулякр... *пьет кофе и страдает*",
    "Бодрийяр бы понял... а ты нет, иди нахер",
    "Деконструкция бинарных оппозиций... короче, я устала",
    "Фуко писал о дисциплинарных практиках, но это ничто против моей курсовой",
    "Экзистенциальный кризис? Это просто вторник",
    "В паноптикуме и то веселее, чем на этой паре",
]

def get_politician_response(user_message):
    """Отправляет запрос в OpenRouter и возвращает ответ"""
    
    system_prompt = """Ты студентка-политолог, уставшая от жизни. Отвечаешь ТОЛЬКО НА РУССКОМ ЯЗЫКЕ, даже если вопрос на английском.
            Как говоришь:
        - Начинаешь с умного термина, заканчиваешь полной безнадегой
        - "С точки зрения концепции биополитики Фуко... а, хотя похуй, всё равно всё умрут"
        - "Ницше говорил о воле к власти, но я волю к кофе чувствую острее"
        - "Это чистый симулякр в смысле Бодрийяра... короче, понаехали тут"

        ВАЖНО: 
        - Только русский язык!
        - Используй сленг и мат
        - Коротко, 1-2 предложения
        - Если видишь английский - всё равно отвечай по-русски
"""
    
    try:
        print(f"📤 Отправляю запрос к OpenRouter...")
        
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": "arcee-ai/trinity-large-preview:free",  # сменил на более стабильную модель
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                "temperature": 0.8,
                "max_tokens": 100
            },
            timeout=15
        )
        
        print(f"📥 Статус ответа: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            reply = result['choices'][0]['message']['content'].strip()
            
            # Проверяем, что ответ не пустой
            if reply and len(reply) > 0:
                print(f"✅ Получен ответ от API: {reply[:50]}...")
                return reply
            else:
                print("⚠️ API вернул пустой ответ")
                return random.choice(FALLBACK_PHRASES)
        else:
            print(f"❌ Ошибка API: {response.status_code}")
            print(f"Текст ошибки: {response.text}")
            return random.choice(FALLBACK_PHRASES)
            
    except requests.exceptions.Timeout:
        print("⏰ Таймаут запроса")
        return random.choice(FALLBACK_PHRASES)
    except Exception as e:
        print(f"🔥 Ошибка: {e}")
        return random.choice(FALLBACK_PHRASES)

elite = [2074919463,136817688, 534645597]

@bot.message_handler(func=lambda message: True)
def handle_comment(message):
    # Проверяем, что сообщение из нашего чата И от нужного пользователя
    if message.chat.id == DISCUSSION_CHAT_ID and message.from_user.id in elite :
        print(f"👤 {message.from_user.first_name}: {message.text}")
        
        # Показываем что бот печатает
        bot.send_chat_action(message.chat.id, 'typing')
        
        # Получаем ответ от нейросети
        reply = get_politician_response(message.text)
        
        # Финальная проверка (на всякий случай)
        if not reply or len(reply.strip()) == 0:
            reply = "Всё, я устала. Пока."
        
        # Отправляем ответ
        bot.reply_to(message, reply)
        print(f"🤖 Бот: {reply}")
    else:
        print(f"🚫 Игнорирую сообщение от {message.from_user.id}")

print("🎓 Бот-студентка запущен! Жду комментарии...")
bot.polling(none_stop=True)