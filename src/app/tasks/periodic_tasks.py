"""
This package describe all periodic tasks
"""

from celery import shared_task
from celery.utils import log
from sqlalchemy.orm import Session

from app.helper import get_config
from app.models import Host
from app.tasks import DBTask
from app.tasks.normal_tasks import check_host

_configs = get_config()
logger = log.get_task_logger(__name__)


@shared_task(bind=True, base=DBTask, ignore_result=True)
def devices_check(self):
    db: Session = self.get_db_session()
    _hosts = Host.get_all(db=db)
    logger.info(f'check if {len(_hosts)} Hosts are online')
    for d in _hosts:
        check_host.delay(d.url)
