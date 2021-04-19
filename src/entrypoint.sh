#!/usr/bin/env bash
set -e
case $1 in
web)
  echo "Deploy web"
  alembic upgrade head
  python -m app.__main__
#	gunicorn -w ${WORKERS:-2} -b 0.0.0.0:5000 app.__main__:app --log-level=${LOG_LEVEL:-debug}
  ;;
worker)
  echo "Deploy worker"
  celery -A app.tasks.main worker -n default@%%h -l ${CELERY_LOG_LEVEL:-INFO}
  ;;
beat)
  echo "Deploy beat"
  celery -A app.tasks.main beat -l ${CELERY_LOG_LEVEL:-INFO}
  ;;
*)
  echo "Fail!"
  ;;
esac
