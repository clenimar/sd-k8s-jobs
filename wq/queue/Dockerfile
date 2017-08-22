FROM gliderlabs/alpine:3.2

RUN apk-install python

ADD requirements.txt /

RUN apk --update add --virtual build-dependencies py-pip \
  && pip install -r requirements.txt \
  && apk del build-dependencies

ADD generator.py /
ADD ../rediswq.py /
