from flask import Flask
from peewee_aio import Manager

__project__ = "sequvice"

app = Flask(__name__)

db = Manager("aiosqlite:///db.sqlite")
