FROM heroku/heroku:22-build

ENV DEBIAN_FRONTEND noninteractive
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8
ENV PORT '80'
ENV PYTHONDONTWRITEBYTECODE 1

# -- Install
RUN apt-get update
RUN apt-get install language-pack-da python3-pip -y

RUN pip install responder typesystem==0.2.5

RUN set -ex && mkdir /app
WORKDIR /app
COPY . /app

CMD python3 main.py
EXPOSE 80
