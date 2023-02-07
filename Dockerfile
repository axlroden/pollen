FROM heroku/heroku:22-build

ENV DEBIAN_FRONTEND noninteractive
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8
# Python, don't write bytecode!
ENV PYTHONDONTWRITEBYTECODE 1

# -- Install Pipenv:
RUN apt update && apt upgrade -y && apt install python3.10-dev libffi-dev language-pack-da -y
RUN curl --silent https://bootstrap.pypa.io/get-pip.py | python3.10

# Backwards compatility.
RUN rm -fr /usr/bin/python3 && ln /usr/bin/python3.10 /usr/bin/python3

RUN pip3 install pipenv

# -- Install Application into container:
RUN set -ex && mkdir /app

WORKDIR /app

# -- Adding Pipfiles
COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock

# -- Install dependencies:
RUN set -ex && pipenv install --deploy --system

ENV PORT '80'
COPY . /app
CMD python3 main.py
EXPOSE 80
