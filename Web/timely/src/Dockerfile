FROM python:3.9-slim-bullseye
WORKDIR /opt/chal

# gevent/greenlet ship manylinux wheels for CPython 3.9, so no build toolchain
# (and no apt, whose bullseye pool paths have since rotted) is needed.

COPY requirements.txt /opt/chal/

RUN pip install -r requirements.txt --no-cache-dir

COPY . /opt/chal

# hadolint ignore=SC2086
RUN adduser \
    --disabled-login \
    -u 1001 \
    --gecos "" \
    --shell /bin/bash \
    chal
RUN chmod +x /opt/chal/docker-entrypoint.sh

USER 1001
EXPOSE 8000
ENTRYPOINT ["/opt/chal/docker-entrypoint.sh"]
