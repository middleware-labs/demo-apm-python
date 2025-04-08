# Django Application with uWSGI, Nginx, and Middleware Integration Guide

This project demonstrates how to set up a **Django** application with **uWSGI** and **Nginx**, along with **Middleware** integration for Application Performance Monitoring (APM).

Follow the [Middleware APM setup documentation](https://docs.middleware.io/docs/apm-configuration/python/python-apm-setup) to integrate APM with your Django application.

[![PyPI - Version](https://img.shields.io/pypi/v/middleware-io)](https://pypi.org/project/middleware-io/)

| Traces | Metrics | Profiling | Logs (App/Custom) |
|:------:|:-------:|:---------:|:-----------------:|
|   Yes  |    Yes  |    Yes    |      Yes/Yes      |

## Prerequisites

Before running the project, ensure you have the **Middleware Host Agent** installed to view Python demo data on your dashboard.

---

## Steps to Run the Project

Create and Activate Virtual Environment:

```python
python3 -m venv env
source env/bin/activate
```

Install Dependencies

```
pip install -r requirements.txt
```

Install OpenTelemetry instrument libraries 

```python
middleware-bootstrap -a install
```

Run the Application

```
docker compose up --build
```

Command for App Instrumentation

```python
DJANGO_SETTINGS_MODULE="django_uwsgi_nginx_settings" middleware-run uwsgi  --http  :8000  --module django_uwsgi_nginx_wsgi  --static-map  /static=/static
```

If you are running this application in a serverless setup consider adding `MW_API_KEY` and `MW_TARGET` as mentioned in the command below :

```python
MW_API_KEY=********** MW_TARGET=https://*****.middleware.io:443 DJANGO_SETTINGS_MODULE="django_uwsgi_nginx_settings" middleware-run uwsgi  --http  :8000  --module django_uwsgi_nginx_wsgi  --static-map  /static=/static
```