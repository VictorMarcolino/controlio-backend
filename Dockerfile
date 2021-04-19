FROM python:3.8
WORKDIR /usr/src
ENV PYTHONPATH /usr/src
ENV PYTHONUNBUFFERED 1

RUN apt-get update -y && \
apt-get upgrade -y && \
apt-get install libpq-dev python-dev -y
RUN apt install postgresql libpq-dev postgresql-client postgresql-client-common -y
# Install DEPS
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

#COPY FILES
COPY src /usr/src
ENTRYPOINT ["./entrypoint.sh"]