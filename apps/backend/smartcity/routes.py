from apps.backend.smartcity import blueprint
from flask import render_template, request, jsonify
from flask_login import login_required
from sqlalchemy import distinct, desc

import psutil
import shutil


@blueprint.route('/')
@login_required
def index():
    return jsonify({'status': 'ok'}), 200
