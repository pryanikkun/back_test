FROM python:3.11-alpine
WORKDIR /usr/src
COPY ./requirements.txt /requirements.txt
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev bash
RUN pip install --no-cache-dir --upgrade -r /requirements.txt
COPY . .