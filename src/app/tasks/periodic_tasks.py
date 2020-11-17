"""
This package describe all periodic tasks
"""

from celery import shared_task
from celery.utils import log
from sqlalchemy.orm import Session

from app.helper import get_config
from app.models import DeviceSwitch
from app.tasks import DBTask
from app.tasks.normal_tasks import foo2, check_device

_configs = get_config()
logger = log.get_task_logger(__name__)


@shared_task(bind=True, base=DBTask, ignore_result=True)
def foo1(self):
    foo2.delay()
    logger.info('periodic task called')


@shared_task(bind=True, base=DBTask, ignore_result=True)
def devices_check(self):
    db: Session = self.get_db_session()
    devices = DeviceSwitch.get_all(db=db)
    logger.info(f'check if {len(devices)} Devices are online')
    for d in devices:
        check_device.delay(d.identifier)
