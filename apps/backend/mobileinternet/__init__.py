from flask import Blueprint

blueprint = Blueprint('mb_blueprint',
                      __name__,
                      url_prefix='/mb')
