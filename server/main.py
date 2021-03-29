import keyboard
from flask import Flask, request


app = Flask(__name__)


@app.route('/shortcut', methods=['POST'])
def shortcut():
    data = request.get_json()

    if not data.get('command', False):
        return {
            "success": False,
            "message": "send command name in 'command' field"
        }

    if data.get('command') == 'minimize_all':
        keyboard.press_and_release('windows+d')

    elif data.get('command') == 'lock_screen':
        keyboard.press_and_release('windows+l')

    else:
        return {"success": False, "message": "command not found"}

    return {"success": True}


app.run(host='0.0.0.0')
