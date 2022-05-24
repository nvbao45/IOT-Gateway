from apps.backend.devices import blueprint
from flask import render_template, request, jsonify
from flask_login import login_required
from apps.backend.devices.models import Devices
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
    _devices = Devices.query.order_by(Devices.device_created_at.desc()).all()
    return render_template('devices/devices.html',
                           segment='devices-token',
                           devices=_devices)


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
