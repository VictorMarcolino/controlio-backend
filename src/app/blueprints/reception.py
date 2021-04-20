from flask import request
from flask_restx import Namespace, Resource, abort

from app.models import Microcontroller, ActuatorBinary

ns = Namespace('reception', description='...')


@ns.route('')
class ActuatorWithId(Resource):
    def post(self):
        try:
            if request.is_json:
                microcontroller = {**request.json}
                print(microcontroller)
                h = Microcontroller.query_by_url(microcontroller["host"])
                if h:
                    h.delete()

                _host = Microcontroller(url=microcontroller["host"])
                _host.is_online = True
                for d in microcontroller["actuators"]:
                    ds = ActuatorBinary.find_by_id(d["identifier"])
                    if ds:
                        ds.state = bool(d["state"])
                        _host.actuator_binary.append(ds)
                    else:
                        abort(404)
                _host.add()
                print(microcontroller)
                return 200, {}
            abort(400)
        except Exception as e:
            print(e)
            abort(500)
