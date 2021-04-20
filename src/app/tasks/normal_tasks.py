import datetime

from celery import shared_task
from celery.utils import log
from requests import get
from sqlalchemy.orm import Session

from app.helper import get_config
from app.models import Microcontroller
from app.tasks import DBTask, AUTORETRY_FOR

_config = get_config()
logger = log.get_task_logger(__name__)

MAX_RETRIES = 5


@shared_task(base=DBTask, bind=True, max_retries=MAX_RETRIES, autoretry_for=AUTORETRY_FOR)
def check_host(self, url):
    db: Session = self.get_db_session()
    logger.info(f'checking actuator {url}')
    host = Microcontroller.query_by_url(url, db=db)
    if host:
        logger.info(f'host {url} found')
        host.check_online(db=db)
