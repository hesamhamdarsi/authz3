from flask import current_app    #https://flask.palletsprojects.com/en/1.1.x/appcontext/
from time import sleep
from sys import exit
from os import system

from authz.command.app.test import test_database
from authz import create_app
from authz import config
app = create_app()

print("Starting tests....")

for _ in range(10):
    ctx = app.app_context()   #check the other references at authz > other references 
    ctx.push()
    result = test_database()
    if result:
        ctx.pop()   
        break
    sleep(2)

if not result:
    print("Test was Succeed....")
    exit(1)

system("flask db upgrade")
ctx = app.app_context()
ctx.push()
#this will not load ".flaskenv". keep in mind that in production env, we don't use .flaskenv
current_app.run()
ctx.pop()