from flask import request
from flask_restx import Namespace, Resource

from app.tasks.normal_tasks import foo2

ns = Namespace('reception', description='...')


@ns.route('')
class DeviceWithId(Resource):
    def post(self):
        if request.is_json:
            print({**request.json})
            return 200
        return 400
