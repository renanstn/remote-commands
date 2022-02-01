import os
import socket

import chime
import clipboard
import keyboard
from flask import Flask, request
from flask_admin import Admin
from peewee import DoesNotExist
from flask_admin.contrib.peewee import ModelView

from models import Command, Clipbullet
from decorators import requires_auth
from settings import *


chime.theme("mario")
app = Flask(__name__)
app.config.from_object(__name__)
admin = Admin(app, name="remote-commands", template_mode="bootstrap3")

# Add views to flask admin
admin.add_view(ModelView(Command))
admin.add_view(ModelView(Clipbullet))

# Define endpoints
@app.route("/shortcut", methods=["POST"])
@requires_auth
def shortcut():
    """
    Expects a JSON containing the shortcut name in 'shortcut' field
    Shortcut must be one of this:
    - 'minimize_all'
    - 'mute_unmute_meet'
    """
    data = request.get_json()
    if not data.get("shortcut", False):
        return {
            "success": False,
            "message": "Send shortcut name in 'shortcut' field",
        }
    if data.get("shortcut") == "minimize_all":
        keyboard.press_and_release("windows+d")
    elif data.get("shortcut") == "mute_unmute_meet":
        keyboard.press_and_release("ctrl+d")
    else:
        return {"success": False, "message": "Shortcut not found"}
    return {"success": True}


@app.route("/command/<int:command_id>", methods=["POST"])
@requires_auth
def exec_command(command_id):
    """
    Exec a previously created command in terminal
    The command ID must be informed in URL
    """
    try:
        to_exec = Command.get(id=command_id)
        command = to_exec.command
    except DoesNotExist:
        return {
            "success": False,
            "message": f"Command not found: ID {command_id}",
        }

    # Executa o comando
    output = os.system(command)
    # output = subprocess.check_output(to_exec.command)

    if output == 0:
        chime.success()
        return {"command": command, "success": True}
    else:
        chime.error()
        return {"command": command, "success": False}


@app.route("/clipbullet/<int:paste_id>", methods=["POST"])
@requires_auth
def load_clipbullet(paste_id):
    """
    Loads a previously created text to clipboard
    The text ID must be informed in URL
    """
    try:
        to_copy = Clipbullet.get(id=paste_id)
        clipboard.copy(to_copy.text)
        chime.info()
    except DoesNotExist:
        return {"success": False, "message": f"Text not found: ID {paste_id}"}
    return {"success": True}


if __name__ == "__main__":
    Command.create_table()
    Clipbullet.create_table()
    # Obter o IP local da máquina, apenas para exibição
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 1))
    local_ip = s.getsockname()[0]
    print(f" * Running app on: {local_ip}")
    print(f" * Add commands on: http://{local_ip}:5000/admin")
    app.run(host="0.0.0.0")
