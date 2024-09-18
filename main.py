import eel
import os
import subprocess
import tkinter 
import tkinter.filedialog as filedialog


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
    os.chdir(path)
    if(pathIsRepo):
        origin = subprocess.run(['git', 'ls-remote', '--get-url'], capture_output=True, text=True).stdout.strip("\n")
        parts = origin.split("/")
        reponame = parts[4].strip(".git")
        eel.SetTitle(reponame)
        locked = subprocess.run(['git', 'lfs', 'locks'], capture_output=True, text=True).stdout.split("\n")
        for i in locked:
            p = i.split("\t")
            eel.AddFile(p)
            #print(p)

eel.start('index.html', port=8000, size=(500, 600))

