from datetime import datetime, timedelta

class SchoolScheduleError(Exception):
    pass

class InvalidSchoolCodeError(SchoolScheduleError):
    def __init__(self, code):
        self.code = code
        self.message = f"არაკორექტული სკოლის კოდი: {code}"
        super().__init__(self.message)

class ScheduleGenerationError(SchoolScheduleError):
    def __init__(self, message):
        self.message = f"განრიგის გენერაციის შეცდომა: {message}"
        super().__init__(self.message)

def parse_time(time_str):
    
        parsed_time = datetime.strptime(time_str, '%H:%M')
        if parsed_time.hour < 8 or parsed_time.hour > 15:
            raise ScheduleGenerationError("გაკვეთილის დაწყების დრო უნდა იყოს  8-დან  15 საათამდე.")
        if parsed_time.minute < 0 or parsed_time.minute > 59:
            raise ScheduleGenerationError("წუთების მაჩვენებელი უნდა იყოს  0-59 დიაპაზონში.")
        return parsed_time
    

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
        schedule.append(f'# ᲒᲐᲙᲕᲔᲗᲘᲚᲘ {lesson_num + 1} ')
        schedule.append(f'{current_time.strftime("%M %H")} * *  1-5 {run_program_string} in')
        # ᲒᲐᲙᲕᲔᲗᲘᲚᲘᲡ ᲓᲐᲡᲠᲣᲚᲔᲑᲐ
        schedule.append( f'{(current_time + timedelta(minutes=lesson_duration)).strftime("%M %H")} * *  1-5 {run_program_string} out')
        schedule.append(f'')
        current_time += timedelta(minutes=lesson_duration)

        

        if (lesson_num + 1) == big_break_count and lesson_num < lessons_count - 1:
            # Большая перемена начинается
            current_time += timedelta(minutes=big_break_duration)

        
        else:    
            current_time += timedelta(minutes=break_duration)

        

    return schedule
def main():
    
    try:


        # ᲡᲙᲝᲚᲘᲡ ᲙᲝᲓᲘᲡ ᲛᲝᲗᲮᲝᲕᲜᲐ
        school_code = get_input_or_default('ᲨᲔᲘᲧᲕᲐᲜᲔ ᲡᲙᲝᲚᲘᲡ 4 ᲜᲘᲨᲜᲐ ᲙᲝᲓᲘ', '0000')
        
        # ᲡᲙᲝᲚᲘᲡ ᲙᲝᲓᲘᲡ ᲨᲔᲛᲝᲬᲛᲔᲑᲐ
        if not school_code.isdigit() or len(school_code) != 4:
            raise InvalidSchoolCodeError(school_code)
        
        
        schedule_params = {
            'გაკვეთილების რაოდენობა': get_input_or_default('შეიყვანე გაკვეთილების რაოდენობა', '7'),
            'გაკვეთილების დაწყება': get_input_or_default('შეიყვანე გაკვეთილების დაწყების დრო (ᲡᲡ:ᲬᲬ)', '9:00'),
            'გაკვეთილის ხანგრძლივობა': get_input_or_default('შეიყვანე გაკვეთილის ხანგრძლივობა', '45'),
            'დასვენების ხანგრძლივობა': get_input_or_default('შეიყვანე შესვენების ხანგრძლივობა', '5'),
            'დიდი დასვენების ხანგრძლივობა': get_input_or_default('შეიყვანე დიდი დასვენების ხანგრძლივობა', '10'),
            'რომელია დიდი დასვენება': get_input_or_default('შეიყვანე რომელია დიდი დასვენება', '3')
        }

        # ᲒᲐᲜᲠᲘᲒᲘᲡ ᲒᲔᲜᲔᲠᲐᲪᲘᲐ
        schedule = generate_schedule(schedule_params)

        # ᲤᲐᲘᲚᲘᲡ ᲡᲐᲮᲔᲚᲘ ᲘᲥᲜᲔᲑᲐ ᲡᲙᲝᲚᲘᲡ ᲙᲝᲓᲘ
        

        # ᲕᲮᲡᲜᲘᲗ ᲤᲐᲘᲚᲡ ᲩᲐᲬᲔᲠᲘᲡᲐᲗᲕᲘᲡ
        with open(school_code, 'w') as file:
            # ᲗᲘᲗᲝᲔᲣᲚ ᲔᲚᲔᲛᲔᲜᲢᲡ ᲕᲬᲔᲠᲗ ᲤᲐᲘᲚᲨᲘ
            for item in schedule:
                file.write(str(item) + '\n')

        print(f"ᲒᲐᲜᲠᲘᲒᲘ ᲩᲐᲘᲬᲔᲠᲐ ᲤᲐᲘᲚᲨᲘ {school_code}")

        # Вывод расписания
        print("ᲒᲐᲙᲕᲔᲗᲘᲚᲔᲑᲘᲡ ᲒᲐᲜᲠᲘᲒᲘ:")
        print("")
        for item in schedule:
            print(item)
            
    except InvalidSchoolCodeError as e:
        print(f"ᲨᲔᲪᲓᲝᲛᲐ (ᲙᲝᲓᲘ {e.code}): {e.message}")
        
    except ScheduleGenerationError as e:
        print(f"ᲨᲔᲪᲓᲝᲛᲐ: {e.message}")

    except Exception as e:
        print("ᲨᲔᲪᲓᲝᲛᲐ: ", str(e))
    

if __name__ == "__main__":    # Параметры расписания на основе ваших данных
    
    main()       
        