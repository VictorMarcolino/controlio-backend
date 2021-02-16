"""
This package describe all periodic tasks
"""

from celery import shared_task
from celery.utils import log
from sqlalchemy.orm import Session

from src.app.helper import get_config
from src.app.models import DeviceSwitch, Host
from src.app.tasks import DBTask
from src.app.tasks.normal_tasks import foo2, check_host

_configs = get_config()
logger = log.get_task_logger(__name__)


@shared_task(bind=True, base=DBTask, ignore_result=True)
def foo1(self):
    foo2.delay()
    logger.info('periodic task called')


@shared_task(bind=True, base=DBTask, ignore_result=True)
def devices_check(self):
    db: Session = self.get_db_session()
    _hosts = Host.get_all(db=db)
    logger.info(f'check if {len(_hosts)} Hosts are online')
    for d in _hosts:
        check_host.delay(d.url)
