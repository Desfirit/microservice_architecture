import os
from flask import Flask, request
import postgre_utils as utils
import postgre_create as create_utils
import logging
import datetime
import requests
import json
import time

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)

postgre = None

def comma_separated_params_to_list(param):
    result = []
    for val in param.split(','):
        if val:
            result.append(val)
    return result

@app.route("/api/students", methods=["GET"])
def get_students():
    args = request.args
    if "from" in args and "until" in args and "lessons" in args:
        app.logger.info("Search request")

        lections = args.getlist("lessons")
        if len(lections) == 1 and ',' in lections[0]:
            lections = tuple(comma_separated_params_to_list(lections[0]))

        start_date = datetime.datetime.strptime(args.get("from"), "%d-%m-%Y")
        end_date = datetime.datetime.strptime(args.get("until"), "%d-%m-%Y")

        app.logger.info(f"lessons = {lections}")
        app.logger.info(f"from = {start_date}")
        app.logger.info(f"until = {end_date}")

        return utils.find_worst_students(postgre, lections, start_date, end_date)

    return utils.get_students(postgre)

@app.route("/api/groups", methods=["GET"])
def get_groups():
    return utils.get_groups(postgre)

@app.route("/api/lessons", methods=["GET"])
def get_lessons():
    return utils.get_lessons(postgre)

@app.route("/api/courses", methods=["GET"])
def get_courses():
    return utils.get_courses(postgre)

def is_scheme_created(postgre):
    postgre.execute("SELECT * FROM information_schema.tables WHERE table_name = 'groups';")
    records = postgre.fetchall()

    if records:
        return True
    else:
        return False

def try_fetch(url):
    while True:
        app.logger.info(f"Fetching {url} ...")
        try:
            response = requests.get(url)
            if response.status_code == 200:
                app.logger.info(f"Fetching {url} successded!")
                return response
        except Exception:
            app.logger.info(f"Fetching {url} failed")
        time.sleep(0.5)

def get_courses_from_mongo():
    response = try_fetch("http://mongo-ma:22808/api/courses")
    insts = response.json()

    courses = []
    for deps in insts:
        for dep in deps["department"]:
            for course in dep["courses"]:
                name = course["name"]
                courses.append(name)
                   
    return courses

def get_specialities_from_mongo():
    response = try_fetch("http://mongo-ma:22808/api/specialities")
    insts = response.json()

    specs = []
    for deps in insts:
        for dep in deps["department"]:
            for spec in dep["specs"]:
                name = spec["name"]
                specs.append(name)

    return specs

def get_lessons_from_elastic():
    response = try_fetch("http://elastic-ma:22808/api/lessons")
    lessons = response.json()

    app.logger.info(f"108) {lessons}")
    res = []
    for lesson in lessons:
        if isinstance(lesson, dict):
            res.append(lesson["name"])

    return res

def prepare_database(postgre):

    courses = get_courses_from_mongo()

    specs = get_specialities_from_mongo()

    get_lessons_from_elastic()
    time.sleep(1)
    lessons = get_lessons_from_elastic()
    app.logger.info(lessons)

    app.logger.info("Creating scheme")
    create_utils.create_scheme(postgre)
    app.logger.info("Created scheme")

    app.logger.info("Filling database")
    create_utils.fill_scheme(postgre, specs, courses, lessons)
    app.logger.info("Filled database")

if __name__ == "__main__":
    app.logger.info("Connecting to postgres")
    postgre = utils.get_postgre()
    app.logger.info("Connected to postgres")

    if is_scheme_created(postgre):
        app.logger.info("Scheme already created. Simple start")
    else:
        prepare_database(postgre)

    app.run(host="0.0.0.0", port=os.environ["LOCAL_SERVICES_PORT"])