from flask import request
from flask_restx import Namespace, Resource, abort
from requests import get

from app.models import DeviceSwitch, uuid

ns = Namespace('device_switch', description='...')
DeviceSwitchModel = ns.model(*DeviceSwitch.get_swagger_model())


@ns.route('/<identifier>')
class DeviceSwitchWithId(Resource):
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
    @ns.marshal_with(DeviceSwitchModel)
    def post(self, identifier):
        force_uuid = uuid.UUID(identifier)
        result = DeviceSwitch.find_by_id(force_uuid)
        if request.is_json and result:
            device_sw = {**request.json}
            result.is_on = bool(device_sw["is_on"])
            Host = result.seek_for_active_host()
            if Host:
                response = get(url=f'http://{Host.url}/{force_uuid}/{int(result.is_on)}')
                print(response.ok)
                if response.ok:
                    result.reflect_changes()
                    return result, 200
            return result, 404
        elif not result:
            return 404
        return 400


@ns.route('/')
class DeviceSwitchRol(Resource):

    @ns.marshal_with(DeviceSwitchModel, as_list=True)
    def get(self):
        return DeviceSwitch.get_all(), 200

    @ns.expect(DeviceSwitchModel)
    @ns.marshal_with(DeviceSwitchModel)
    def post(self):
        if request.is_json:
            device_sw = {**request.json}
            name = device_sw.get('name', False)
            kwargs = dict()
            if name:
                kwargs['name'] = name
            ds = DeviceSwitch(**kwargs)
            ds.add()
            return ds, 202
        return 400
