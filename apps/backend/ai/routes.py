import os
import time

from werkzeug.utils import secure_filename
from flask import current_app, jsonify, Response
from apps import db
from apps.backend.ai import blueprint
from apps.backend.ai.models import AIModel
from flask import render_template, request, json
from flask_login import login_required
from datetime import datetime
from flask_login import (
    current_user,
    login_user,
    logout_user
)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'bin', 'hex', 'elf', 'ino'}

@blueprint.route('/model')
@login_required
def index():
    _images = AIModel.query.all()
    return render_template('ai/models.html', segment='ai-model', images=_images)


@blueprint.route('/model/upload', methods=['POST'])
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
    # if file and allowed_file(file.filename):
    name = request.form['name']
    description = request.form['description']
    version = request.form['version']
    filename = version + "-" + secure_filename(file.filename)
    file_url = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    owner = current_user.username

    file.save(file_url)
    file_size = os.stat(file_url).st_size

    image = AIModel(name=name, description=description,
                    file=filename, created_at=datetime.now(),
                    version=version, size=file_size,
                    url=file_url, owner=owner)
    db.session.add(image)
    db.session.commit()
    return jsonify({'success': True, 'message': 'File uploaded'}), 200
