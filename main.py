import eel
import os
import sqlite3


dirname = os.path.dirname(__file__)
eel.init(os.path.join(dirname, "web/"), allowed_extensions=['.js', '.html'])

@eel.expose
def say_hello_py(x):
    print('Hello from %s' % x)

# Initialize and start the Eel application
eel.start('index.html', mode='None', port=1000)
