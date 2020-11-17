from flask_restx import Namespace, Resource

from app.tasks.normal_tasks import foo2

ns = Namespace('reception', description='...')


@ns.route('/<identifier>')
class DeviceWithId(Resource):

    def get(self, identifier):
        foo2.delay()


    def post(self, identifier):
        pass
