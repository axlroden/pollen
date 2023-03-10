FROM heroku/heroku:22-build

ENV DEBIAN_FRONTEND noninteractive
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8
# Python, don't write bytecode!
ENV PYTHONDONTWRITEBYTECODE 1

# -- Install
RUN apt update && apt install language-pack-da python3-pip -y

RUN pip install responder typesystem==0.2.5

# -- Install Application into container:
RUN set -ex && mkdir /app

WORKDIR /app

ENV PORT '80'
COPY . /app
CMD python3 main.py
EXPOSE 80
