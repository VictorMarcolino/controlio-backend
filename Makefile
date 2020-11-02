default:
	echo "look the commands"
docker:
	docker-compose up --build -V --remove-orphans
worker:
	export PYTHONPATH=$(pwd)/src && celery -A app.tasks.main worker -n default@%%h -l INFO
beat:
	export PYTHONPATH=$(pwd)/src && celery -A app.tasks.main beat -l INFO
app:
	export PYTHONPATH=$(pwd)/src && cd src && alembic upgrade head
	gunicorn -w ${WORKERS:-2} -b 0.0.0.0:5000 app.__main__:app --log-level=${LOG_LEVEL:-debug}
alembic_revision:
	export PYTHONPATH=$(pwd)/src && cd src && alembic revision --autogenerate