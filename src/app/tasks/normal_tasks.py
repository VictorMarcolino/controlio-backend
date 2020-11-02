from celery import shared_task
from celery.utils import log

from app.helper import get_config

from app.tasks import DBTask, AUTORETRY_FOR

_config = get_config()
logger = log.get_task_logger(__name__)

MAX_RETRIES = 5


@shared_task(base=DBTask, bind=True, max_retries=MAX_RETRIES, autoretry_for=AUTORETRY_FOR)
def foo2(self, a, b):
    logger.info('normal task')
    return a + b
