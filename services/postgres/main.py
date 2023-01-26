import os
from flask import Flask, request
import postgre_utils as utils
import postgre_create as create_utils
import logging
import datetime

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

def prepare_database(postgre):
    app.logger.info("Creating scheme")
    create_utils.create_scheme(postgre)
    app.logger.info("Created scheme")

    app.logger.info("Filling database")
    create_utils.fill_scheme(postgre)
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