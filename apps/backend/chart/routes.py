from apps import db
from apps.backend.chart import blueprint
from flask import render_template, request, jsonify
from flask_login import login_required, current_user

from apps.backend.ws.models import LastData, SensorParser
from apps.backend.chart.models import Charts
from apps.backend.devices.models import Devices

from sqlalchemy import distinct, desc


@login_required
@blueprint.route('/')
def index():
    charts = Charts.query.order_by(desc(Charts.id)).filter_by(enable=True).all()
    charts_data = list()
    for i, chart in enumerate(charts):
        _data = SensorParser.query.with_entities(SensorParser.value, SensorParser.timestamp)\
            .filter_by(sensor=chart.sensor, device_id=chart.device_id)\
            .order_by(desc(SensorParser.timestamp)).limit(chart.samples).all()
        data = [x[0] for x in _data]
        datetime = [x[1].strftime("%m/%d/%Y-%H:%M:%S") for x in _data]

        data.reverse()
        datetime.reverse()
        charts_data.append(dict(
            id=chart.id,
            name=chart.name,
            sensor=chart.sensor,
            samples=chart.samples,
            device_id=chart.device_id,
            type=chart.type,
            color=chart.color,
            size=chart.size,
            data=data,
            datetime=datetime
        ))

    return render_template('chart/index.html',
                           segment='chart-index',
                           charts=charts_data)


@login_required
@blueprint.route('/<int:chart_id>', methods=['GET'])
def get(chart_id):
    chart = Charts.query.filter_by(id=chart_id).first()
    if not chart:
        return jsonify({'message': 'Chart not found'}), 404

    return jsonify(chart), 200


@login_required
@blueprint.route('/config')
def config():
    charts = Charts.query.order_by(desc(Charts.id)).all()
    devices = Devices.query.order_by(desc(Devices.id)).all()
    for i, chart in enumerate(charts):
        for j, device in enumerate(devices):
            if chart.device_id == device.id:
                charts[i].device_name = device.device_name

    return render_template('chart/config.html',
                           segment='chart-config',
                           devices=devices,
                           charts=charts)


@login_required
@blueprint.route('/config/add', methods=['POST'])
def add():
    name = request.form['name']
    sensor = request.form['sensor']
    devices = request.form.getlist('devices')
    type = request.form['type']
    samples = request.form['samples']
    color = request.form['color']
    size = request.form['size']
    if 'enable' not in request.form:
        enable = False
    else:
        enable = True if request.form['enable'] == 'true' else False

    if not name or not sensor or not type or not samples or not color or not size or not devices:
        return jsonify({'message': 'Please fill all fields'}), 400

    chart = dict(
        name=name,
        sensor=sensor,
        type=type,
        device_id=devices,
        samples=samples,
        color=color,
        size=size,
        enable=enable,
        owner=current_user.username
    )
    chart = Charts(**chart)
    db.session.add(chart)
    db.session.commit()

    return jsonify({'success': True, 'message': 'Chart added'}), 200


@login_required
@blueprint.route('/config/edit/<int:chart_id>', methods=['POST'])
def edit(chart_id):
    name = request.form['name']
    sensor = request.form['sensor']
    devices = request.form.getlist('devices')
    type = request.form['type']
    samples = request.form['samples']
    color = request.form['color']
    size = request.form['size']
    if 'enable' not in request.form:
        enable = False
    else:
        enable = True if request.form['enable'] == 'true' else False

    if not name or not sensor or not type or not samples or not color or not size or not devices:
        return jsonify({'message': 'Please fill all fields'}), 400

    chart = Charts.query.filter_by(id=chart_id).first()
    chart.name = name
    chart.sensor = sensor
    chart.type = type
    chart.device_id = devices
    chart.samples = samples
    chart.color = color
    chart.size = size
    chart.owner = current_user.username
    chart.enable = enable

    db.session.commit()

    return jsonify({'success': True, 'message': 'Chart updated'}), 200


@login_required
@blueprint.route('/config/delete/<int:chart_id>', methods=['DELETE'])
def delete(chart_id):
    if not chart_id:
        return jsonify({'message': 'Please provide chart id'}), 400

    Charts.query.filter_by(id=chart_id).delete()
    db.session.commit()

    return jsonify({'success': True, 'message': 'Chart deleted'}), 200
