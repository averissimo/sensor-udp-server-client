FROM python:3.6.9-alpine

RUN pip install --upgrade pip

ENV DATABASE_HOST=localhost DATABASE_PORT=8086 DATABASE_USER=root DATABASE_PASSWD=root DATABASE_TABLE=example

RUN mkdir /usr/src/app

WORKDIR /usr/src/app

COPY ./server/requirements.txt .

RUN pip install -r requirements.txt

COPY ./server/ /usr/src/app/

EXPOSE 20001/udp


CMD ["python3", "-u",  "server.py"]
