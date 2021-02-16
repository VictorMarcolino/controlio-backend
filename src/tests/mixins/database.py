from os.path import abspath, dirname

import transaction
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.app.models.base import db_session, Base

here = abspath(dirname(__file__))


class DatabaseMixin(object):
    engine_url = 'sqlite:///:memory:'
    db_session = ...

    @classmethod
    def database_set_up_class(cls):
        cls.engine = create_engine(cls.engine_url, echo=False)
        cls.session = sessionmaker()
        Base.metadata.create_all(cls.engine)

    @classmethod
    def database_tear_down_class(cls):
        cls.session.close_all()
        cls.engine.dispose()

    def database_set_up(self):
        self._connection = self.engine.connect()
        self.trans = self._connection.begin_nested()
        db_session.configure(bind=self._connection)
        self.db_session = db_session

    def database_tear_down(self):
        self.trans.rollback()
        db_session.remove()
        transaction.abort()
        self._connection.close()
