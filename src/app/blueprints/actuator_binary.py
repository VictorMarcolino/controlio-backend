import json

from flask import request, Response
from flask_restx import Namespace, Resource, abort, reqparse, inputs
from requests import get

from app.models import ActuatorBinary, uuid
from app.support import generators

parser = reqparse.RequestParser()
parser.add_argument('kind_of_code', required=True, location='json')
parser.add_argument('actuator_uuids', type=list, required=True, location='json')
parser.add_argument('download',default=False, type=inputs.boolean, required=True, location='args')

ns = Namespace('actuator_binary', description='...')
ActuatorBinaryModel = ns.model(*ActuatorBinary.get_swagger_model())


@ns.route('/<identifier>')
class ActuatorBinaryWithId(Resource):
    @ns.response(200, description='found', model=ActuatorBinaryModel)
    @ns.response(404, description='not found')
    @ns.marshal_with(ActuatorBinaryModel)
    def get(self, identifier):
        try:
            result = ActuatorBinary.find_by_id(uuid.UUID(identifier))
            return result, 200 if result else 404
        except ValueError:
            abort(400, 'badly formed hexadecimal UUID string')

    @ns.expect(ActuatorBinaryModel)
    @ns.response(200, 'asdas', model=ActuatorBinaryModel)
    @ns.marshal_with(ActuatorBinaryModel)
    def post(self, identifier):
        force_uuid = uuid.UUID(identifier)
        result = ActuatorBinary.find_by_id(force_uuid)
        if request.is_json and result:
            actuator_binary = {**request.json}
            Host = result.seek_for_active_host()
            if Host:
                if result.state == bool(actuator_binary["state"]):
                    return result, 200
                response = get(url=f'http://{Host.url}/2/{force_uuid}')
                if response.ok:
                    result.state = not result.state
                    result.reflect_changes()
                    return result, 200
            return result, 404
        elif not result:
            return {}, 404
        return {}, 400

    def delete(self, identifier):
        force_uuid = uuid.UUID(identifier)
        result = ActuatorBinary.find_by_id(force_uuid)
        if result:
            result.delete()
        else:
            return 404
        return 400

    @ns.expect(ActuatorBinaryModel)
    @ns.response(200, 'asdas', model=ActuatorBinaryModel)
    @ns.marshal_with(ActuatorBinaryModel, code=200)
    def put(self, identifier):
        force_uuid = uuid.UUID(identifier)
        result = ActuatorBinary.find_by_id(force_uuid)
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
class ActuatorBinaryRol(Resource):

    @ns.marshal_with(ActuatorBinaryModel, as_list=True)
    def get(self):
        return ActuatorBinary.get_all(), 200

    @ns.expect(ActuatorBinaryModel)
    @ns.marshal_with(ActuatorBinaryModel)
    def post(self):
        if request.is_json:
            actuator_binary = {**request.json}
            name = actuator_binary.get('name', False)
            pin = actuator_binary.get('pin', False)
            kwargs = dict()
            if name:
                kwargs['name'] = name
                kwargs['pin'] = pin
            ds = ActuatorBinary(**kwargs)
            ds.add()
            return ds, 201
        return 400


@ns.route('/code-generate')
class GenerateCode(Resource):
    @ns.expect(parser)
    def post(self):
        args = parser.parse_args()
        actuator_uuids = args.get('actuator_uuids')
        kind_of_code = args.get('kind_of_code')
        download = args.get('download')
        print(json.dumps(args, indent=4, sort_keys=True))

        if kind_of_code in generators:
            listOfActuators = ActuatorBinary.find_all_by_id(actuator_uuids)
            if listOfActuators:
                gen = generators.get(kind_of_code)
                generator = gen(listOfActuators)
                if download:
                    return Response(
                        generator.generate_file_string(),
                        mimetype="text/plain",
                        headers={"Content-disposition":
                                     f"attachment; filename={kind_of_code}.txt"})
                return {**args, "code": generator.generate_file_string()}, 200
        abort(401)
