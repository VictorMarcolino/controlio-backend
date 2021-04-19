from flask import Blueprint
from flask_restx import Api

from .device_switch import ns as device_switch_ns
from .reception import ns as reception_ns

default_api = Blueprint('api', __name__)
default_api_def = Api(default_api,
                      title='riskywords admin api',
                      version='1.0',
                      description='A description',
                      )

default_api_def.add_namespace(device_switch_ns)
default_api_def.add_namespace(reception_ns)


@default_api_def.errorhandler(ValueError)
def handle_value_error(e):
    return {}, 400
