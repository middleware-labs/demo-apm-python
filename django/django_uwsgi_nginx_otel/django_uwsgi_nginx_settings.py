SECRET_KEY = 'replace-with-a-secure-key'
DEBUG = True
ALLOWED_HOSTS = ['*']
ROOT_URLCONF = 'django_uwsgi_nginx_urls'
WSGI_APPLICATION = 'django_uwsgi_nginx_wsgi.application'

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.staticfiles',
    'sample_app',
]

MIDDLEWARE = [
    'django.middleware.common.CommonMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [],
        },
    },
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    }
}

STATIC_URL = '/static/'
STATIC_ROOT = '/static/'
