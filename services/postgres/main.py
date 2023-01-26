import os
from flask import Flask, jsonify
import postgre_utils as connect_utils
import postgre_create as utils

app = Flask(__name__)
postgre = None

@app.route("/api/students", methods=["GET"])
def get_students():
    postgre.execute("SELECT * FROM students")
    students = [dict((postgre.description[i][0], value) for i, value in enumerate(row)) for row in postgre.fetchall()]
    return students

@app.route("/api/groups", methods=["GET"])
def get_groups():
    postgre.execute("SELECT * FROM groups")
    groups = [dict((postgre.description[i][0], value) for i, value in enumerate(row)) for row in postgre.fetchall()]
    return groups

def is_scheme_created(postgre):
    postgre.execute("SELECT * FROM information_schema.tables WHERE table_name = 'groups';")
    records = postgre.fetchall()

    if records:
        return True
    else:
        return False

def prepare_database(postgre):
    print("Creating scheme")
    utils.create_scheme(postgre)
    print("Created scheme")

    print("Filling database")
    utils.fill_scheme(postgre)
    print("Filled databse")

if __name__ == "__main__":
    print("Connecting to postgres")
    postgre = connect_utils.get_postgre()
    print("Connected to postgres")

    if is_scheme_created(postgre):
        print("Scheme already created. Simple start")
    else:
        prepare_database(postgre)

    app.run(host="0.0.0.0", port=os.environ["LOCAL_SERVICES_PORT"])