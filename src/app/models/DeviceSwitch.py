from __future__ import annotations

from sqlalchemy.orm import Session, relationship

from src.app.models.Device import Device
from src.app.models.Hosts import ds_host_relation
from src.app.models.base import Base, db_session


class DeviceSwitch(Device, Base):
    __tablename__ = 'device_switch'
    __swagger_doc_format__ = {**Device.__swagger_doc_format__}
    hosts = relationship("Host", secondary=ds_host_relation,
                         back_populates="device_switch")

    def add(self, db: Session = db_session):
        try:
            db.add(self)
            db.commit()
        except Exception as e:
            print(e)
            db.rollback()

    def reflect_changes(self, db: Session = db_session):
        try:
            db.commit()
        except Exception as e:
            print(e)
            db.rollback()

    @classmethod
    def get_all(cls, db: Session = db_session):
        return db.query(cls).all()

    @classmethod
    def find_by_id(cls, identifier, db: Session = db_session) -> DeviceSwitch:
        return db.query(cls).filter(cls.identifier == identifier).first()

    def seek_for_active_host(self, db: Session = db_session):
        if self.hosts:
            return self.hosts[0]
        return None
