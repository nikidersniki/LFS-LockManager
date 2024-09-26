import eel
import os
import subprocess
import tkinter 
import tkinter.filedialog as filedialog
import glob
from pathlib import Path
import json


eel.init(("web"))

@eel.expose
def loadOnStartup():
    DocumentFolder = Path.home() / 'Documents'
    configExists = os.path.exists(str(DocumentFolder) + "\GHLM\Locks.json")
    if configExists == True:
        path = str(DocumentFolder) + "\GHLM\Locks.json"
        f = open(path, "r")
        jsonStr = f.read()
        if (jsonStr == ""):
            os.remove(str(DocumentFolder) + "\GHLM\Locks.json")
        else:
            jsonA = json.loads(jsonStr)
            print("Loaded Theme: " + str(jsonA["theme"]))
            eel.loadStyle(jsonA["theme"])
            if (jsonA["openLast"] == "True"):                 
                    if (jsonA["github"] != ""):
                        initialize(jsonA["github"])
    else:
        return 0

def pathIsRepo():
    for i in os.listdir():
        if i == ".git":
            return True
        else:
            return False


@eel.expose
def selectFolder():
    root = tkinter.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    directory_path = filedialog.askdirectory()
    eel.setDirText(directory_path)

@eel.expose
def initialize(path):
    #print(path)
    os.chdir(path)
    if(pathIsRepo):
        origin = subprocess.run(['git', 'ls-remote', '--get-url'], capture_output=True, text=True).stdout.strip("\n")
        parts = origin.split("/")
        reponame = parts[4].strip(".git")
        eel.SetTitle(reponame)
        reloadPY()
        DocumentFolder = Path.home() / 'Documents'
        print(str(DocumentFolder) + "\GHLM\Locks.json")
        configExists = os.path.exists(str(DocumentFolder) + "\GHLM\Locks.json")
        if not configExists:
            if not os.path.exists(str(DocumentFolder) + "\GHLM"):
                os.makedirs(str(DocumentFolder) + "\GHLM")
            f = open(str(DocumentFolder) + "\GHLM\Locks.json", "a")
            dog_data = {
              "github": path,
              "type": "Unreal",
              "theme": 0,
              "openLast" : "True"
            }
            dog_data = json.dumps(dog_data)
            print(dog_data)
            f.write(dog_data)
            f.close()
        elif configExists:
            print("Loaded Config")
            jsonpath = str(DocumentFolder) + "\GHLM\Locks.json"
            f = open(jsonpath, "r")
            jsonStr = f.read()
            jsonA = json.loads(jsonStr)
            eel.ToggleSwitches(jsonA["openLast"])
            if (jsonA["github"] == ""):
                jsonA["github"] = path
                data = json.dumps(jsonA)
                f.close()
                f = open(jsonpath, "w")
                f.write(data)
                f.close()
         
        eel.ToggleButtons()
    else:
        return 0

@eel.expose
def remove(file):
    result = subprocess.run(['git', 'lfs', 'unlock', file], capture_output=True, text=True).stdout.split("\n")
    eel.reloadJS()
    print(result)

@eel.expose
def removeAll():
    locked = subprocess.run(['git', 'lfs', 'locks'], capture_output=True, text=True).stdout.split("\n")
    for i in locked:
        if i != "":
            p = i.split("\t")
            file = p[0]
            result = subprocess.run(['git', 'lfs', 'unlock', file], capture_output=True, text=True).stdout.split("\n")
            print(result)
    eel.LoadingFinished()
    eel.reloadJS()

@eel.expose
def reloadPY():
    locked = subprocess.run(['git', 'lfs', 'locks'], capture_output=True, text=True).stdout.split("\n")
    for i in locked:
        if i != "":
            p = i.split("\t")
            text = p[0]
            text = text.replace(" ", "")
            leng = len(text)
            p.append("")
            if(leng > 40):
                actualLength = len(text)
                actualLength = actualLength * -1 + 40
                text = text[::-1]
                text = text[:actualLength]
                points = "&#x2026;"[::-1]
                text = text + points
                text = text[::-1]
                p[3] = text
            else:
                p[3] = p[0]
            eel.AddFile(p)

def lockFile(filepath):
    print('git lfs lock' + filepath)
    result = subprocess.run(['git', 'lfs', 'lock', filepath], capture_output=True, text=True).stdout.split("\n")
    eel.reloadJS()
    print(result)

@eel.expose
def SelectFileToAdd():
    root = tkinter.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    file = filedialog.askopenfile()
    print(file.name)
    lockFile(file.name)

@eel.expose
def AddFile(filename):
    print(filename)
    lockFile(filename)
    eel.cSearch()
    

@eel.expose
def Search(name):
    if name == "":
        eel.cSearch()
    else:
        path = os.getcwd()
        paths = [p for p in glob.glob(path +'/**/'+ name + '*', recursive=True) if os.path.isfile(p)]
        stripped=[]
        for pathe in paths:
            noabsolute = pathe.lstrip(path)
            noabsolute = noabsolute.replace("\\", "/")
            stripped.append(noabsolute)
        eel.populateSearch(stripped)

@eel.expose
def changeThemePy(theme):
    DocumentFolder = Path.home() / 'Documents'
    path = str(DocumentFolder) + "\GHLM\Locks.json"
    print(path)
    f = open(path, "r")
    jsonStr = f.read()
    jsonA = json.loads(jsonStr)
    jsonA["theme"] = theme
    f.close()
    f = open(path, "w")
    modified_json = json.dumps(jsonA)
    print(modified_json)
    f.write(modified_json)
    f.close()
    eel.loadStyle(theme)

@eel.expose
def loadTheme():
    DocumentFolder = Path.home() / 'Documents'
    path = str(DocumentFolder) + "\GHLM\Locks.json"
    print(path)
    f = open(path, "r")
    jsonStr = f.read()
    jsonA = json.loads(jsonStr)
    print("Loaded Theme: " + jsonA["theme"])
    changeThemePy(jsonA["theme"])
    f.close()


@eel.expose
def logout():
    DocumentFolder = Path.home() / 'Documents'
    path = str(DocumentFolder) + "\GHLM\Locks.json"
    f = open(path, "r")
    jsonStr = f.read()
    jsonA = json.loads(jsonStr)
    jsonA["github"] = ""
    f = open(path, "w")
    modified_json = json.dumps(jsonA)
    print(modified_json)
    f.write(modified_json)
    f.close()
    f.close()
    #os.remove(str(DocumentFolder) + "\GHLM\Locks.json")  
    eel.reloadApp()


eel.start('index.html', port=8000, size=(800, 610))

