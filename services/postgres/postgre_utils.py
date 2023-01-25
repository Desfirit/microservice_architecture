import os
import psycopg2

TABLE_STUDENTS = "students"
TABLE_GROUPS = "groups"
TABLE_VISITS = "visits"
TABLE_LESSONS = "lessons"
TABLE_SCHEDULE = "schedule"

def get_postgre():
    conn = psycopg2.connect(dbname=os.environ["POSTGRE_DBNAME"], user=os.environ["POSTGRE_USER"], 
                        password=os.environ["POSTGRE_PASS"], host="postgres", connect_timeout=15)

    conn.autocommit = True
    return conn.cursor()