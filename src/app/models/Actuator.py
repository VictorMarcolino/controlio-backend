import uuid

from flask_restx import fields
from sqlalchemy import Column, Boolean, String
from sqlalchemy.orm import relationship
from sqlalchemy_utils import UUIDType

from app.models.ExtraTables import relation_between_microcontrollers_and_actuators
from app.models.mixins import CreatedAtMixin, UpdatedAtMixin


class Actuator(CreatedAtMixin, UpdatedAtMixin):
    __swagger_doc_format__ = {
        'identifier': fields.String(description='The name', required=True),
        'name': fields.String(description='The name'),
        'state': fields.Boolean(description='The object type', required=True),
        'is_attached': fields.Boolean(description='The object type', required=True),
        **CreatedAtMixin.__swagger_doc_format__,
        **UpdatedAtMixin.__swagger_doc_format__,
    }
    identifier = Column(UUIDType(binary=False), default=uuid.uuid4, primary_key=True)
    state = Column(Boolean(), nullable=False, default=False)
    name = Column(String(), nullable=True, default='No name Provided')
    pin = Column(String(), nullable=False, default='INSERT_PIN_HERE', server_default='INSERT_PIN_HERE')
    microcontrollers = ...

    @classmethod
    def get_swagger_model(cls):
        return cls.__tablename__, cls.__swagger_doc_format__

    @property
    def is_attached(self) -> bool:
        return len(self.microcontrollers) > 0
