from apps.backend.devices import blueprint
from flask import render_template, request, jsonify
from flask_login import login_required
from apps.backend.devices.models import Devices
from apps.backend.ws.models import LastData

from sqlalchemy import distinct, desc
from apps import db
from datetime import datetime
from flask_login import current_user

import random
import string


def get_random_string(length):
    result_str = ''.join(random.choice(string.ascii_letters) for i in range(length))
    return result_str


@blueprint.route('/')
@login_required
def index():
    _devices = Devices.query.filter_by(flag=1).order_by(Devices.device_created_at.desc()).all()
    return render_template('devices/devices.html',
                           segment='devices-token',
                           devices=_devices)


@login_required
@blueprint.route('/<int:id>', methods=['GET'])
def get(id):
    device = Devices.query.filter_by(id=id, flag=1).first()
    if device is None:
        return jsonify({"success": False, "message": "Device not found"})

    return jsonify(device)


@login_required
@blueprint.route('/<int:id>/sensors', methods=['GET'])
def get_sensor(id):
    sensors = LastData.query.filter_by(device_id=id).all()
    res = []
    for sensor in sensors:
        res.append({
            "device_id": sensor.device_id,
            "sensor": sensor.sensor,
        })

    return jsonify(res), 200


@blueprint.route('/add', methods=['POST'])
@login_required
def add():
    if "name" not in request.form:
        return jsonify({"status": "error", "message": "Name is required"})
    if "description" not in request.form:
        return jsonify({"status": "error", "message": "Description is required"})

    device = Devices(device_name=request.form['name'],
                     device_description=request.form['description'],
                     device_token=get_random_string(64),
                     device_owner=current_user)
    db.session.add(device)
    db.session.commit()
    return jsonify({"success": True, "message": "Device added successfully"})


@login_required
@blueprint.route('/delete/<int:id>', methods=['DELETE'])
def delete(id):
    device = Devices.query.filter_by(id=id).first()
    if device is None:
        return jsonify({"success": False, "message": "Device not found"})

    device.flag = 0
    db.session.commit()
    return jsonify({"success": True, "message": "Device deleted successfully"})


@login_required
@blueprint.route('/<int:id>/edit', methods=['POST'])
def edit(id):
    device = Devices.query.filter_by(id=id, flag=1).first()
    if device is None:
        return jsonify({"success": False, "message": "Device not found"})

    if "name" in request.form:
        device.device_name = request.form['name']
    if "description" in request.form:
        device.device_description = request.form['description']
    if "token" in request.form:
        device.device_token = request.form['token']

    db.session.commit()
    return jsonify({"success": True, "message": "Device updated successfully"})
