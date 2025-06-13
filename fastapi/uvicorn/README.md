# Python FastAPI Application Instrumentation Guide
Follow our [documentation](https://docs.middleware.io/docs/apm-configuration/python/python-apm-setup) to setup APM for your python FastAPI application.

[![PyPI - Version](https://img.shields.io/pypi/v/middleware-io)](https://pypi.org/project/middleware-io/)


|  Traces  |  Metrics  |  Profiling  |  Logs (App/Custom)  |
|:--------:|:---------:|:-----------:|:-------------------:|
|   Yes    |    Yes    |     Yes     |       Yes/Yes       |

## Prerequisites
Ensure that you have the Middleware Host Agent installed to view Python demo data on your dashboard.

---------------------
## Setup Virtual Environment
```
python -m venv newenv
source newenv/bin/activate

pip install -r requirements.txt
```

## Install Middleware APM package
```shell
pip install middleware-io
```

## Install OpenTelemetry instrument libraries 
```shell
middleware-bootstrap -a install
```

## Run Your Application 

### Option 1 : With Host Agent
To run your application, use the following command:
```shell
middleware-run uvicorn main:app --host localhost --port 5002
```
### Option 2 : Serverless Setup
```shell
MW_API_KEY=******************* MW_TARGET=https://******.middleware.io:443 MW_SERVICE_NAME=fastapi-local OTEL_BSP_SCHEDULE_DELAY=10 OTEL_LOG_LEVEL=debug middleware-run uvicorn main:app --host localhost --port 5002
```
---------------------------------
## Run on Docker
1. Build: `docker build -t demo-python .`
2. Run: `docker run demo-python`
3. Debug: `docker run -it demo-python sh`

--------------
## Run on Google Cloud Run

gcloud run deploy fastapi-uvicorn \
  --image <IMAGE_NAME> \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 512Mi \
  --cpu 1 \
  --min-instances 0 \
  --max-instances 10 \
  --port 8000