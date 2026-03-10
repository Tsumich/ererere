from datetime import datetime

base_date = datetime(2026, 2, 23) #четная неделя
EVEN_WEEK = 1

def get_week_parity():
    today = datetime.now()
    
    days_diff = (today - base_date).days
    
    week_number = days_diff // 7
    
    if week_number % 2 == 0:
        return 1
    else:
        return 0

def get_today_schedule():
    EVEN_WEEK = get_week_parity()
    today = datetime.now()
    weekday = today.weekday()

    if weekday >= 5:
        return None
    subject_list = []
    if(EVEN_WEEK):
        subject_list = even_week[weekday]
    else:
        subject_list = odd_week[weekday]
    message = "Неделя: "

    message += "четная" if EVEN_WEEK==1 else "нечетная" 
    message += '\n\nРасписание: \n\n'

    for i in range(len(subject_list)):
        if subject_list[i] != "-":
            message += raspisanie_zvonkov[i] + ":   " +  subject_list[i] + '\n'
    return message
    

raspisanie_zvonkov = ['8:00 - 9:35', '9:45 - 11:20', '11:45 - 13:20', '13:30 - 15:05', '15:30 - 17:05']
#---------------------
# Четная неделя
#---------------------

even_Monday = ["Дискретная математика (л), Гутова С.Г. 1 блочная",
               "Обучение служением Егорова Н.М. 5406",
               "Математический анализ (л) Жалнина А.А. 2226",
               "Компьютерные сети (л) Карабцев С.Н. 2226"]

even_Tuesday = ["Электротехника", "Дискретная математика", 
                "Электротехника", "Электротехника"]

even_Wednesday = ["-", "-", "Иностранный язык", "Языки практика"]

even_Thursday = ["-", "Языки программирования (л)", "История (л)"]

even_Friday = ["-", "ФИз-ра", "Матанализ", 
               "История России", "Компьютерные сети Карабцев"]

#---------------------
# Нечетная неделя
#---------------------

odd_Monday = ["Операционные системы",
               "Обучение служением Егорова Н.М. 5406",
               "Математический анализ (л) Жалнина А.А. 2226"]

odd_Tuesday = ["Операционные системы", "Дискретная математика", 
                "Ин-яз"]

odd_Wednesday = ["Физ-ра", "Операционные системы", "Иностранный язык", "Языки практика"]

odd_Thursday = ["-", "Языки программирования (л)", "История (л)"]

odd_Friday = ["-", "ФИз-ра", "Матанализ", 
               "История России", "Компьютерные сети Карабцев"]

even_week = [even_Monday, even_Tuesday, even_Wednesday, even_Thursday, even_Friday]
odd_week = [odd_Monday, odd_Tuesday, odd_Wednesday, odd_Thursday, odd_Friday]
