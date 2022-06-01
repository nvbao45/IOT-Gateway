from flask import Blueprint
from . import events

blueprint = Blueprint(
    'chart_blueprint',
    __name__,
    url_prefix='/chart'
)
