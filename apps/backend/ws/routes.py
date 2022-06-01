from apps.backend.ws import blueprint
from flask import render_template, request, jsonify
from flask_login import login_required
from apps.backend.ws.models import SensorParser, LastData
from apps.backend.devices.models import Devices
from sqlalchemy import distinct, desc
from apps.backend.ws.func import *

import json


@blueprint.route('/')
@login_required
def index():
    last_data = LastData.query.order_by(desc(LastData.timestamp)).all()
    devices = LastData.query.with_entities(distinct(LastData.node_name), LastData.access_token).all()

    for i, device in enumerate(devices):
        device_name = Devices.query.filter_by(device_token=device.access_token).with_entities(
            Devices.device_name).first()
        tmp = list(device)
        tmp.append(device_name[0])
        device = tuple(tmp)
        devices[i] = device

    return render_template('ws/ws-dashboard.html',
                           segment='ws-dashboard',
                           system=get_system_info(),
                           node_names=devices,
                           last_data=last_data)


@blueprint.route('/data', methods=['POST'])
@login_required
def data():
    start = int(request.form['start'])
    length = int(request.form['length'])

    page = start // length + 1

    _data = SensorParser.query \
        .order_by(desc(SensorParser.timestamp)) \
        .paginate(page=page, per_page=length, error_out=False)
    return jsonify({'recordsTotal': _data.total, 'recordsFiltered': _data.total, 'data': _data.items}), 200


@blueprint.route('/datatable')
@login_required
def datatable():
    return render_template('ws/ws-datatable.html',
                           segment='ws-datatable')
