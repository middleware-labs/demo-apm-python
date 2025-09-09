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
RUN pip install middleware-io
RUN middleware-bootstrap -a install 

#
# Runtime
#
FROM base as runtime
WORKDIR /usr/src/app/
COPY --from=builder /reqs /usr/local
COPY ./ ./

ENV GIT_PYTHON_REFRESH=quiet

RUN python3 manage.py migrate
RUN python3 manage.py createsuperuser --username admin --email admin@mail.com
ENV DJANGO_SETTINGS_MODULE="demo.settings"
ENTRYPOINT ["middleware-run", "gunicorn", "-c", "conf/gunicorn.conf.py", "--workers=4", "--bind", "0.0.0.0:8000", "--timeout", "120", "demo.wsgi"]

EXPOSE 8000
