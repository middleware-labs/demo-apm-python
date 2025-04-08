FROM python:3.10
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
ENV DJANGO_SETTINGS_MODULE=django_uwsgi_nginx_settings
RUN ls -l /app && python manage.py collectstatic --noinput

# replace with your Middleware API key
ENV MW_API_KEY="whkvkobudfitutobptgonaezuxpjjypnejbb" 

# replace with your Middleware App name
ENV MW_SERVICE_NAME="MyPythonApp"

# replace with your Middleware App url for serverless
ENV MW_TARGET="https://myapp.middleware.io:443"

# enable Middleware Console Exporter for logs and debug
ENV MW_CONSOLE_EXPORTER=True
ENV MW_DEBUG_LOG_FILE=True
ENV MW_LOG_LEVEL=DEBUG

# attach middleware-run to the entrypoint for instrumentation
CMD ["middleware-run","uwsgi", "--http", ":8000", "--module", "django_uwsgi_nginx_wsgi", "--static-map", "/static=/static"]
