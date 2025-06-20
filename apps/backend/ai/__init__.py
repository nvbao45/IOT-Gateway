from flask import Blueprint

blueprint = Blueprint(
    'ai_blueprint',
    __name__,
    url_prefix='/ai'
)
