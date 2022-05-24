import os

from werkzeug.utils import secure_filename
from flask import current_app, jsonify
from apps import db
from apps.backend.ota import blueprint
from apps.backend.ota.models import Images
from flask import render_template, request, json
from flask_login import login_required
from datetime import datetime
from flask_login import (
    current_user,
    login_user,
    logout_user
)

import subprocess
import re


def get_ip_esp8266():
    try:
        output = subprocess.check_output(["avahi-browse", "-ptr", "_arduino._tcp"]).decode('utf-8')
    except:
        return []

    outputs = output.split('\n')
    ips = re.findall(r'[0-9]+(?:\.[0-9]+){3}', output)
    res = []
    for o in outputs:
        for ip in ips:
            if ip in o:
                _tmp = o.split(';')[-1].replace('\"', '').split(" ")
                __tmp = []
                for i in _tmp:
                    __tmp.append(i.split('=')[-1])
                res.append(o.split(';')[6:-1] + __tmp)

    return res


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'bin'}


@blueprint.route('/')
@login_required
def index():
    devices = get_ip_esp8266()
    _images = Images.query.all()
    return render_template('ota/ota-dashboard.html', segment='ota-main', devices=devices, images=_images)


@blueprint.route('/images', methods=['GET'])
@login_required
def images():
    _images = Images.query.order_by(Images.image_created_at.desc()).all()
    return render_template('ota/ota-images.html', segment='ota-images', images=_images)


@blueprint.route('/reconfig', methods=["POST"])
def reconfig():
    if 'image' not in request.form:
        return jsonify({'success': False, 'message': 'Image not found'}), 404
    if 'deviceID' not in request.form:
        return jsonify({'success': False, 'message': 'Device ID not found'}), 404

    image_id = request.form['image']
    device_ip = request.form['deviceID'].replace("-", ".")

    image = Images.query.get(image_id)
    image_location = image.image_url
    python_script = current_app.root_path + "/python_scripts/espota.py"

    try:
        reconfig_output = subprocess.check_output(
            ["python", python_script, "-d", "-i", device_ip, "-f", image_location]).decode('utf-8')
    except Exception as e:
        print(str(e))
        return jsonify({'success': False, 'message': 'Reconfig failed! See server logs for more details'}), 500

    return jsonify({'success': True, 'message': reconfig_output}), 200


@blueprint.route('/image/delete/<int:image_id>', methods=['DELETE'])
@login_required
def delete_image(image_id):
    image = Images.query.get(image_id)
    if image:
        os.remove(image.image_url)
        db.session.delete(image)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Image deleted'}), 200
    else:
        return jsonify({'success': False, 'message': 'Image not found'}), 404


@blueprint.route('/image/upload', methods=['POST'])
@login_required
def images_upload():
    print("file upload")
    if 'name' not in request.form:
        return jsonify({'success': False, 'message': 'Please enter a name'}), 400
    if 'version' not in request.form:
        return jsonify({'success': False, 'message': 'Please enter a version'}), 400,
    if 'description' not in request.form:
        return jsonify({'success': False, 'message': 'Please enter a description'}), 400
    if 'file' not in request.files:
        return jsonify({'success': False, 'message': 'No file part'}), 404
    file = request.files['file']
    if file.filename == '':
        return jsonify({'success': False, 'message': 'No selected file'}), 404
    if file and allowed_file(file.filename):
        name = request.form['name']
        description = request.form['description']
        version = request.form['version']
        filename = version + "-" + secure_filename(file.filename)
        file_url = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        owner = current_user.username

        file.save(file_url)
        file_size = os.stat(file_url).st_size

        image = Images(image_name=name, image_description=description,
                       image_file=filename, image_created_at=datetime.now(),
                       image_version=version, image_size=file_size,
                       image_url=file_url, image_owner=owner)
        db.session.add(image)
        db.session.commit()
        return jsonify({'success': True, 'message': 'File uploaded'}), 200
