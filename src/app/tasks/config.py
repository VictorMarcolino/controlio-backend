import re

from urllib.parse import urlparse
from kombu import Queue
from app.helper import get_config

__config = get_config()

broker_url = __config["BROKER_URL"]

broker_url_parsed = urlparse(broker_url)

if broker_url_parsed.scheme == 'amqps':
    broker_transport_options = {'login_method': 'PLAIN'}

if False:
    result_backend = __config["BACKEND_URL"]
    redis_retry_on_timeout = __config["REDIS_RETRY_ON_TIMEOUT"]
    redis_socket_keepalive = __config["REDIS_SOCKET_KEEPALIVE"]

task_create_missing_queues = True
result_expires = 60 * 60 * 3  # 3 hours
result_chord_join_timeout = 120
task_acks_late = True
task_reject_on_worker_lost = True
task_serializer = 'json'

task_default_queue = 'app'

task_queues = (
    Queue('app',
          routing_key='app.#'),
    Queue('io',
          routing_key='io.#'),
)

task_routes = ([
                   (re.compile(r'^(.*)_is_ready$'),
                    {'queue': 'io',
                     'routing_key': 'io.task'}),
                   ('*', {'queue': 'app'}),
               ],)

beat_schedule = {
    'task-every-x-minutes': {
        'task': 'app.tasks.periodic_tasks.foo1',
        'schedule': 60 * 5,
        'options': {
            'expires': 60 * 5,
            'rate_limit': '30/m'
        }
    },
}
