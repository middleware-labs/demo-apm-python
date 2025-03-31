# Copyright The OpenTelemetry Authors
# SPDX-License-Identifier: Apache-2.0


FROM python:3.11-slim-bullseye as base

RUN apt-get -qq update \
    && apt-get install -y --no-install-recommends g++ \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app/
COPY ./requirements.txt ./
COPY ./ ./
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install middleware-io==2.1.2rc16
RUN middleware-bootstrap -a install

ENTRYPOINT [ "middleware-run", "flask", "run" ]