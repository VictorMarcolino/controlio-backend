import uuid
from datetime import datetime

from flask_restx import fields
from requests import get
from sqlalchemy import Boolean, String
from sqlalchemy import Column, DateTime
from sqlalchemy.orm import Session

from app.models.base import Base, db_session
from app.models.mixins import CreatedAtMixin, UpdatedAtMixin


class Host(CreatedAtMixin, UpdatedAtMixin, Base):
    __swagger_doc_format__ = {
        'url': fields.String(description='The name', required=True),
        'is_online': fields.Boolean(description='The object type', required=True),
        **CreatedAtMixin.__swagger_doc_format__,
        **UpdatedAtMixin.__swagger_doc_format__,
        'last_time_was_saw_online': fields.DateTime(description='when it was created'),
    }
    url = Column(String(), default=uuid.uuid4, primary_key=True)
    is_online = Column(Boolean(), nullable=False, default=False)
    last_time_was_saw_online = Column(DateTime, default=datetime.utcnow, index=True)

    @classmethod
    def get_swagger_model(cls):
        return cls.__tablename__, cls.__swagger_doc_format__

    def check_online(self, db: Session = db_session):
        response = get(self.url)
        if response.ok:
            self.last_time_was_saw_online = datetime.utcnow()
            self.is_online = True
        else:
            self.is_online = False
        db.commit()
