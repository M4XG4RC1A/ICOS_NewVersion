import os
import json

def getImages(path):
    try:
        # Get list of files in folder
        file_list = os.listdir(path)
    except:
        file_list = []
    fnames = [
        f
        for f in file_list
        if os.path.isfile(os.path.join(path, f))
        and f.lower().endswith((".png"))
    ]
    return fnames

def getFolders(path):
    try:
        # Get list of files in folder
        file_list = os.listdir(path)
    except:
        file_list = []
    fnames = [
        f
        for f in file_list
        if os.path.isdir(os.path.join(path, f))
    ]
    return fnames

def getName(name):
    if name == "":
        return name
    elif name.lower().endswith(".png"):
        return name[3:-4]
    else:
        return name[3:]

def getOrder(name):
    return name[:3]

def listNames(list):
    return [getName(l) for l in list]

def listOrder(list):
    return [getOrder(l) for l in list]

def getPath():
    return os.getcwd()

def readJSON(path,name):
    with open(path+"\\"+name, "r") as openfile:
        data = json.load(openfile)
    return data

def writeJSON(path,name,data):
    with open(path+"\\"+name, "w") as outfile:
        json.dump(data, outfile)
        
def getJSONs(path,list):
    return [readJSON(path,l+"\\config.json") for l in list]