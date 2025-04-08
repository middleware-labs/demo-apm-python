import os
from django.core.wsgi import get_wsgi_application
from uwsgidecorators import postfork
from middleware import mw_tracker, MWOptions, record_exception, DETECT_AWS_EC2

@postfork
def tracing():
    mw_tracker()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_uwsgi_nginx_settings')
application = get_wsgi_application()

