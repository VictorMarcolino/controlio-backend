from typing import List

from app.models import Actuator


class FileGenerator:
    listOfActuators = ...

    def __init__(self, listOfActuators: List[Actuator]):
        self.listOfActuators = [{
            "pin": actuator.pin,
            "identifier": actuator.identifier,
            "name": actuator.name,
        } for actuator in listOfActuators]
        print(self.listOfActuators)

    def generate_file_string(self) -> str:
        raise NotImplementedError()

    def write_to_file(self, path):
        with open('./result.h', 'w') as f:
            f.write(self.generate_file_string())
