import os
from unittest import mock
from urllib import response
from flask import Flask, jsonify
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

mongo = None

@app.route("/api/all", methods=["GET"])
def get_all():
    res = utils.get_all(mongo)
    return res

@app.route("/api/courses", methods=["GET"])
def get_courses():
    return utils.get_courses(mongo)

@app.route("/api/specialities", methods=["GET"])
def get_specialities():
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