from __future__ import annotations

from sqlalchemy.orm import Session, relationship

from app.models.Actuator import Actuator
from app.models.Microcontroller import relation_between_microcontrollers_and_actuators
from app.models.base import Base, db_session


class ActuatorBinary(Actuator, Base):
    __tablename__ = 'actuator_binary'
    __swagger_doc_format__ = {**Actuator.__swagger_doc_format__}
    microcontrollers = relationship("Microcontroller", secondary=relation_between_microcontrollers_and_actuators)

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
    def find_by_id(cls, identifier, db: Session = db_session) -> ActuatorBinary:
        return db.query(cls).filter(cls.identifier == identifier).first()

    @classmethod
    def find_all_by_id(cls, identifier, db: Session = db_session) :
        return db.query(cls).filter(cls.identifier.in_(identifier) ).all()

    def delete(self, db: Session = db_session):
        db.delete(self)
        db.commit()

    def seek_for_active_host(self, db: Session = db_session):
        if self.microcontrollers:
            return self.microcontrollers[0]
        return None
