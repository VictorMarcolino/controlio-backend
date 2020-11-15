from sqlalchemy.orm import Session

from app.models.Device import Device
from app.models.base import Base, db_session


class DeviceSwitch(Device, Base):
    __tablename__ = 'device_switch'
    __swagger_doc_format__ = {**Device.__swagger_doc_format__}

    def add(self, db: Session = db_session):
        try:
            db.add(self)
            db.commit()
        except Exception as e:
            print(e)
            db.rollback()

    @classmethod
    def get_all(cls, db: Session = db_session):
        return db.query(cls).all()
