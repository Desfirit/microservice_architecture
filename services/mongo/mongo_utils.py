from unicodedata import name
import pymongo

def get_mongo():
    return pymongo.MongoClient('mongo', 27017, directConnection=True)

def get_all(mongo):
    res = mongo.find({})

    response = []
    for inst in res:
        del inst["_id"]
        response.append(inst)
    return response

def find_institute(mongo, name):
    res = mongo.find_one({"name": name})
    del res["_id"]
    return res

def find_speciality(mongo, name):
    res = mongo.find_one({"department.specs.name": name}, {"department.specs.name": 1, "department.name": 1})
    return res

def find_course(mongo, name):
    res = mongo.find_one({"department.courses.name": name}, {"department.courses.name": 1, "department.name": 1})
    return res

def get_specialities(mongo):
    res = mongo.find({}, {"department.specs": 1, "department.name": 1})

    response = []
    for inst in res:
        del inst["_id"]
        response.append(inst)

    return response

def get_courses(mongo):
    res = mongo.find({}, {"department.courses": 1, "department.name": 1})

    response = []
    for inst in res:
        del inst["_id"]
        response.append(inst)

    return response