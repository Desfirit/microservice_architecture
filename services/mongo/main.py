import os
from flask import Flask
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

if __name__ == "__main__":
    app.logger.info("Connecting to mongo")
    mongo = utils.get_mongo()
    app.logger.info("Connected to mongo")

    app.logger.info("Filling mongo")
    for doc in DOCS:
        app.logger.info(f"Created document with id: {filler.insert_document(mongo, load_config(doc))}")
    app.logger.info("Filled mongo")

    app.run(host="0.0.0.0", port=os.environ["LOCAL_SERVICES_PORT"])