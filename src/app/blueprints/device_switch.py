from flask_restx import Namespace, Resource

from app.models import DeviceSwitch

ns = Namespace('device_switch', description='...')

DeviceSwitchModel = ns.model(*DeviceSwitch.get_swagger_model())


@ns.route('/<identifier>')
class DeviceWithId(Resource):
    def get(self):
        return 200

    @ns.response(200, 'asdas', model=DeviceSwitchModel)
    def post(self):
        return 400
@ns.route('/')
class DeviceWithId(Resource):

    @ns.marshal_with(DeviceSwitchModel, as_list=True)
    def get(self):
        return DeviceSwitch.get_all()

    @ns.expect(DeviceSwitchModel)
    @ns.response(400, 'asdas', model=[DeviceSwitchModel])
    @ns.marshal_with(DeviceSwitchModel)
    def post(self):
        ds= DeviceSwitch()
        ds.add()
        return 200
