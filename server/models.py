from peewee import (
    AutoField,
    TextField,
    Model,
)

from database import database


class Command(Model):
    id = AutoField()
    command = TextField()

    class Meta:
        database = database


class Clipbullet(Model):
    id = AutoField()
    text = TextField()

    class Meta:
        database = database
