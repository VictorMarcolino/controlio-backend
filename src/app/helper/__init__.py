from os import environ as env


def get_env_typed(evar, default_value=None, default_type=int):
    _result = env.get(evar, default_value)
    return default_type(_result)


def get_config() -> dict:
    configs = {
        'BROKER_URL': env.get('BROKER_URL', 'amqp://rabbitmq:rabbitmq@localhost:5672'),
        'MODE': env.get('MODE', 'worker').lower() == 'worker',
        'BACKEND_URL': env.get('BACKEND_URL', 'redis://localhost/2'),
        'REDIS_RETRY_ON_TIMEOUT': env.get('REDIS_RETRY_ON_TIMEOUT', 'false').lower() == 'true',
        'REDIS_SOCKET_KEEPALIVE': env.get('REDIS_SOCKET_KEEPALIVE', 'false').lower() == 'true',
        # GERAL

        'web_database_url': env.get('WEB_DATABASE_URL', 'sqlite:////tmp/dev.db'),
        'database_url': env.get('DATABASE_URL', 'sqlite:////tmp/dev.db'),
        'worker_database_url': env.get('WORKER_DATABASE_URL', 'sqlite:////tmp/dev.db'),
        'create_database': True if env.get('CREATE_DATABASE', 'false').lower() == 'true' else False,
        'workflow_timeout': get_env_typed('WORKFLOW_TIMEOUT', 10 * 60),
        'time_to_wait_for_service_result': get_env_typed('TIME_TO_WAIT_FOR_SERVICE_RESULT', 60 * 60),
        'extra_retries': get_env_typed('EXTRA_RETRIES', 0),
        'lock_expire': get_env_typed('LOCK_EXPIRE', 10),
        # SENTRY

        'SENTRY_URL': env.get('SENTRY_URL', False),
    }

    return configs
