from celery import shared_task
from celery.utils import log

from app.helper import get_config
from app.models import DeviceSwitch
from app.tasks import DBTask, AUTORETRY_FOR

_config = get_config()
logger = log.get_task_logger(__name__)

MAX_RETRIES = 5


@shared_task(base=DBTask, bind=True, max_retries=MAX_RETRIES, autoretry_for=AUTORETRY_FOR)
def foo2(self, *args, **kwargs):
    logger.info('normal task called')


@shared_task(base=DBTask, bind=True, max_retries=MAX_RETRIES, autoretry_for=AUTORETRY_FOR)
def check_device(self, identifier):
    logger.info(f'checking device {identifier}')
    result = DeviceSwitch.find_by_id(identifier, db=self.get_db_session())
    if result:
        logger.info(f'device {identifier} found')
