from peewee import Model

from .db import model_database


class BaseModel(Model):
    class Meta:
        database = model_database
