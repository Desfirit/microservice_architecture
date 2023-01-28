import os
from unittest import mock
from urllib import response
from flask import Flask, jsonify, request
import logging
import mongo_utils as utils
import mongo_create as filler
import json

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)

DOCS = ["data/institute_1.json", "data/institute_2.json", "data/institute_3.json"]

def load_config(path):
    with open(path, 'r', encoding='utf-8') as fp:
        file = json.load(fp)
        return file

def comma_separated_params_to_list(param):
    result = []
    for val in param.split(','):
        if val:
            result.append(val)
    return result

mongo = None

@app.route("/api/all", methods=["GET"])
def get_all():
    res = utils.get_all(mongo)
    return res

@app.route("/api/courses", methods=["GET"])
def get_courses():
    args = request.args

    if "courses" in args:
        courses = args.getlist("courses")
        if len(courses) == 1 and ',' in courses[0]:
            courses = comma_separated_params_to_list(courses[0])

        utils.find_course(mongo, courses)

    return utils.get_courses(mongo)

@app.route("/api/specialities", methods=["GET"])
def get_specialities():
    args = request.args

    if "specs" in args:
        specs = args.getlist("specs")
        if len(specs) == 1 and ',' in specs[0]:
            specs = comma_separated_params_to_list(specs[0])

        utils.find_speciality(mongo, specs)

    return utils.get_specialities(mongo)

if __name__ == "__main__":
    app.logger.info("Connecting to mongo")
    mongo = utils.get_mongo()
    mongo.drop_database("mirea-db")
    app.logger.info("Connected to mongo")

    app.logger.info("Filling mongo")
    mongo = mongo["mirea-db"]["institutes"]

    for doc in DOCS:
        app.logger.info(f"Created document with id: {filler.insert_document(mongo, load_config(doc))}")
    app.logger.info("Filled mongo")

    #utils.get_institute(mongo, "Институт кибербезопасности и цифровых технологий")

    app.run(host="0.0.0.0", port=os.environ["LOCAL_SERVICES_PORT"])