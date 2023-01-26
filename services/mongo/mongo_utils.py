import pymongo

def get_mongo():
    db = pymongo.MongoClient('mongo', 27017, directConnection=True)
    return db['mirea-db']