import os
from flask import Flask, jsonify
import postgre_utils as connect_utils
import postgre_create as utils

app = Flask(__name__)
postgre = None

default_resp = [
    {"id":"19Б0726", "name": "Вася", "surname": "Пупкин", "group_fk" : "БСБО12-111"},
    {"id":"19Б0226", "name": "Гриша", "surname": "Синьков", "group_fk" : "БИСО-80-2208"}
]

@app.route("/api/students", methods=["GET"])
def get_students():
    if postgre is None:
        return default_resp

    postgre.execute("SELECT * FROM students")
    students = [dict((postgre.description[i][0], value) for i, value in enumerate(row)) for row in postgre.fetchall()]
    print(students)
    return students

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