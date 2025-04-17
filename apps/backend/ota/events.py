from apps import sock, db
from flask_login import login_required
from apps.backend.ota.func import *
from apps.backend.ota.models import Images

import time
import json


@login_required 
@sock.route('/ota/devices/<string:type>')
def devices(ws, type):
    while True:
        try:
            images = Images.query.filter_by(flag=True).all()
            if type == "usb":
                boards = {}
                boards["esp8266"] = get_board_fqbn("esp8266")
                boards["esp32"] = get_board_fqbn("esp32")
                boards["arduino"] = get_board_fqbn("arduino:avr")
                _data = get_usb_serial_info()
                _data = {
                    "boards": boards,
                    "devices": _data,
                    "images": [{"id": image.id, "image_name": image.image_name, "image_version": image.image_version, "image_description": image.image_description} for image in images]
                }
            elif type == "network":
                _data = get_esp_devices()
                _data = {
                    "devices": _data,
                    "images": [{"id": image.id, "image_name": image.image_name, "image_version": image.image_version, "image_description": image.image_description} for image in images]
                }

            ws.send(json.dumps(_data))
        except Exception as e:
            print(f"Error: {e}")
            ws.close()
            break

        time.sleep(0.1)