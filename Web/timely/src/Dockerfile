FROM python:3.9-slim-buster
WORKDIR /opt/chal

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        python3-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

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
