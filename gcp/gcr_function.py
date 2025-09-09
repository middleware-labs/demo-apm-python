# gcr : Google Cloud Run

from middleware import mw_tracker, MWOptions, DETECT_GCP
from opentelemetry import trace

# Initialize Middleware tracker at startup
mw_tracker(
    MWOptions(
        access_token="whkvkobudfitutobptgonaezuxpjjypnejbb",
        target="https://myapp.middleware.io:443",
        service_name="MyPythonApp",
        otel_propagators="b3,tracecontext",
        detectors=[DETECT_GCP],   # Use GCP detector here, not AWS
        collect_metrics=False,
        debug_log_file=True,
        log_level="DEBUG",
    )
)

tracer = trace.get_tracer("custom-tracer")

import functions_framework

@functions_framework.http
def hello_http(request):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
        <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.
    """
    with tracer.start_as_current_span("gcp_function_handler"):
        request_json = request.get_json(silent=True)
        request_args = request.args

        if request_json and 'name' in request_json:
            name = request_json['name']
        elif request_args and 'name' in request_args:
            name = request_args['name']
        else:
            name = 'World'
        if name:
            trace.get_current_span().set_attribute("endpoint", f"http:127.0.0.1:8080/?name={name}")
        else:
            trace.get_current_span().set_attribute("endpoint", "http:127.0.0.1:8080/")
        return 'Hello {}!'.format(name)
