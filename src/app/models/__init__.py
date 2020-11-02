from sqlalchemy import Column, event, DateTime, Enum, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import PasswordType, UUIDType

from datetime import datetime

import uuid

db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False))

Base = declarative_base()
Base.query = db_session.query_property()

EXTENDED_USER = 'extended_user'


class CreatedAtMixin(object):
    created_at = Column(DateTime, default=datetime.utcnow, index=True)


class UpdatedAtMixin(object):
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, index=True)


account_types = Enum(EXTENDED_USER, name='account_types')


class Account(Base):
    __tablename__ = 'accounts'
    uuid = Column(UUIDType(binary=False), primary_key=True)
    type = Column(account_types, nullable=False, index=True)
    value = Column(String(64), nullable=False, index=True)

    __table_args__ = (
        UniqueConstraint('type', 'value', name='type_value'),
    )

    __mapper_args__ = {
        'polymorphic_identity': 'account',
        'polymorphic_on': type
    }


# class ExtendedUser(Account, CreatedAtMixin, UpdatedAtMixin):
#     __tablename__ = 'account_extended_user'
#     uuid = Column(UUIDType(binary=False), ForeignKey('accounts.uuid'), primary_key=True)
#     password = Column(PasswordType(schemes=['pbkdf2_sha512']))
#
#     @property
#     def username(self):
#         return self.value
#
#     @username.setter
#     def username(self, value):
#         self.value = value
#
#     def __repr__(self):
#         return f'<LocalUser {self.uuid}, {self.value}>'
#
#     __mapper_args__ = {
#         'polymorphic_identity': EXTENDED_USER,
#     }
#
#
# @event.listens_for(ExtendedUser, 'before_insert')
# def create_uuid(mapper, connection, target):
#     if not target.uuid:
#         target.uuid = uuid.uuid4()
