from apps.backend.camera_device import blueprint
from flask import render_template, request, jsonify, Response
from flask_login import login_required
from apps.backend.camera_device.models import CameraDevices

from apps import db
from flask_login import current_user

import random
import string
import cv2

def get_random_string(length):
    result_str = ''.join(random.choice(string.ascii_letters) for i in range(length))
    return result_str


def generate(uri):
    cap = cv2.VideoCapture(uri)

    while True:
        success, frame = cap.read()
        if not success:
            break
        # Encode frame to JPEG
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        # Create HTTP multipart stream
        yield (b'--fprame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@blueprint.route('/<int:id>/video_feed')
@login_required
def video_feed(id):
    camera = CameraDevices.query.filter_by(id=id, flag=1).first()
    if not camera:
        return jsonify({"status": "error", "message": "Camera not found"}), 404
    uri = camera.uri
    
    return Response(generate(uri),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@blueprint.route('/')
@login_required
def index():
    _cameras = CameraDevices.query.filter_by(flag=1).order_by(CameraDevices.created_at.desc()).all()
    return render_template('devices/camera.html',
                           segment='camera-device',
                           cameras=_cameras)


@blueprint.route('/<int:id>', methods=['GET'])
@login_required
def camera_detail(id):
    camera = CameraDevices.query.filter_by(id=id, flag=1).first()
    if not camera:
        return jsonify({"status": "error", "message": "Camera not found"}), 404
    
    return jsonify(camera)


@blueprint.route('/view/<int:id>', methods=['GET'])
@login_required
def camera_view(id):
    camera = CameraDevices.query.filter_by(id=id, flag=1).first()
    if not camera:
        return jsonify({"status": "error", "message": "Camera not found"}), 404

    return render_template('devices/camera-view.html',
                           segment='camera-device',
                           camera=camera)
    

@blueprint.route('/add', methods=['POST'])
@login_required
def add():
    if "name" not in request.form:
        return jsonify({"status": "error", "message": "Name is required"})
    if "description" not in request.form:
        return jsonify({"status": "error", "message": "Description is required"})
    if "protocol" not in request.form:
        return jsonify({"status": "error", "message": "Protocol is required"})
    if "port" not in request.form:
        return jsonify({"status": "error", "message": "Port is required"})
    if "ip_address" not in request.form:
        return jsonify({"status": "error", "message": "IP Address is required"})

    name = request.form['name'].strip()
    description = request.form['description'].strip()
    protocol = request.form['protocol'].strip()
    port = request.form['port'].strip()
    uri =  request.form['uri'].strip() if 'uri' in request.form else None
    ip_address = request.form['ip_address'].strip()
    username = request.form['username'].strip() if 'username' in request.form else None
    password = request.form['password'].strip() if 'password' in request.form else None
    stream_path = request.form['stream_path'].strip() if 'stream_path' in request.form else None

    camera_device = CameraDevices(
        name=name,
        description=description,
        protocol=protocol,
        port=port,
        uri=uri,
        ip_address=ip_address,
        stream_path=stream_path,
        username=username,
        password=password,
        owner=current_user.username
    )

    db.session.add(camera_device)
    db.session.commit()

    return jsonify({"success": True, "message": "Device added successfully"})


@blueprint.route('/delete/<int:camera_id>', methods=['DELETE'])
def delete(camera_id):
    camera = CameraDevices.query.filter_by(id=camera_id).first()
    if camera is None:
        return jsonify({"success": False, "message": "Camera not found"})

    camera.flag = 0
    db.session.commit()
    return jsonify({"success": True, "message": "Camera deleted successfully"})


@blueprint.route('/edit/<int:camera_id>', methods=['POST'])
@login_required
def edit(camera_id):
    if "name" not in request.form:
        return jsonify({"status": "error", "message": "Name is required"})
    if "description" not in request.form:
        return jsonify({"status": "error", "message": "Description is required"})
    if "protocol" not in request.form:
        return jsonify({"status": "error", "message": "Protocol is required"})
    if "port" not in request.form:
        return jsonify({"status": "error", "message": "Port is required"})
    if "ip_address" not in request.form:
        return jsonify({"status": "error", "message": "IP Address is required"})

    name = request.form['name'].strip()
    description = request.form['description'].strip()
    protocol = request.form['protocol'].strip()
    port = request.form['port'].strip()
    uri =  request.form['uri'].strip() if 'uri' in request.form else None
    ip_address = request.form['ip_address'].strip()
    username = request.form['username'].strip() if 'username' in request.form else None
    password = request.form['password'].strip() if 'password' in request.form else None
    stream_path = request.form['stream_path'].strip() if 'stream_path' in request.form else None

    camera_device = CameraDevices.query.get(camera_id)
    camera_device.name = name
    camera_device.description = description
    camera_device.protocol = protocol
    camera_device.port = port
    camera_device.uri = uri
    camera_device.ip_address = ip_address
    camera_device.username = username
    camera_device.password = password
    camera_device.stream_path = stream_path

    db.session.commit()

    return jsonify({"success": True, "message": "Device updated successfully"})