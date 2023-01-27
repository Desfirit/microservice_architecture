import json
import mongo_utils as utils

def read_group(name):
    mongo = utils.get_mongo()

    group = mongo.find_one({'name': name})

    if group is not None:
        return utils.Group.from_bson(group)
    else:
        return None

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Group reader')

    parser.add_argument('name', type=str, help='Group name')

    args = parser.parse_args()

    group = read_group(args.name)
    if(group is None):
        print(f'Group {args.name} not found')
        pass
    
    print(f'Group: {group.get_name()}')
    print(group.get_students())