FROM heroku/heroku:22-build

ENV DEBIAN_FRONTEND noninteractive
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1

# -- Install
RUN apt-get update
RUN apt-get install language-pack-da python3-pip -y

COPY requirements.txt .
RUN pip install -r requirements.txt

RUN set -ex && mkdir /app
WORKDIR /app
COPY . /app

CMD python3 main.py
EXPOSE 80
