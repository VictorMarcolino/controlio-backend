from __future__ import annotations

from datetime import datetime

from requests import get
from sqlalchemy import Boolean, String, Table, ForeignKey, Column, DateTime
from sqlalchemy.orm import Session, relationship
from sqlalchemy_utils import UUIDType

from app.models.ExtraTables import relation_between_microcontrollers_and_actuators
from app.models.base import Base, db_session
from app.models.mixins import CreatedAtMixin, UpdatedAtMixin




class Microcontroller(CreatedAtMixin, UpdatedAtMixin, Base):
    __tablename__ = 'hosts'
    url = Column(String(), primary_key=True)
    is_online = Column(Boolean(), nullable=False, default=False)
    last_time_was_saw_online = Column(DateTime, default=datetime.utcnow, index=True)
    actuator_binary = relationship("ActuatorBinary", secondary=relation_between_microcontrollers_and_actuators)

    def check_online(self, db: Session = db_session):

        try:
            response = get(url=f'http://{self.url}/0')
            print(response.status_code)
            print(f'http://{self.url}/0')
            if response.status_code == 200:
                self.last_time_was_saw_online = datetime.utcnow()
                self.is_online = True
                ac = response.json().get("actuators")
                for b in ac:
                    for a in self.actuator_binary:
                        if str(a.identifier) == b.get("identifier"):
                            a.state = b.get("state")
                db.commit()
                return
        except Exception as e:
            pass
        self.is_online = False
        db.commit()
        time_delta = (datetime.utcnow() - self.last_time_was_saw_online)
        total_seconds = time_delta.total_seconds()
        minutes = total_seconds / 60
        print(minutes)
        if minutes > 2:
            self.delete(db=db)

    def add(self, db: Session = db_session):
        try:
            db.add(self)
            db.commit()
        except Exception as e:
            db.rollback()
            raise e

    @classmethod
    def query_by_url(cls, url, db: Session = db_session) -> Microcontroller:
        return db.query(cls).filter(cls.url == url).first()

    def delete(self, db: Session = db_session):
        db.delete(self)
        db.commit()

    @classmethod
    def get_all(cls, db: Session = db_session):
        return db.query(cls).all()
