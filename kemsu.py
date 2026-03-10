from bs4 import BeautifulSoup
import fake_useragent
import requests
from dotenv import load_dotenv
import os

load_dotenv()

def request_to_kemsu():
    session = requests.Session()
    user = fake_useragent.UserAgent().random

    auth_url = "https://api2.kemsu.ru/api/auth"

    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Origin': 'https://eios.kemsu.ru',
        'Referer': 'https://eios.kemsu.ru/',
        'User-Agent': user
    }

    payload = {
    "login": os.getenv("KEMSU_USER_LOGIN"),
    "password": os.getenv("KEMSU_USER_PASSWORD"),
    "lifetime": "3m"
    }

    response = session.post(
        auth_url,
        headers=headers,
        json=payload,  
    )

    headers = {
        'Accept': 'ext/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'xiais.kemsu.ru',
        'Referer': 'https://eios.kemsu.ru/',
        'User-Agent': user
    }
    sync_response = session.get('https://xiais.kemsu.ru/dekanat/eios-next-sync/auth.htm', headers=headers)

    cred_data = {
        "login": os.getenv("KEMSU_USER_LOGIN"),
        "password": os.getenv("KEMSU_USER_PASSWORD"),
    }

    headers = {
        'Accept': 'ext/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'xiais.kemsu.ru',
        'Origin': 'https://eios.kemsu.ru',
        'Referer': 'https://xiais.kemsu.ru/dekanat/eios-next-sync/auth.htm',
        'User-Agent': user
    }

    session.post('https://xiais.kemsu.ru/dekanat/restricted/index_next.htm', headers=headers, data=cred_data)
    session.get('https://xiais.kemsu.ru/dekanat/restricted/', headers=headers)

    #выполняется автоматически после авторизации в нетворк
    #person_info = session.get('https://api2.kemsu.ru/api/person-area-user-info', headers=headers)
    #print(person_info.text)

    headers = {
        'Accept': 'ext/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'eios.kemsu.ru',
        'Referer': 'https://xiais.kemsu.ru/',
        'User-Agent': user
    }
    session.get('https://eios.kemsu.ru/a/eios', headers=headers)


    data = response.json()
    userId = data['userInfo']['id']
    print("Сбор данных о пользовале: ", userId)

    subject_link = "https://xiais.kemsu.ru/proc/stud/index.shtm"

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Content-Type': 'application/x-www-form-urlencoded',  
        'Origin': 'https://xiais.kemsu.ru',  
        'Referer': 'https://xiais.kemsu.ru/proc/stud/index.shtm',  
        'Sec-Ch-Ua': 'Chromium";v="142", "YaBrowser";v="25.12", "Not_A Brand";v="99", "Yowser";v="2.5',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Sec-Fetch-Dest': 'document',
        'Host': 'xiais.kemsu.ru',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': user,
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-User': '?1'
    }

    response = session.post(subject_link, headers=headers, data = 'studyYear=2025-2026')
    if response.status_code != 200:
        error_messages = {
            401: "Авторизация протухла, надо перезайти",
            403: "Доступа нет, видимо кемсу меня забанил",
            404: "Страница с оценками не найдена",
            500: "У кемсу сервер упал, ну бывает",
            502: "Шлюз кемсу сломался, перегрузка видимо",
            503: "Кемсу лежит, обслуживание"
        }
        return error_messages.get(response.status_code, f"Ошибка {response.status_code}, сам хз что случилось")

    soup = BeautifulSoup(response.text, 'html.parser')

    tables = soup.find_all('table', recursive=True)
    subject_table = tables[3].find_all('table', recursive=True)[0]
    rows = subject_table.find_all('tr', recursive=True)  

    message = ""    

    for i in range(1, len(rows)):
        subject_title = rows[i].find_all('td', recursive=True)[1].text
        amout = rows[i].find_all('td', recursive=True)[7].text
        
        subject_title = subject_title.strip()
        amout = amout.strip()
            
        message += subject_title +" : " + amout +"\n\n"
    return message


