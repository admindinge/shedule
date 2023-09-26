from datetime import datetime, timedelta

def parse_time(time_str):
    try:
        parsed_time = datetime.strptime(time_str, '%H:%M')
        if parsed_time.hour < 8 or parsed_time.hour > 15:
            raise ValueError("Час начала урока должен быть от 8 до 15.")
        if parsed_time.minute < 0 or parsed_time.minute > 59:
            raise ValueError("Минуты начала урока должны быть от 0 до 59.")
        return parsed_time
    except ValueError as e:
        print("Ошибка! ", str(e))
        return None

def generate_schedule(schedule_params):
    lessons_count = int(schedule_params['количество уроков'])
    lesson_duration = int(schedule_params['продолжительность урока в минутах'])
    break_duration = int(schedule_params['продолжительность перемена в минутах'])
    big_break_count = int(schedule_params['после которого урока большая переменная'])
    big_break_duration = int(schedule_params['продолжительность большой перемены'])

    start_time = parse_time(schedule_params['начало занятий'])
    lessons_begin_bell_time = start_time - timedelta(minutes=int(schedule_params['время звонка перед началом урока']))
    bell_time_between_lessons = timedelta(minutes=int(schedule_params['время звонка между уроками']))
    bell_time_after_break = timedelta(minutes=int(schedule_params['время звонка после перемены']))
    
    if start_time is None:
        return []

    schedule = []
    current_time = start_time

    for lesson_num in range(lessons_count):
        

        # Урок начинается
        schedule.append(f'{current_time.strftime("%M %H")} * *  1-5 /usr/sbin/mpg123')
        schedule.append( f'{(current_time + timedelta(minutes=lesson_duration)).strftime("%M %H")} * *  1-5 /usr/sbin/mpg123')

        current_time += timedelta(minutes=lesson_duration)

        

        if (lesson_num + 1) % big_break_count == 0 and lesson_num < lessons_count - 1:
            # Большая перемена начинается
            current_time += timedelta(minutes=big_break_duration)

        
        else:    
            current_time += timedelta(minutes=break_duration)

        

    return schedule

# Параметры расписания на основе ваших данных
schedule_params = {
    'количество уроков': '7',
    'начало занятий': '9:00',
    'продолжительность урока в минутах': '45',
    'продолжительность перемена в минутах': '5',
    'продолжительность большой перемены': '10',
    'после которого урока большая переменная': '3',
    'время звонка перед началом урока': '10',
    'время звонка между уроками': '5',
    'время звонка после перемены': '10'
}

# Генерация расписания
schedule = generate_schedule(schedule_params)

# Вывод расписания
print("Сгенерированное расписание:")
for item in schedule:
    print(item)
