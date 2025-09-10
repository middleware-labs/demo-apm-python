# Copyright The OpenTelemetry Authors
# SPDX-License-Identifier: Apache-2.0

FROM python:3.11-slim-bullseye as base

#
# Fetch requirements
#
FROM base as builder
RUN apt-get -qq update \
    && apt-get install -y --no-install-recommends g++ \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app/
COPY ./requirements.txt ./

RUN pip install --upgrade pip
RUN pip install --prefix="/reqs" -r requirements.txt
#
# Runtime
#
FROM base as runtime
WORKDIR /usr/src/app/
COPY --from=builder /reqs /usr/local
COPY ./ ./

ENV GIT_PYTHON_REFRESH=quiet
ENV MW_TRACKER=True
ENV MW_AGENT_SERVICE="172.17.0.1"

RUN python3 manage.py migrate
RUN python3 manage.py createsuperuser --username admin --email admin@mail.com
RUN middleware-bootstrap -a install 

CMD ["sh", "-c", "DJANGO_SETTINGS_MODULE='helloworld.settings' middleware-run python3 manage.py runserver 0.0.0.0:8000"]