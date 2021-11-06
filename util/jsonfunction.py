import os
import json

import requests


def getValue(obj, key):
    if isinstance(obj , dict):
        return obj[key]
    else:
        return getattr(obj, key)


def listMatchList(ll1, ll2):
    if not len(ll1):
        return True
    for l1 in ll1:
        if l1 in ll2:
            return True
    return False


def getJson(name, directory="json/"):
    files = os.listdir(directory)
    for file in files:
        if name + ".json" in file:
            with open(os.path.join(directory, file)) as jsonFile:
                data = json.load(jsonFile)
            return data
    return []


def saveJsonApiResponseInJsonFile(url, filePath):
    with open(filePath, "w+") as f:
        rJson = requests.get(url).json()
        json.dump(rJson, f, indent=4)
        return rJson


def applyJsonConfig(obj, name, directory="json/"):
    res = []
    for k, v in getJson(name, directory=directory).items():
        setattr(obj, k, v)
        res.append(k)
    return res


def toJson(name, data, directory=""):
    directory = "json/" + directory
    with open(os.path.join(directory, name + ".json"), 'w') as f:
        json.dump(data, f, indent=2)


def appendJson(name, data, directory=""):
    datastore = getJson(directory, name)
    if name == "verifiedLol":
        del data['birthdate']
        del data['confirm_password']
        mail = data['email'][0] + "@" + data['email'][1]
        data['email'] = mail

    datastore.append(data)
    directory = "json/" + directory
    with open(os.path.join(directory, name + ".json"), 'w') as f:
        json.dump(datastore, f, indent=2)


def jsonPrint(dataName, data):
    print(dataName + ":", json.dumps(data, indent=2))
