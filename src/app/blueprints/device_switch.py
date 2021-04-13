from flask import request, Response
from flask_restx import Namespace, Resource, abort, reqparse
from requests import get

from app.models import DeviceSwitch, uuid
from app.support import generators

parser = reqparse.RequestParser()
parser.add_argument('kind_of_code', required=True, location='json')
parser.add_argument('devices_uuids', type=list, required=True, location='json')

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
            Host = result.seek_for_active_host()
            if Host:
                if result.is_on == bool(device_sw["is_on"]):
                    return result, 200
                response = get(url=f'http://{Host.url}/2/{force_uuid}')
                if response.ok:
                    result.is_on = not result.is_on
                    result.reflect_changes()
                    return result, 200
            return result, 404
        elif not result:
            return {}, 404
        return {}, 400

    def delete(self, identifier):
        force_uuid = uuid.UUID(identifier)
        result = DeviceSwitch.find_by_id(force_uuid)
        if result:
            result.delete()
        else:
            return 404
        return 400

    @ns.expect(DeviceSwitchModel)
    @ns.response(200, 'asdas', model=DeviceSwitchModel)
    @ns.marshal_with(DeviceSwitchModel, code=200)
    def put(self, identifier):
        force_uuid = uuid.UUID(identifier)
        result = DeviceSwitch.find_by_id(force_uuid)
        if request.is_json and result:
            payload_input = {**request.json}
            if not payload_input.get("name"):
                return {}, 400
            result.name = payload_input.get("name")
            result.reflect_changes()
            return result, 200
        elif not result:
            return {}, 404
        return {}, 400


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
            return ds, 201
        return 400


@ns.route('/code-generate')
class GenerateCode(Resource):
    @ns.expect(parser)
    def post(self):
        args = parser.parse_args()
        devices_uuids = args.get('devices_uuids')
        kind_of_code = args.get('kind_of_code')
        if kind_of_code in generators:
            print(devices_uuids)
            listOfDevices = DeviceSwitch.find_all_by_id(devices_uuids)
            if listOfDevices:
                gen = generators.get(kind_of_code)
                generator = gen(listOfDevices)
                return Response(
                    generator.generate_file_string(),
                    mimetype="text/plain",
                    headers={"Content-disposition":
                                 f"attachment; filename={kind_of_code}.txt"})
                # return {**args, "code": generator.generate_file_string()}, 200
        abort(400)
