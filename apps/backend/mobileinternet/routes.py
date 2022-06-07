import serial
import json
import serial.tools.list_ports
import os
import re
from apps.backend.mobileinternet import blueprint
from flask import render_template, request, jsonify, current_app
from flask_login import login_required


def get_logs_info():
    modem_logs = os.path.join(current_app.config['LOGS_FOLDER'], '3g-logs.txt')
    log_content = ""

    with open(modem_logs, 'r') as f:
        tmp = f.readlines()
    for line in tmp:
        log_content += line

    try:
        wvdial_version = re.search('WvDial: (.*)', log_content).group(1)
        phone_number = re.search('\+CNUM: ,\"(.*)\"', log_content).group(1)
        manufacturer = re.search('Manufacturer: (.*)', log_content).group(1)
        model = re.search('Model: (.*)', log_content).group(1)
        revision = re.search('Revision: (.*)', log_content).group(1)
        imei = re.search('IMEI: (.*)', log_content).group(1)
        local_ip = re.search('local  IP address (.*)', log_content).group(1)
        remote_ip = re.search('remote IP address (.*)', log_content).group(1)
        primary_dns = re.search('primary   DNS address (.*)', log_content).group(1)
        secondary_dns = re.search('secondary DNS address (.*)', log_content).group(1)

        return dict(
            wvdial_version={'value': wvdial_version, 'description': 'WvDial version'},
            phone_number={'value': phone_number, 'description': 'Phone number'},
            manufacturer={'value': manufacturer, 'description': 'Manufacturer'},
            model={'value': model, 'description': 'Model'},
            revision={'value': revision, 'description': 'Revision'},
            imei={'value': imei, 'description': 'IMEI'},
            local_ip={'value': local_ip, 'description': 'Local IP'},
            remote_ip={'value': remote_ip, 'description': 'Remote IP'},
            primary_dns={'value': primary_dns, 'description': 'Primary DNS'},
            secondary_dns={'value': secondary_dns, 'description': 'Secondary DNS'}
        )
    except:
        return dict()


@blueprint.route('/info')
@login_required
def index():
    return render_template('mobileinternet/mb-info.html', logs=get_logs_info(), segment="mb-info")


"""
-- uncomment all the following lines to enable sim module

from apps import sim800l
@blueprint.route('/call', methods=['POST'])
@login_required
def call():
    number = ''
    hangup = ''
    if 'number' in request.form:
        number = request.form['number']
    if 'hangup' in request.form:
        hangup = request.form['hangup']
    if hangup == "true":
        res = sim800l.hangup()
    else:
        res = sim800l.call(number)
    return jsonify(res), 200


@blueprint.route('/post', methods=['POST'])
@login_required
def post():
    if 'url' not in request.form:
        return jsonify({'success': False, 'message': 'No url'}), 200
    if 'body' not in request.form:
        return jsonify({'success': False, 'message': 'No body'}), 200
    url = request.form['url']
    body = request.form['body']
    return jsonify(sim800l.http_post(url, body)), 200


@blueprint.route('/get', methods=['POST'])
@login_required
def get():
    if 'url' not in request.form:
        return jsonify({'success': False, 'message': 'No url'}), 200

    url = request.form['url']
    return jsonify(sim800l.http_get(url)), 200


@blueprint.route('/config', methods=['POST'])
@login_required
def save_config():
    port = request.form['port']
    baudrate = int(request.form['baudrate'])
    timeout = int(request.form['timeout'])
    apn = request.form['apn']
    user = request.form['user']
    pwd = request.form['pwd']

    sim800l.config(port, baudrate, timeout, apn, user, pwd)
    serial_config = dict(
        port=port,
        baudrate=baudrate,
        timeout=timeout,
        apn=apn,
        user=user,
        pwd=pwd
    )
    with open(current_app.root_path + '/config/serial', 'w') as f:
        json.dump(serial_config, f)
    config = SerialConfig.query.first()
    if config is None:
        config = SerialConfig(port=port,
                              baudrate=baudrate,
                              timeout=timeout,
                              apn=apn,
                              apn_user=user,
                              apn_pwd=pwd)
        db.session.add(config)
    else:
        config.port = port
        config.baudrate = baudrate
        config.timeout = timeout
        config.apn = apn
        config.apn_user = user,
        config.apn_pwd = pwd

    db.session.commit()
    return jsonify({'success': True, 'message': 'Saved'}), 200


@blueprint.route('/')
@login_required
def index():
    device_info = []
    sim_status = []
    device_status = False
    return render_template('mobileinternet/mobileinternet.html',
                           device_info=device_info,
                           device_status=device_status,
                           sim_status=sim_status,
                           segment='mobile_internet_main')


@blueprint.route('/config')
@login_required
def config_view():
    ports = list(serial.tools.list_ports.comports())
    baudrates = [9600, 19200, 38400, 57600, 115200]
    config = SerialConfig.query.first()
    device_info = []
    sim_status = []
    device_status = False
    if sim800l is not None:
        try:
            device_status = sim800l.ready()
            device_info = [sim800l.product_name, sim800l.manufacturer]
            sim_status = [sim800l.sim_status, sim800l.phone_number, sim800l.ip_address]
            # sim800l.close()
        finally:
            pass

    return render_template('mobileinternet/mobileinternet-config.html',
                           ports=ports,
                           baudrates=baudrates,
                           config=config,
                           device_info=device_info,
                           device_status=device_status,
                           sim_status=sim_status,
                           segment='mobile_internet_config')

"""
