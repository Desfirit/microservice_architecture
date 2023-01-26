import os
from flask import Flask
import logging
import mongo_utils as utils

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)

if __name__ == "__main__":
    mongo = utils.get_mongo()

    app.run(host="0.0.0.0", port=os.environ["LOCAL_SERVICES_PORT"])