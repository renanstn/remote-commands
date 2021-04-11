import os
import keyboard
from flask import Flask, request
from peewee import SqliteDatabase, AutoField, IntegerField, CharField, Model
from flask_admin import Admin
from flask_admin.contrib.peewee import ModelView


DEBUG = True
SECRET_KEY = 'secret'
FLASK_ADMIN_SWATCH = 'darkly'

app = Flask(__name__)
app.config.from_object(__name__)
database =SqliteDatabase('database.db')
admin = Admin(app, name='remote-commands', template_mode='bootstrap3')


class Command(Model):
    id = AutoField(primary_key=True)
    index = IntegerField()
    command = CharField(max_length=255)

    class Meta:
        database = database


admin.add_view(ModelView(Command, database, 'Commands'))

@app.route('/shortcut', methods=['POST'])
def shortcut():
    data = request.get_json()
    if not data.get('command', False):
        return {
            "success": False,
            "message": "send command name in 'command' field"
        }
    if data.get('command') == 'minimize_all':
        keyboard.press('windows+d')
    else:
        return {"success": False, "message": "command not found"}
    return {"success": True}


@app.route('/command/<int:command_index>')
def exec_command(command_index):
    to_exec = Command.get(index=command_index)
    command = to_exec.command
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
    app.run(host='0.0.0.0')
