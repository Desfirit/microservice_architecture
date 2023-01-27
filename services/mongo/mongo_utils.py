from unicodedata import name
import pymongo

def get_mongo():
    return pymongo.MongoClient('mongo', 27017, directConnection=True)

def get_all(mongo):
    return mongo.find({})

def get_institute(mongo, name):
    res = mongo.find_one({"name": name})
    del res["_id"]
    return res

def get_specialities(mongo):
    res = mongo.find_one({}, {"department.specs": 1})
    del res["_id"]
    return res

def get_courses(mongo):
    res = mongo.find_one({}, {"department.courses": 1})
    del res["_id"]
    return res