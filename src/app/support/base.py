from typing import List

from app.models import Device


class FileGenerator:
    listOfDevices = ...

    def __init__(self, listOfDevices: List[Device]):
        self.listOfDevices = [{
            "pin": device.pin,
            "identifier": device.identifier,
            "name": device.name,
        } for device in listOfDevices]
        print(self.listOfDevices)

    def generate_file_string(self) -> str:
        raise NotImplementedError()

    def write_to_file(self, path):
        with open('./result.h', 'w') as f:
            f.write(self.generate_file_string())
