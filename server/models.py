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
    View que armazenará os possíveis comandos que poderão ser executados.
    """
    id = AutoField(primary_key=True)
    index = IntegerField(unique=True)
    command = CharField(max_length=255)

    class Meta:
        database = database
