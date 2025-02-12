import os
from django.core.wsgi import get_wsgi_application

from uwsgidecorators import postfork

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

@postfork
def init_tracing():
    resource = Resource.create(attributes={
        "service.name": "django-uwsgi-otel"
    })

    trace.set_tracer_provider(TracerProvider(resource=resource))
    span_processor = BatchSpanProcessor(
        OTLPSpanExporter(endpoint="http://localhost:9319")
    )
    trace.get_tracer_provider().add_span_processor(span_processor)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_uwsgi_nginx_settings')
application = get_wsgi_application()

