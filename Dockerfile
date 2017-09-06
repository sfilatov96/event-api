FROM python:3.5

COPY . /event-api

WORKDIR /event-api

ENV APP_HOST "0.0.0.0"
ENV APP_PORT 5000
ENV MONGO_HOST "127.0.0.1"
ENV MONGO_PORT 27017

EXPOSE $APP_PORT

RUN pip3 install -r requirements.txt

CMD python3 run.py

