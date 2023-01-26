import os
from flask import Flask, jsonify
import postgre_utils as utils
import postgre_create as create_utils

app = Flask(__name__)
postgre = None

@app.route("/api/students", methods=["GET"])
def get_students():
    return utils.get_students(postgre)

@app.route("/api/groups", methods=["GET"])
def get_groups():
    return utils.get_groups(postgre)

def is_scheme_created(postgre):
    postgre.execute("SELECT * FROM information_schema.tables WHERE table_name = 'groups';")
    records = postgre.fetchall()

    if records:
        return True
    else:
        return False

def prepare_database(postgre):
    print("Creating scheme")
    create_utils.create_scheme(postgre)
    print("Created scheme")

    print("Filling database")
    create_utils.fill_scheme(postgre)
    print("Filled database")

if __name__ == "__main__":
    print("Connecting to postgres")
    postgre = utils.get_postgre()
    print("Connected to postgres")

    if is_scheme_created(postgre):
        print("Scheme already created. Simple start")
    else:
        prepare_database(postgre)

    app.run(host="0.0.0.0", port=os.environ["LOCAL_SERVICES_PORT"])