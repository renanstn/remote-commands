from peewee import (
    AutoField,
    TextField,
    Model,
)

from database import database


class Command(Model):
    id = AutoField(primary_key=True)
    command = TextField()

    class Meta:
        database = database


class Clipbullet(Model):
    id = AutoField(primary_key=True)
    text = TextField()

    class Meta:
        database = database
