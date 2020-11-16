from flask_restx import Namespace, Resource, abort

from app.models import DeviceSwitch, uuid

ns = Namespace('device_switch', description='...')

DeviceSwitchModel = ns.model(*DeviceSwitch.get_swagger_model())


@ns.route('/<identifier>')
class DeviceWithId(Resource):
    @ns.response(200, description='found', model=DeviceSwitchModel)
    @ns.response(404, description='not found')
    @ns.marshal_with(DeviceSwitchModel)
    def get(self, identifier):
        try:
            result = DeviceSwitch.find_by_id(uuid.UUID(identifier))
            return result, 200 if result else 404
        except ValueError:
            abort(400, 'badly formed hexadecimal UUID string')

    @ns.expect(DeviceSwitchModel)
    @ns.response(200, 'asdas', model=DeviceSwitchModel)
    def post(self):
        return 400


@ns.route('/')
class DeviceWithId(Resource):

    @ns.marshal_with(DeviceSwitchModel, as_list=True)
    def get(self):
        return DeviceSwitch.get_all(), 200

    @ns.expect(DeviceSwitchModel)
    @ns.response(400, 'asdas', model=[DeviceSwitchModel])
    @ns.marshal_with(DeviceSwitchModel)
    def post(self):
        ds = DeviceSwitch()
        ds.add()
        return ds, 202
