import os
import keyboard
from decouple import config
from flask import Flask, request
from peewee import (
    SqliteDatabase,
    AutoField,
    IntegerField,
    CharField,
    Model,
    DoesNotExist
)
from flask_admin import Admin
from flask_admin.contrib.peewee import ModelView


DEBUG = config('DEBUG', cast=bool, default=False)
SECRET_KEY = config('SECRET_KEY', default="secret")
FLASK_ADMIN_SWATCH = 'darkly'

app = Flask(__name__)
app.config.from_object(__name__)
database =SqliteDatabase('database.db')
admin = Admin(app, name='remote-commands', template_mode='bootstrap3')


class Command(Model):
    """
    View que armazenará os possíveis comandos que poderão ser executados.
    """
    id = AutoField(primary_key=True)
    index = IntegerField(unique=True)
    command = CharField(max_length=255)

    class Meta:
        database = database


class CommandView(ModelView):
    """
    View da model Command, com a exclusão da coluna 'id' da tela de admin,
    pois não é interessante exibir este dado.
    """
    column_exclude_list = ('id',)


# Adiciona as views na tela de Admin:
admin.add_view(CommandView(Command))


# Definição de endpoints da aplicação Flask
@app.route('/shortcut', methods=['POST'])
def shortcut():
    """
    Recebe um json que deve conter a chave 'command', com o nome de um atalho
    a ser executado.
    Atalhos válidos até o momento:
    - minimize_all: windows + d
    """
    data = request.get_json()
    if not data.get('command', False):
        return {
            "success": False,
            "message": "send command name in 'command' field"
        }
    if data.get('command') == 'minimize_all':
        keyboard.press_and_release('windows+d')
    elif data.get('command') == 'mute_unmute_meet':
        keyboard.press_and_release('ctrl+d')
    else:
        return {"success": False, "message": "command not found"}
    return {"success": True}


@app.route('/command/<int:command_index>')
def exec_command(command_index):
    """
    Executa um comando no terminal. O comando deve ser previamente cadastrado
    na tela de Admin do flask.
    Informar na URL o index do comando a ser executado.
    """
    try:
        to_exec = Command.get(index=command_index)
        command = to_exec.command
    except DoesNotExist:
        return {
            "success": False,
            "message": f"Nenhum comando cadastrado com index {command_index}"
        }

    # Executa o comando
    output = os.system(command)
    # output = subprocess.check_output(to_exec.command)

    if output == 0:
        return {
            "command": command,
            "success": True
        }
    else:
        return {
            "command": command,
            "success": False
        }


if __name__ == '__main__':
    Command.create_table()
    print("* Adicione comandos em http://localhost:5000/admin")
    app.run(host='0.0.0.0')
