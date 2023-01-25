import postgre_utils as utils

import datetime
import random

START_SEMESTER_WEEK = datetime.datetime(2019, 2, 4)
WEEK_DELTA = datetime.timedelta(weeks=1)

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
    return psql.execute(f"CREATE TABLE {utils.TABLE_LESSONS} (id SERIAL PRIMARY KEY, type lesson_type NOT NULL, cource_fk INT NOT NULL, description_fk VARCHAR(50) NOT NULL );")

def create_table_schedule(psql):
    return psql.execute(f"CREATE TABLE {utils.TABLE_SCHEDULE}(id SERIAL, groups_fk VARCHAR(12) REFERENCES {utils.TABLE_GROUPS} (id) NOT NULL, lessons_fk INT REFERENCES {utils.TABLE_LESSONS} (id) NOT NULL, lesson_time TIMESTAMP NOT NULL ) PARTITION BY RANGE (lesson_time);")

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
    for week in range(1, 17):
        partitionTableName = utils.TABLE_SCHEDULE + str(currentWeek.year) + "week" + str(week)
        weekEnd = currentWeek + WEEK_DELTA

        create_table_schedule_partition(postgre, partitionTableName, currentWeek.strftime("%Y-%m-%d"), weekEnd.strftime("%Y-%m-%d"))

        currentWeek = weekEnd + datetime.timedelta(days=1)

    create_table_visits(postgre)

NAMES = ['Вася', 'Гриша', 'Петя', 'Родион', 'Саня', 'Макс', 'Влад', 'Вадим']
GROUPS = ['БСБО-01-19', 'БСБО-02-19', 'БСБО-03-19', 'БИСО-01-20', 'БИСО-02-20', 'БИСО-03-20', 'БИСО-03-20', 'БИСО-01-19']
LESSONS = ['Математика', "Вышивание", "Программирование", "Философия", "Микроархитектура систем"]

def shood_add():
    return random.random() < 0.8

def insert_group(psql, indx, group):
    return psql.execute(f"INSERT INTO {utils.TABLE_GROUPS}(id, name) VALUES ({id}, '{group}');")

def insert_student(psql, student, group):
    #return psql.execute(f"INSERT INTO {utils.TABLE_GROUPS}(name) VALUES ('{group}');")
    pass

def insert_lesson(psql, lesson):
    return psql.execute(f"INSERT INTO {utils.TABLE_LESSONS}(id, name) VALUES ({id}, '{lesson}');")

def insert_schedule(psql, group, lesson, time):
    return psql.execute(f"INSERT INTO {utils.TABLE_SCHEDULE} VALUES({group}, {lesson}, '{time}');")

def fill_schedule(psql, lesson, group):
    lessonWeekDay = random.randint(0, 5)
    lessonHourDay = random.randint(9, 18)

    #lessonPerWeek = 1

    lessonTime = datetime.timedelta(days=lessonWeekDay, hours=lessonHourDay)

    currentWeek = START_SEMESTER_WEEK
    for week in range(16):
        currentWeek 

        currentWeek = currentWeek + WEEK_DELTA


def fill_scheme(postgre):
    # Сначала создается предмет, 
    # К нему создаются группы,
    # К группам студенты
    # Урок добавляется в расписание и к нему группа по расписанию на весь семестр

    for indxLes, lesson in enumerate(LESSONS):
        insert_lesson(postgre, indxLes, lesson)
        for indxGroup, group in enumerate(GROUPS):
            if not shood_add():
                continue

            insert_group(postgre, indxGroup, group)

            fill_schedule(postgre, indxLes, indxGroup)
            
        

if __name__ == "__main__":
    postgre = utils.get_postgre()

    create_scheme(postgre)

    fill_scheme(postgre)
