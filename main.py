import eel
import os
import sqlite3
import subprocess


#
#dirname = os.path.dirname(__file__)
#eel.init(os.path.join(dirname, "web/"), allowed_extensions=['.js', '.html'])
#
#@eel.expose
#def say_hello_py(x):
#    print('Hello from %s' % x)
#
## Initialize and start the Eel application
#eel.start('index.html', mode='None', port=1000)
def pathIsRepo():
    for i in os.listdir():
        if i == ".git":
            return True
        else:
            return False
def initialize():
    print("Enter your repositorys directory:")
    path = input()
    #change to repo root
    os.chdir(path)
    if(pathIsRepo):
        origin = subprocess.run(['git config --get remote.origin.url'])
        print(origin)
initialize()
    

