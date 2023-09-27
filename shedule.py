from datetime import datetime, timedelta

def parse_time(time_str):
    try:
        parsed_time = datetime.strptime(time_str, '%H:%M')
        if parsed_time.hour < 8 or parsed_time.hour > 15:
            raise ValueError("გაკვეთილის დაწყების დრო უნდა იყოს  8-დან  15 საათამდე.")
        if parsed_time.minute < 0 or parsed_time.minute > 59:
            raise ValueError("წუთების მაჩვენებელი უნდა იყოს  0-59 დიაპაზონში.")
        return parsed_time
    except ValueError as e:
        print("ᲨᲔᲪᲓᲝᲛᲐ:! ", str(e))
        return None

def get_input_or_default(prompt, default):
    user_input = input(f"{prompt} ({default}): ").strip()
    return default if user_input == "" else user_input

def generate_schedule(schedule_params):
    lessons_count = int(schedule_params['გაკვეთილების რაოდენობა'])
    lesson_duration = int(schedule_params['გაკვეთილის ხანგრძლივობა'])
    break_duration = int(schedule_params['დასვენების ხანგრძლივობა'])
    big_break_count = int(schedule_params['რომელია დიდი დასვენება'])
    big_break_duration = int(schedule_params['დიდი დასვენების ხანგრძლივობა'])

    start_time = parse_time(schedule_params['გაკვეთილების დაწყება'])
    
    
    if start_time is None:
        return []

    schedule = []
    current_time = start_time
    
    run_program_string = '/home/tc/bell.c'

    for lesson_num in range(lessons_count):
        

        # ᲒᲐᲙᲕᲔᲗᲘᲚᲘᲡ ᲓᲐᲬᲧᲔᲑᲐ
        schedule.append(f'# ᲒᲐᲙᲕᲔᲗᲘᲚᲘ {lesson_num} ')
        schedule.append(f'{current_time.strftime("%M %H")} * *  1-5 {run_program_string} in')
        # ᲒᲐᲙᲕᲔᲗᲘᲚᲘᲡ ᲓᲐᲡᲠᲣᲚᲔᲑᲐ
        schedule.append( f'{(current_time + timedelta(minutes=lesson_duration)).strftime("%M %H")} * *  1-5 {run_program_string} out')
        schedule.append(f'')
        current_time += timedelta(minutes=lesson_duration)

        

        if (lesson_num + 1) % big_break_count == 0 and lesson_num < lessons_count - 1:
            # Большая перемена начинается
            current_time += timedelta(minutes=big_break_duration)

        
        else:    
            current_time += timedelta(minutes=break_duration)

        

    return schedule

# Параметры расписания на основе ваших данных
schedule_params = {
    'გაკვეთილების რაოდენობა': get_input_or_default('შეიყვანე გაკვეთილების რაოდენობა', '7'),
    'გაკვეთილების დაწყება': get_input_or_default('შეიყვანე გაკვეთილების დაწყების დრო (ᲡᲡ:ᲬᲬ)', '9:00'),
    'გაკვეთილის ხანგრძლივობა': get_input_or_default('შეიყვანე გაკვეთილის ხანგრძლივობა', '45'),
    'დასვენების ხანგრძლივობა': get_input_or_default('შეიყვანე შესვენების ხანგრძლივობა', '5'),
    'დიდი დასვენების ხანგრძლივობა': get_input_or_default('შეიყვანე დიდი დასვენების ხანგრძლივობა', '10'),
    'რომელია დიდი დასვენება': get_input_or_default('შეიყვანე რომელია დიდი დასვენება', '3')
}

# Генерация расписания
schedule = generate_schedule(schedule_params)

# Вывод расписания
print("ᲒᲐᲙᲕᲔᲗᲘᲚᲔᲑᲘᲡ ᲒᲐᲜᲠᲘᲒᲘ:")
print("")
for item in schedule:
    print(item)
