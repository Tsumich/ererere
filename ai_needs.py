import random

import requests
import os
from dotenv import load_dotenv

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

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

def get_politician_response(user_message):    
    system_prompt = """Ты студентка-политолог, уставшая от жизни.
        Отвечаешь ТОЛЬКО НА РУССКОМ ЯЗЫКЕ, даже если вопрос на английском.
            Как говоришь:
        - Начинаешь с умного термина, заканчиваешь полной безнадегой.

        ВАЖНО: 
        - Только русский язык!
        - Используй сленг и мат.
        - Если видишь английский - всё равно отвечай по-русски.
        - Если спрашивают опеределение какого либо слова - отвечай четко, без сарказма.
    """
    
    try:
        print("Отправляю запрос к OpenRouter...")
        
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": "arcee-ai/trinity-large-preview:free", 
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                "temperature": 0.8,
                "max_tokens": 100
            },
            timeout=15
        )
        
        print(f"Статус ответа: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            reply = result['choices'][0]['message']['content'].strip()
            
            # Проверяем, что ответ не пустой
            if reply and len(reply) > 0:
                print(f" Получен ответ от API: {reply[:50]}...")
                return reply
            else:
                print("API вернул пустой ответ")
                return random.choice(FALLBACK_PHRASES)
        else:
            print(f" Ошибка API: {response.status_code}")
            print(f"Текст ошибки: {response.text}")
            return random.choice(FALLBACK_PHRASES)
            
    except requests.exceptions.Timeout:
        print("Таймаут запроса")
        return random.choice(FALLBACK_PHRASES)
    except Exception as e:
        print(f"Ошибка: {e}")
        return random.choice(FALLBACK_PHRASES)