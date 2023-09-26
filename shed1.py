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

def get_input_or_default(prompt, default):
    user_input = input(f"{prompt} ({default}): ").strip()
    return default if user_input == "" else user_input

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
        # Звонок перед началом урока
        schedule.append(f'Звонок: {lessons_begin_bell_time.strftime("%H:%M")} перед началом урока {lesson_num + 1}')

        # Урок начинается
        schedule.append(f'Урок {lesson_num + 1}: начало - {current_time.strftime("%H:%M")}, '
                        f'конец (звонок) - {(current_time + timedelta(minutes=lesson_duration)).strftime("%H:%M")}')

        current_time += timedelta(minutes=lesson_duration)

        # Звонок после урока
        schedule.append(f'Звонок: {current_time.strftime("%H:%M")} после урока {lesson_num + 1}')

        if (lesson_num + 1) % big_break_count == 0 and lesson_num < lessons_count - 1:
            # Большая перемена начинается
            current_time += timedelta(minutes=big_break_duration)

            # Звонок после перемены
            schedule.append(f'Звонок: {current_time.strftime("%H:%M")} после большой перемены')

        # Учет продолжительности перемен
        current_time += timedelta(minutes=break_duration)

        if lesson_num < lessons_count - 1:
            # Звонок перед следующим уроком
            current_time += bell_time_between_lessons
            schedule.append(f'Звонок: {current_time.strftime("%H:%M")} перед следующим уроком {lesson_num + 2}')

    return schedule

# Параметры расписания на основе ваших данных
schedule_params = {
    'количество уроков': get_input_or_default('Введите количество уроков', '7'),
    'начало занятий': get_input_or_default('Введите время начала занятий (чч:мм)', '9:00'),
    'продолжительность урока в минутах': get_input_or_default('Введите продолжительность урока в минутах', '45'),
    'продолжительность перемена в минутах': get_input_or_default('Введите продолжительность перемены в минутах', '5'),
    'продолжительность большой перемены': get_input_or_default('Введите продолжительность большой переменной в минутах', '10'),
    'после которого урока большая переменная': get_input_or_default('Введите после какого урока идет большая перемена', '3'),
    'время звонка перед началом урока': get_input_or_default('Введите время звонка перед началом урока в минутах', '10'),
    'время звонка между уроками': get_input_or_default('Введите время звонка между уроками в минутах', '5'),
    'время звонка после перемены': get_input_or_default('Введите время звонка после перемены в минутах', '10')
}

# Генерация расписания
schedule = generate_schedule(schedule_params)

# Вывод расписания
print("Сгенерированное расписание:")
for item in schedule:
    print(item)
