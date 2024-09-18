import eel
import os
import subprocess
import tkinter 
import tkinter.filedialog as filedialog
import glob
import re


eel.init(("web"))

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
        locked = subprocess.run(['git', 'lfs', 'locks'], capture_output=True, text=True).stdout.split("\n")
        for i in locked:
            if i != "":
                p = i.split("\t")
                eel.AddFile(p)
                print(p)
        eel.ToggleButtons()
    else:
        return 0

@eel.expose
def remove(file):
    result = subprocess.run(['git', 'lfs', 'unlock', file], capture_output=True, text=True).stdout.split("\n")
    eel.reloadJS()
    print(result)

@eel.expose
def reloadPY():
    locked = subprocess.run(['git', 'lfs', 'locks'], capture_output=True, text=True).stdout.split("\n")
    for i in locked:
        if i != "":
            p = i.split("\t")
            eel.AddFile(p)
            print(p)

def lockFile(filepath):
    result = subprocess.run(['git', 'lfs', 'lock', filepath], capture_output=True, text=True).stdout.split("\n")
    print(result)

@eel.expose
def SelectFileToAdd():
    root = tkinter.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    file = filedialog.askopenfile()
    print(file.name)
    lockFile(file.name)
    eel.reloadJS()

@eel.expose
def Search(name):
    path = os.getcwd()
    paths = [p for p in glob.glob(path +'/**/'+ name + '*', recursive=True) if os.path.isfile(p)]
    stripped=[]
    for pathe in paths:
        noabsolute = pathe.lstrip(path)
        stripped.append(noabsolute)
    eel.populateSearch(stripped)

eel.start('index.html', port=8000, size=(800, 610))

