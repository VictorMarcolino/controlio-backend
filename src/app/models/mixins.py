from datetime import datetime

from flask_restx import fields
from sqlalchemy import Column, DateTime


class CreatedAtMixin(object):
    __swagger_doc_format__ = {
        'created_at': fields.DateTime(description='when it was created'),
    }
    created_at = Column(DateTime, default=datetime.utcnow, index=True)


class UpdatedAtMixin(object):
    __swagger_doc_format__ = {
        'updated_at': fields.DateTime(description='last time something change'),
    }
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, index=True)
