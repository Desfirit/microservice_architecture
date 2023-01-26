import os
from flask import Flask
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.environ["LOCAL_SERVICES_PORT"])