FROM        python:3.7-slim-stretch as trader

RUN apt-get update && apt-get install -y python3-tk #libx11-dev

ENV         PYTHONUNBUFFERED 1
ENV         PYTHONDONTWRITEBYTECODE 1

RUN mkdir   /usr/src/trader
WORKDIR     /usr/src/trader

COPY        requirements.txt /usr/src/trader/requirements.txt 
RUN         pip3 install -r requirements.txt

ENV         PYTHONPATH /usr/src/trader:$PYTHONPATH
COPY        . /usr/src/trader
