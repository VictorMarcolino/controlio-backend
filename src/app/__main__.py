from flask import Flask

from src.app.blueprints import default_api
from src.app.tasks import create_celery
from sqlalchemy import create_engine
from src.app.blueprints.health import health

from src.app.models import Base, db_session
from src.app.helper import get_config
from urllib.parse import urlparse, parse_qs
import os
import logging
import sentry_sdk


def create_database(config=None):
    if not config:
        config = get_config()

    engine = create_engine(config['database_url'], convert_unicode=True)
    Base.metadata.create_all(engine)


def bind_database():
    from flask import current_app as app
    database_uri = app.config['database_url']

    parsed = urlparse(database_uri)
    kwargs = {}
    if parsed.scheme in ['postgres', 'postgresql']:
        kwargs['pool_size'] = 10
        kwargs['pool_pre_ping'] = True
        kwargs['max_overflow'] = 10
        kwargs['pool_recycle'] = 3600
        query = parse_qs(parsed.query)
        if 'sslmode' in query:
            kwargs['connect_args'] = {'sslmode': query['sslmode'][0]}

    engine = create_engine(database_uri, convert_unicode=True, **kwargs)
    db_session.configure(bind=engine)


def create_app():
    config = get_config()
    if config.get('create_database', False):
        create_database(config)

    app = Flask(__name__)
    is_gunicorn = "gunicorn" in os.environ.get("SERVER_SOFTWARE", "")
    if is_gunicorn:
        gunicorn_logger = logging.getLogger('gunicorn.error')
        app.logger.handlers = gunicorn_logger.handlers
        app.logger.setLevel(gunicorn_logger.level)

    app.config.update(config)

    with app.app_context():
        bind_database()

    app.secret_key = 'secret_key'
    app.register_blueprint(health, url_prefix='/health')
    app.register_blueprint(default_api, url_prefix='/api')
    app.debug = True

    sentry_url = config['SENTRY_URL']
    if sentry_url:
        sentry_sdk.init(sentry_url)

    create_celery()
    return app


app = create_app()


@app.teardown_appcontext
def cleanup(response):
    db_session.remove()


if __name__ == '__main__':
    app.run(port=5000, host="0.0.0.0", debug=True)
