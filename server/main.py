import keyboard
from flask import Flask, request


app = Flask(__name__)


@app.route('/shortcut', methods=['POST'])
def hello_world():
    data = request.get_json()
    if data.get('command') == 'minimize_all':
        keyboard.press_and_release('windows+d')
    return {"success": True}


app.run(host='0.0.0.0')
