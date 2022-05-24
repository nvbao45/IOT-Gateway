from flask import Blueprint

blueprint = Blueprint(
    'smartcity_blueprint',
    __name__,
    url_prefix='/sm'
)
