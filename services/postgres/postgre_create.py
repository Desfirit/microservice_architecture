import postgre_utils as utils
from pathlib import Path

import datetime
import random

def get_string_from_date(date):
    return date.strftime("%Y-%m-%d")

def get_string_from_date_with_time(date):
    return date.strftime("%Y-%m-%d %H:%M")

def create_database(psql, dbName):
    psql.execute(f"CREATE DATABASE {dbName}")
    
def create_table_groups(psql):
    return psql.execute(f"CREATE TABLE {utils.TABLE_GROUPS} (id VARCHAR(12) PRIMARY KEY, speciality_fk VARCHAR(8) NOT NULL );")

def create_table_students(psql):
    return psql.execute(f"CREATE TABLE {utils.TABLE_STUDENTS} (id VARCHAR(8) PRIMARY KEY, name VARCHAR(20) NOT NULL, surname VARCHAR(20) NOT NULL, group_fk VARCHAR(12) NOT NULL, FOREIGN KEY (group_fk) REFERENCES {utils.TABLE_GROUPS} (id));")

def create_table_lessons(psql):
    psql.execute(f"CREATE TYPE lesson_type AS ENUM ('Практика', 'Лекция');")
    return psql.execute(f"CREATE TABLE {utils.TABLE_LESSONS} (id SERIAL PRIMARY KEY, type lesson_type NOT NULL, course_fk VARCHAR(120) NOT NULL, description_fk VARCHAR(50) NOT NULL );")

def create_table_schedule(psql):
    return psql.execute(f"CREATE TABLE {utils.TABLE_SCHEDULE}(id SERIAL, group_fk VARCHAR(12) REFERENCES {utils.TABLE_GROUPS} (id) NOT NULL, lesson_fk INT REFERENCES {utils.TABLE_LESSONS} (id) NOT NULL, time TIMESTAMP NOT NULL ) PARTITION BY RANGE (time);")

def create_table_schedule_partition(psql, partitonName, timeFrom, timeTo):
    return psql.execute(f"CREATE TABLE {partitonName} PARTITION OF {utils.TABLE_SCHEDULE} FOR VALUES FROM ('{timeFrom}') TO ('{timeTo}');")

def create_table_visits(psql):
    return psql.execute(f"CREATE TABLE {utils.TABLE_VISITS}(id SERIAL PRIMARY KEY, visited boolean NOT NULL, student_fk VARCHAR(8) NOT NULL, schedule_fk INT NOT NULL, FOREIGN KEY (student_fk) REFERENCES {utils.TABLE_STUDENTS} (id));")

def create_scheme(postgre):
    create_table_groups(postgre)
    create_table_students(postgre)
    create_table_lessons(postgre)
    create_table_schedule(postgre)

    currentWeek = START_SEMESTER_WEEK
    for week in range(1, WEEKS_TO_FILL+1):
        partitionTableName = utils.TABLE_SCHEDULE + str(currentWeek.year) + "week" + str(week)
        weekEnd = currentWeek + WEEK_DELTA

        create_table_schedule_partition(postgre, partitionTableName, currentWeek.strftime("%Y-%m-%d"), weekEnd.strftime("%Y-%m-%d"))

        currentWeek = weekEnd

    create_table_visits(postgre)

START_SEMESTER_WEEK = datetime.datetime(2019, 2, 4)
WEEK_DELTA = datetime.timedelta(weeks=1)
DAY_DELTA = datetime.timedelta(days=1)
WEEKS_TO_FILL = 32

STUDENTS = []
GROUPS = ['МГЕР-02-28', 'МГЕР-03-19', 'МГЕР-01-19', 'БСБО-01-19', 'БСБО-02-19', 'ПЕРН-30-20' , 'БСБО-03-19', 'БИСО-01-20', 'БИСО-02-20', 'БИСО-03-20', 'БИСО-06-20', 'БИСО-01-19']
LESSONS = ['Математика', "Вышивание", "Программирование", "Философия", "Микроархитектура систем", "Глиномество", "Дудосинг", "Флекс"]

def gen_student_id():
    russianLetters = "АБВГДЕЖЗИКЛМНОПРСТУФХЦЧШЩЫЭЮЯ"
    nums = "1234567890"
    return "19" + "".join(random.choices(russianLetters, k=2)) + "".join(random.choices(nums, k=4))

def generate_data():
    names = Path("data_dictionary/names.txt").read_text().splitlines()
    surnames = Path("data_dictionary/surnames.txt").read_text().splitlines()

    namesLen = len(names)
    surnamesLen = len(surnames)

    for indxGroup, group in enumerate(GROUPS):
        for i in range(random.randint(20,30)):
            studentId = gen_student_id()
            student = {"id" : studentId, "name" : names[random.randint(0, namesLen-1)], "surname": surnames[random.randint(0, surnamesLen-1)], "group": group}
            STUDENTS.append(student)


def shood_add_group():
    return random.random() < 0.8

def shood_add(prob):
    return random.random() < prob

def insert_group(psql, group, spec):
    return psql.execute(f"INSERT INTO {utils.TABLE_GROUPS}(id, speciality_fk) VALUES ('{group}', '{spec}');")

def insert_student(psql, studentId, studentName, studentSurname, group):
    return psql.execute(f"INSERT INTO {utils.TABLE_STUDENTS}(id, name, surname, group_fk) VALUES ('{studentId}', '{studentName}', '{studentSurname}', '{group}');")

def insert_lesson(psql, name, type, courseId):
    return psql.execute(f"INSERT INTO {utils.TABLE_LESSONS}(description_fk, type, course_fk) VALUES ('{name}', '{type}', '{courseId}');")

def insert_schedule(psql, group, lesson, time):
    return psql.execute(f"INSERT INTO {utils.TABLE_SCHEDULE}(group_fk, lesson_fk, time) VALUES('{group}', {lesson}, '{time}');")

def insert_visit(psql, schedule_fk, student, visited):
    return psql.execute(f"INSERT INTO {utils.TABLE_VISITS}(schedule_fk, student_fk, visited) VALUES('{schedule_fk}', '{student}', {visited});")

def fill_day(psql, day, group, lessons):
    lessonsTime = [datetime.timedelta(hours=9), datetime.timedelta(hours=10.5), datetime.timedelta(hours=12.5), datetime.timedelta(hours=14, minutes=20), datetime.timedelta(hours=16, minutes=20), datetime.timedelta(hours=18)]
    for lessonTime in lessonsTime:
        if not shood_add(0.4):
            continue

        lesson = random.choice(lessons)

        insert_schedule(psql, group, lesson["id"], day + lessonTime)

def fill_week(psql, week, group, lessons):
    currentDay = week

    for i in range(6):
        fill_day(psql, currentDay, group, lessons)
        currentDay += DAY_DELTA

def fill_schedule(psql, group, lessons):
    currentWeek = START_SEMESTER_WEEK

    for i in range(WEEKS_TO_FILL):
        lesson = random.choices(lessons, k=5)
        #lessons = random.choices(range(1, len(LESSONS)+1), k=3)
        fill_week(psql, currentWeek, group, lesson)

        currentWeek += WEEK_DELTA

def fill_visits(psql, schedl):
    for student in filter(lambda student: student["group"] == schedl["group_fk"], STUDENTS):
        insert_visit(psql, schedl["id"], student["id"], shood_add(0.8))


def fill_scheme(postgre, specialitites, courses, lessons_descriptions):
    generate_data()

    for group in GROUPS:
        insert_group(postgre, group, random.choice(specialitites))

    for student in STUDENTS:
        insert_student(postgre, student["id"], student["name"], student["surname"], student["group"])

    for lesson in lessons_descriptions:
        insert_lesson(postgre, lesson, "Лекция" if shood_add(0.5) else "Практика", random.choice(courses))

    lessons = utils.get_lessons(postgre)
    
    #Filling schedule
    for group in GROUPS:
        if not shood_add(0.3):
            continue    

        fill_schedule(postgre, group, lessons)

    #Filling visits
    schedule = utils.get_schedule(postgre)
    for mg in schedule:
        fill_visits(postgre, mg)
