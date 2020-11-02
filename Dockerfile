FROM python:3.8-slim
WORKDIR /usr/src
ENV PYTHONPATH /usr/src
ENV PYTHONUNBUFFERED 1

COPY requirements.txt requeriments.txt
RUN pip install -r requeriments.txt
# Install DEPS
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

#COPY FILES
COPY src /usr/src
ENTRYPOINT ["./entrypoint.sh"]