from flask import Flask
from peewee_aio import Manager

__project__ = "sequvice"


class FlaskApp(Flask):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db = Manager("aiosqlite:///db.sqlite")


app = FlaskApp(__name__)

from sequvice_app.api import *
