import uuid

from flask_restx import fields
from sqlalchemy import Column, Boolean, String
from sqlalchemy_utils import UUIDType

from src.app.models.mixins import CreatedAtMixin, UpdatedAtMixin


class Device(CreatedAtMixin, UpdatedAtMixin):
    __swagger_doc_format__ = {
        'identifier': fields.String(description='The name', required=True),
        'name': fields.String(description='The name'),
        'is_on': fields.Boolean(description='The object type', required=True),
        **CreatedAtMixin.__swagger_doc_format__,
        **UpdatedAtMixin.__swagger_doc_format__,
    }
    identifier = Column(UUIDType(binary=False), default=uuid.uuid4, primary_key=True)
    is_on = Column(Boolean(), nullable=False, default=False)
    name = Column(String(), nullable=True, default='No name Provided')
    hosts = ...

    @classmethod
    def get_swagger_model(cls):
        return cls.__tablename__, cls.__swagger_doc_format__
