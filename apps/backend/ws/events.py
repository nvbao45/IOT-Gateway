from apps import sock
from flask_login import login_required
from .func import *

import time
import json


@sock.route('/ws/echo')
@login_required
def echo(ws):
    while True:
        message = ws.receive()
        ws.send(message)


@sock.route('/ws/system-info')
@login_required
def system_info(ws):
    while True:
        ws.send(json.dumps(get_system_info()))
        time.sleep(10)
