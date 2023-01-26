import os
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