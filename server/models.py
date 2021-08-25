from peewee import (
    SqliteDatabase,
    AutoField,
    IntegerField,
    CharField,
    Model,
)


database = SqliteDatabase('database.db')


class Command(Model):
    """
    Model que armazenará os possíveis comandos que poderão ser executados
    """
    id = AutoField(primary_key=True)
    index = IntegerField(unique=True)
    command = CharField(max_length=255)

    class Meta:
        database = database


class Clipbullet(Model):
    """
    Model que armazenará os possíveis textos que serão carregados no clipboard
    """
    id = AutoField(primary_key=True)
    index = IntegerField(unique=True)
    text = CharField(max_length=1024)

    class Meta:
        database = database
