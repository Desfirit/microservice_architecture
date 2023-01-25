import os
from flask import Flask
import postgre_utils as connect_utils
import postgre_create as utils

app = Flask(__name__)

default_resp = [
    {"id":"19Б0726", "name": "Вася", "surname": "Пупкин", "group_fk" : "БСБО12-111"},
    {"id":"19Б0226", "name": "Гриша", "surname": "Синьков", "group_fk" : "БИСО-80-2208"},
]

@app.route("/api/students", methods=["GET"])
def get_students():
    return default_resp

if __name__ == "__main__":
    print("Connecting to postgres")
    postgre = connect_utils.get_postgre()
    print("Connected to postgres")

    print("Creating scheme")
    utils.create_scheme(postgre)
    print("Created scheme")

    #print("Filling database")
    #utils.fill_scheme(postgre)
    #print("Filled databse")

    app.run(host="0.0.0.0", port=os.environ["LOCAL_SERVICES_PORT"])