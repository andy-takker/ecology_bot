FROM python:3.10-slim

RUN apt update && apt install -y --no-install-recommends build-essential wget unzip libssl-dev libffi-dev python-dev tzdata && rm -rf /var/lib/apt/lists/*
ENV TZ="Europe/Moscow"
RUN python3 -m pip install -U pip

WORKDIR /bot
ADD /requirements.txt /
RUN python3 -m pip install -r /requirements.txt --no-cache-dir

ARG TELEGRAM_BOT_TOKEN
ARG ADMINS

ARG POSTGRES_DB
ARG POSTGRES_PORT
ARG POSTGRES_USER
ARG POSTGRES_PASSWORD
ARG POSTGRES_HOST

ARG REDIS_HOST
ARG REDIS_PORT
ARG REDIS_PASSWORD

COPY ./bot /bot

