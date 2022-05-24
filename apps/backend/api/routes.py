from apps.backend.api import blueprint
from flask import render_template, request, jsonify
from flask_login import login_required
from sqlalchemy import distinct, desc, or_, and_, update
from apps import db
from apps.backend.devices.models import Devices
from apps.backend.ws.models import SensorParser, LastData

import datetime


def parse_data_and_save(data, access_token):
    _data = data.split("#")
    device_id = _data[0]
    device_name = _data[1]
    timestamp = datetime.datetime.fromtimestamp(int(_data[2])) - datetime.timedelta(hours=7)
    list_sensor = _data[3].split(";")
    for sensor in list_sensor:
        sensor_name = sensor.split(":")[0]
        sensor_value = float(sensor.split(":")[1])
        data = dict(
            node_id=device_id,
            node_name=device_name,
            sensor=sensor_name,
            value=sensor_value,
            timestamp=timestamp,
            access_token=access_token
        )

        try:
            sensor_data = SensorParser(**data)
            last_data = LastData.query.filter(and_(LastData.node_id == device_id,
                                                   LastData.node_name == device_name,
                                                   LastData.sensor == sensor_name)).first()
            if last_data is None:
                ldt = LastData(**data)
                db.session.add(ldt)
                db.session.commit()
            else:
                last_data.value = sensor_value
                last_data.timestamp = timestamp
                db.session.commit()

            db.session.add(sensor_data)
            db.session.commit()
        except Exception as e:
            print(e)
            return False

    return True


@blueprint.route('/data/insert', methods=['POST'])
def insert_data():
    if 'access-token' not in request.headers:
        return jsonify({'message': 'Access token is missing; Please provide a device token by adding "access-token" '
                                   'in the header of the request'}), 401
    access_token = request.headers['access-token']
    device = Devices.query.filter_by(device_token=access_token).first()
    if device is None:
        return jsonify({'message': 'Token incorrect!'}), 401

    data = request.data.decode('utf-8')
    if parse_data_and_save(data, access_token):
        device.request_count += 1
        db.session.commit()
        return jsonify({'message': 'Data inserted successfully'}), 200
    else:
        return jsonify({'message': 'Data not inserted'}), 400
