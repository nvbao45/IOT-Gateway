from flask import Blueprint

blueprint = Blueprint('camera_blueprint', __name__, url_prefix='/devices/camera')
