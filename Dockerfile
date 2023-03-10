FROM python:3.10.0-alpine

COPY requirements.txt .
RUN pip install -r requirements.txt

RUN set -ex && mkdir /app
WORKDIR /app
COPY app /app

CMD python3 main.py
EXPOSE 80
