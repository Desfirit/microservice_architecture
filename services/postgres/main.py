import os
from flask import Flask

app = Flask(__name__)

@app.route("/api/students", methods=["GET"])
def get_students():
    return ["students"]

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.environ["LOCAL_SERVICES_PORT"])