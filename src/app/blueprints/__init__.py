from flask import Blueprint
from flask_restx import Api

from .device_switch import ns as device_switch_ns

default_api = Blueprint('api', __name__)
default_api_def = Api(default_api,
                      title='riskywords admin api',
                      version='1.0',
                      description='A description',
                      # TODO: security='Basic Auth',
                      # TODO: authorizations=authorizations
                      )

default_api_def.add_namespace(device_switch_ns)
