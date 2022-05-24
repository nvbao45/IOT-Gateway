from flask import Blueprint

blueprint = Blueprint(
    'ota_blueprint',
    __name__,
    url_prefix='/ota'
)
