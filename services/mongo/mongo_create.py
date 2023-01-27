import copy

def insert_document(institutes, data):
    # fill institute
    institutes.insert_one(data)

    #current_inst = copy.deepcopy(data)
    #for el in current_inst['department']:
    #    del el['specs']

    print(data)
    return