"""
This package describe all periodic tasks
"""

from celery import shared_task
from celery.utils import log

from app.tasks import DBTask

from app.helper import get_config

_configs = get_config()
logger = log.get_task_logger(__name__)


@shared_task(bind=True, base=DBTask, ignore_result=True)
def foo1(self):
    logger.info('periodic task')
