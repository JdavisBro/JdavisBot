import json
import os

def create(fileName,write="{}",path="settings/"):
    """Creates a new file at path/fileName.json with json content write"""
    if exists(fileName,path):
        return [False,read(fileName,path)]
    open(path+fileName+".json","x")
    with open(path+fileName+".json","w") as f:
        json.dump(write,f)
    return [True,write]

def exists(fileName,path="settings/"):
    """Checks if a file already exists"""
    if os.path.exists(path+fileName+".json"):
        return True
    return False

def read(fileName,path="settings/",key=None,default=None):
    """Reads the json content from path/fileName.json or optionally from key - if it doesn't exist returns default"""
    if not exists(fileName,path):
        create(fileName,path)
    with open(path+fileName+".json","r") as f:
        read = json.load(f)
    if key:
        out = read
        for k in key:
            if k not in out.keys():
                return default
            out = out[k]
        return out
    else:
        return read

def write(fileName,write,path="settings/",key=None):
    """Writes json content write to path/FileName.json with optional key."""
    if not exists(fileName,path):
        create(fileName,path)
    newWrite = write
    if key:
        newWrite = read(fileName,path)
        newWrite[key] = write            
    with open(path+fileName+".json","w") as f:
        return json.dump(newWrite,f)
