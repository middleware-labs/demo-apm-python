from middleware import mw_tracker, MWOptions, DETECT_GCP, record_exception
import logging

mw_tracker(
    MWOptions(
        access_token="whkvkobudfitutobptgonaezuxpjjypnejbb",
        target="https://myapp.middleware.io:443",
        service_name="MyPythonApp",
        otel_propagators="b3,tracecontext",
        detectors=[],
        collect_metrics=False,  # collect metrics
        debug_log_file=False,  # add to console log telemetry data
        log_level="DEBUG",
    )
)

from flask import Flask, request
from opentelemetry import trace

tracer = trace.get_tracer(__name__)
app = Flask(__name__)
@app.route("/", methods=["GET", "POST"])
def hello_world():
    with tracer.start_as_current_span("gcp_function") as span:
        try:
            1/0
        except Exception as e:
                span.record_exception(e)
        request_json = request.get_json(silent=True)
        request_args = request.args
        if request_json and 'name' in request_json:
            name = request_json['name']
        elif request_args and 'name' in request_args:
            name = request_args['name']
        else:
            name = 'World'
        trace.get_current_span().set_attribute("endpoint", f"http://127.0.0.1:8080/?name={name}")
        logging.info(f"custom endpoint log.\nThe endpoint hit is : http://127.0.0.1:8080/?name={name}")
        return f'Hello, {name}!'

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=False)