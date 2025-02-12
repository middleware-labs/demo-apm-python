from django.urls import path
from .views import api_endpoint, html_page, raise_exception

urlpatterns = [
    path('api/', api_endpoint, name='api'),
    path('page/', html_page, name='html_page'),
    path('error/', raise_exception, name='raise_exception'),
]
