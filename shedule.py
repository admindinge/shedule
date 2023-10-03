""" ᲡᲙᲝᲚᲘᲡ ᲐᲕᲢᲝᲛᲐᲢᲣᲠᲘ ᲖᲐᲠᲘᲡ ᲒᲐᲜᲠᲘᲒᲘᲡ ᲒᲔᲜᲔᲠᲐᲪᲘᲐ """
from datetime import datetime, timedelta


class SchoolScheduleError(Exception):
    """
        ᲒᲐᲜᲠᲘᲒᲘᲡ ᲒᲔᲜᲔᲠᲐᲪᲘᲐ ᲨᲔᲪᲓᲝᲛᲐ
    """
    # No code needed here


class InvalidSchoolCodeError(SchoolScheduleError):
    """
        არაკორექტული სკოლის კოდი

        მაგალითად, სკოლის კოდი უნდა იყოს 4 ციფრიანი
    """

    def __init__(self, code):
        self.code = code
        self.message = f"არაკორექტული სკოლის კოდი: {repr(code)}"
        super().__init__(self.message)


class ScheduleGenerationError(SchoolScheduleError):
    """
        Განრიგის გენერაციის შეცდომა
    """

    def __init__(self, message):
        self.message = f"განრიგის გენერაციის შეცდომა: {repr(message)}"
        super().__init__(self.message)


def parse_time(time_str):
    """
        ᲓᲠᲝᲘᲡ ᲤᲝᲠᲛᲐᲢᲘᲡ ᲞᲐᲠᲡᲘᲜᲒᲘ
    """
    parsed_time = datetime.strptime(time_str, '%H:%M')
    if parsed_time.hour < 8 or parsed_time.hour > 15:
        raise ScheduleGenerationError(
            "გაკვეთილის დაწყების დრო უნდა იყოს  8-დან  15 საათამდე.")
    if parsed_time.minute < 0 or parsed_time.minute > 59:
        raise ScheduleGenerationError(
            "წუთების მაჩვენებელი უნდა იყოს  0-59 დიაპაზონში.")
    return parsed_time


def get_input_or_default(prompt, default):
    """
        ᲞᲐᲠᲐᲛᲔᲢᲠᲘᲡ ᲨᲔᲧᲕᲐᲜᲐ
    """
    user_input = input(f"{prompt} ({default}): ").strip()
    return default if user_input == "" else user_input


def generate_schedule(schedule_params):
    """
        Განრიგის გენერაცია
    """

    lessons_count = int(schedule_params['გაკვეთილების რაოდენობა'])
    lesson_duration = int(schedule_params['გაკვეთილის ხანგრძლივობა'])
    break_duration = int(schedule_params['დასვენების ხანგრძლივობა'])
    big_break_count = int(schedule_params['რომელია დიდი დასვენება'])
    big_break_duration = int(schedule_params['დიდი დასვენების ხანგრძლივობა'])

    start_time = parse_time(schedule_params['გაკვეთილების დაწყება'])

    if start_time is None:
        return []

    schedule = []
    schedule.append('00 05 * * 1 sudo busybox ntpd -qn -g -p pool.ntp.org > /dev/null 2>&1')
    schedule.append('')
    schedule.append('00 08 * * 1 sudo busybox ntpd -qn -g -p pool.ntp.org > /dev/null 2>&1')
    schedule.append('')
    schedule.append('10 05 * * 1 sudo busybox hwclock -w')
    schedule.append('')
    schedule.append('10 08 * * 1 sudo busybox hwclock -w')
    schedule.append('')
    schedule.append('00 00 * * 1-5 sudo /home/tc/check_shedule.sh')
    schedule.append('')
    schedule.append('00 07 * * 1-5 sudo /home/tc/check_shedule.sh')
    schedule.append('')
    
    current_time = start_time

    run_program_string = 'sudo /home/tc/bell.c'

    for lesson_num in range(lessons_count):

        # ᲒᲐᲙᲕᲔᲗᲘᲚᲘ {lesson_num + 1}
        schedule.append(f'# ᲒᲐᲙᲕᲔᲗᲘᲚᲘ {lesson_num + 1} ')
        schedule.append(
            f'{current_time.strftime("%M %H")} * *  1-5 {run_program_string} in')
        # ᲒᲐᲙᲕᲔᲗᲘᲚᲘ {lesson_num + 1}
        schedule.append(
            f'{(current_time + timedelta(minutes=lesson_duration)).strftime("%M %H")} * *  1-5 {run_program_string} out')
        schedule.append('')
        current_time += timedelta(minutes=lesson_duration)

        if (lesson_num + 1) == big_break_count and lesson_num < lessons_count - 1:
            # ᲓᲘᲓᲘ ᲓᲐᲡᲕᲔᲜᲔᲑᲘᲡ ᲓᲐᲡᲐᲬᲧᲘᲡᲘ
            current_time += timedelta(minutes=big_break_duration)

        else:
            current_time += timedelta(minutes=break_duration)

    return schedule


def main():
    """
        ᲖᲐᲠᲘᲡ ᲒᲐᲜᲠᲘᲒᲘᲡ ᲒᲔᲜᲔᲠᲐᲪᲘᲐ
    """
    try:

       # ᲡᲙᲝᲚᲘᲡ ᲙᲝᲓᲘᲡ ᲛᲝᲗᲮᲝᲕᲜᲐ
        school_code = get_input_or_default(
            'ᲨᲔᲘᲧᲕᲐᲜᲔ ᲡᲙᲝᲚᲘᲡ 4 ᲜᲘᲨᲜᲐ ᲙᲝᲓᲘ', '0000')

        # ᲡᲙᲝᲚᲘᲡ ᲙᲝᲓᲘᲡ ᲨᲔᲛᲝᲬᲛᲔᲑᲐ
        if not school_code.isdigit() or len(school_code) != 4:
            raise InvalidSchoolCodeError(repr(school_code))
        lesson_count = 'გაკვეთილების რაოდენობა'
        start_time = 'გაკვეთილების დაწყება'
        lesson_duration = 'გაკვეთილის ხანგრძლივობა'
        break_duration = 'დასვენების ხანგრძლივობა'
        big_break_duration = 'დიდი დასვენების ხანგრძლივობა'
        big_break_count = 'რომელია დიდი დასვენება'

        schedule_params = {
            lesson_count: get_input_or_default('შეიყვანე გაკვეთილების რაოდენობა', '7'),
            start_time: get_input_or_default('შეიყვანე გაკვეთილის დაწყების დრო (ᲡᲡ:ᲬᲬ)', '9:00'),
            lesson_duration: get_input_or_default('შეიყვანე გაკვეთილის ხანგრძლივობა', '45'),
            break_duration: get_input_or_default('შეიყვანე შესვენების ხანგრძლივობა', '5'),
            big_break_duration: get_input_or_default('შეიყვანე დიდი დასვენების ხანგრძლივობა', '10'),
            big_break_count: get_input_or_default(
                'შეიყვანე რომელია დიდი დასვენება', '3')
        }

        # ᲒᲐᲜᲠᲘᲒᲘᲡ ᲒᲔᲜᲔᲠᲐᲪᲘᲐ
        schedule = generate_schedule(schedule_params)

        # ᲤᲐᲘᲚᲘᲡ ᲡᲐᲮᲔᲚᲘ ᲘᲥᲜᲔᲑᲐ ᲡᲙᲝᲚᲘᲡ ᲙᲝᲓᲘ

        # ᲕᲮᲡᲜᲘᲗ ᲤᲐᲘᲚᲘᲡ ᲩᲐᲬᲔᲠᲘᲡᲐᲗᲕᲘᲡ
        with open(school_code, 'w', encoding='utf-8') as file:
            # ᲗᲘᲗᲝᲔᲣᲚ ᲔᲚᲔᲛᲔᲜᲢᲡ ᲕᲬᲔᲠᲗ ᲤᲐᲘᲚᲨᲘ
            for item in schedule:
                file.write(str(item) + '\n')

        print(f"ᲒᲐᲜᲠᲘᲒᲘ ᲩᲐᲘᲬᲔᲠᲐ ᲤᲐᲘᲚᲨᲘ {school_code}")

        # ᲒᲐᲜᲠᲘᲒᲘᲡ ᲒᲐᲛᲝᲢᲐᲜᲐ
        print("ᲒᲐᲙᲕᲔᲗᲘᲚᲔᲑᲘᲡ ᲒᲐᲜᲠᲘᲒᲘ:")
        print("")
        for item in schedule:
            print(item)

    except InvalidSchoolCodeError as value_error:
        print(f"ᲨᲔᲪᲓᲝᲛᲐ (ᲙᲝᲓᲘ {value_error.code}): {value_error.message}")

    except ScheduleGenerationError as value_error:
        print(f"ᲨᲔᲪᲓᲝᲛᲐ: {value_error.message}")

    except ValueError as value_error:
        print("ᲨᲔᲪᲓᲝᲛᲐ: ", str(value_error))


if __name__ == "__main__":    # 

    main()
