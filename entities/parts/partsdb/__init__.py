import json


def getPartsData():
    with open('parts.json', 'r') as file:
        parts_data = json.load(file)
    return parts_data
