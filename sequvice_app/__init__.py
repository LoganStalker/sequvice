import os

from flask import Flask
from peewee_aio import Manager
from modconfig import Config

__project__ = "sequvice"


class FlaskApp(Flask):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        env = os.environ.get("ENV", "develop")
        self.cfg = Config(f"sequvice_app.config.{env}")
        self.db = Manager(self.cfg.PEEWEE_CONNECTION)


app = FlaskApp(__name__)

from sequvice_app.api import *
