FROM ubuntu:14.04

RUN apt-get -qq update && apt-get -qq install -y curl apt-transport-https ca-certificates amqp-tools python --no-install-recommends

COPY ./find-hash.py /find-hash.py

RUN rm -rf /var/lib/apt/lists/*

CMD  /usr/bin/amqp-consume --url=amqp://guest:guest@rabbitmq-service:5672 -q job -c 1 cat | python find-hash.py
