from flask import request
from flask_restx import Namespace, Resource, abort

from app.models import Host, DeviceSwitch

ns = Namespace('reception', description='...')


@ns.route('')
class DeviceWithId(Resource):
    def post(self):
        """
        {
            'host': '192.168.1.11',
            'devices': [
                {'identifier': '4b370ab6-f865-477b-b3f6-073a448fc11a1', 'isOn': 0},
                {'identifier': '4b370ab6-f865-477b-b3f6-073a48fc11a2', 'isOn': 0},
                {'identifier': '4b370ab6-f865-477b-b3f6-073a448fc11a3', 'isOn': 0},
                {'identifier': '4b370ab6-f865-477b-b3f6-073a448fc11a4', 'isOn': 0}
            ]
        }
        """
        try:
            if request.is_json:
                microcontroller = {**request.json}
                print(microcontroller)
                h = Host.query_by_url(microcontroller["host"])
                if h:
                    h.delete()

                _host = Host(url=microcontroller["host"])
                _host.is_online = True
                for d in microcontroller["actuators"]:
                    ds = DeviceSwitch.find_by_id(d["identifier"])
                    if ds:
                        ds.is_on = bool(d["state"])
                        _host.device_switch.append(ds)
                    else:
                        abort(404)
                _host.add()
                print(microcontroller)
                return 200, {}
            abort(400)
        except Exception as e:
            print(e)
            abort(500)
