from __future__ import annotations

from sqlalchemy import String, Table, ForeignKey, Column
from sqlalchemy_utils import UUIDType

from app.models.base import Base

relation_between_microcontrollers_and_actuators = Table(
    'ds_host_relation', Base.metadata,
    Column('host', String(), ForeignKey(f'hosts.url', ondelete="CASCADE", )),
    Column('actuator', UUIDType(), ForeignKey(f'actuator_binary.identifier', ondelete="CASCADE"))
)
