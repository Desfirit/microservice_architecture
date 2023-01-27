import copy

def insert_document(mongo, data):
    # fill institute
    institutes = mongo["institutes"]

    institutes.insert_one(data)

    current_inst = copy.deepcopy(data)
    for el in current_inst['department']:
        del el['specs']
    print(data)
    return