import json
import os
import requests
import psycopg2
import time

TABLE_STUDENTS = "students"
TABLE_GROUPS = "groups"
TABLE_VISITS = "visits"
TABLE_LESSONS = "lessons"
TABLE_SCHEDULE = "schedule"

def try_connect():
    try:
        return psycopg2.connect(dbname=os.environ["POSTGRE_DBNAME"], user=os.environ["POSTGRE_USER"], 
                        password=os.environ["POSTGRE_PASS"], host="postgres", connect_timeout=30)
    except Exception:
        return None

def get_postgre():
    for trying in range(10):
        conn = try_connect()
        if conn is not None:
            break

        time.sleep(0.5)
        
    conn.autocommit = True
    return conn.cursor()

def get_students(postgre):
    postgre.execute("SELECT * FROM students")
    students = [dict((postgre.description[i][0], value) for i, value in enumerate(row)) for row in postgre.fetchall()]
    return students

def get_groups(postgre):
    postgre.execute("SELECT * FROM groups")
    groups = [dict((postgre.description[i][0], value) for i, value in enumerate(row)) for row in postgre.fetchall()]
    return groups

def get_schedule(postgre):
    postgre.execute("SELECT * FROM schedule")
    schedule = [dict((postgre.description[i][0], value) for i, value in enumerate(row)) for row in postgre.fetchall()]
    return schedule

def get_lessons(postgre):
    postgre.execute("SELECT * FROM lessons")
    lessons = [dict((postgre.description[i][0], value) for i, value in enumerate(row)) for row in postgre.fetchall()]
    return lessons

def get_courses(postgre):
    postgre.execute("SELECT group_fk, course_fk FROM schedule JOIN lessons ON schedule.lesson_fk = lessons.id GROUP BY group_fk, course_fk;")
    courses = [dict((postgre.description[i][0], value) for i, value in enumerate(row)) for row in postgre.fetchall()]
    return courses

def find_worst_students(postgre, lections, start_date, end_date):
    postgre.execute(f"SELECT student_fk AS id, CAST(COUNT(CASE visited WHEN true THEN 1 ELSE NULL END) AS FLOAT) / COUNT(*) AS visit_percent \
                      FROM visits JOIN schedule ON visits.schedule_fk = schedule.id \
                      WHERE schedule.lesson_fk IN {lections} AND schedule.time BETWEEN '{start_date}' AND '{end_date}' \
                      GROUP BY student_fk \
                      ORDER BY visit_percent \
                      LIMIT 10;")

    students = [dict((postgre.description[i][0], value) for i, value in enumerate(row)) for row in postgre.fetchall()]
    return students

def initialize_kafka_connector():
    config_file = open("kafka_connector_config.json")

    config_data = json.load(config_file)

    config_data["config"]["database.user"] = os.environ["POSTGRE_USER"]
    config_data["config"]["database.password"] = os.environ["POSTGRE_PASS"]
    config_data["config"]["database.dbname"] = os.environ["POSTGRE_DBNAME"]

    config_file.close()

    connection_url = 'http://kafka-connector:${kafka_port}/connectors/'.format(kafka_port = os.environ["KAFKA_DEFAULT_PORT"])

    x = requests.post(connection_url, headers={"Content-Type": "application/json"}, json=config_data)

    return x.status_code == 200