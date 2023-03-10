FROM heroku/heroku:22-build

ENV DEBIAN_FRONTEND noninteractive
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1

RUN --mount=target=/var/lib/apt/lists,type=cache,sharing=locked \
    --mount=target=/var/cache/apt,type=cache,sharing=locked \
    rm -f /etc/apt/apt.conf.d/docker-clean \
    && apt-get update \
    && apt-get -y --no-install-recommends install \
        language-pack-da language-pack-da-base \
        python3-pip python3-pkg-resources python3-setuptools python3-wheel

COPY requirements.txt .
RUN pip install -r requirements.txt

RUN set -ex && mkdir /app
WORKDIR /app
COPY . /app

CMD python3 main.py
EXPOSE 80
