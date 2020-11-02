import logging
import sys
from http.client import RemoteDisconnected

import sentry_sdk
from celery import Celery, Task
from celery.signals import after_setup_logger
from psycopg2 import OperationalError
from redis.exceptions import ConnectionError as RedisConnectionError
from requests.exceptions import ConnectionError as RequestsConnectionError
from sqlalchemy import create_engine

from app.helper import get_config
from app.models import db_session

AUTORETRY_FOR = (RemoteDisconnected,
                 RequestsConnectionError,
                 OperationalError,
                 RedisConnectionError,
                 )

app_config = get_config()


class DBTask(Task):
    _db_session = None
    _db_engine = None

    def after_return(self, *args, **kwargs):
        if self._db_session is not None:
            self._db_session.remove()
            if self._db_engine is not None:
                self._db_engine.dispose()

    def get_db_session(self):
        """
        this method return a scoped_session configured session with postgreSQL database
        :return: scoped_session
        """
        if self._db_session is None:
            api_database_uri = app_config['worker_database_url']
            self._db_engine = create_engine(api_database_uri, convert_unicode=True)
            db_session.configure(bind=self._db_engine)
            self._db_session = db_session
        return self._db_session


def setup_loggers(logger, *args, **kwargs):
    formatter = logging.Formatter(
        fmt='[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s',
        datefmt="%Y-%m-%dT%H:%M:%S%z"
    )
    stdlog = logging.StreamHandler(sys.stdout)
    stdlog.setFormatter(formatter)
    logger.addHandler(stdlog)


def create_celery():
    app = Celery('background')
    app.config_from_object('app.tasks.config')
    app.autodiscover_tasks([
        'app.tasks.normal_tasks',
        'app.tasks.periodic_tasks',
    ])

    sentry_url = app_config['SENTRY_URL']
    if sentry_url:
        sentry_sdk.init(sentry_url)
    after_setup_logger.connect(setup_loggers)

    return app
