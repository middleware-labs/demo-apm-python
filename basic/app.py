from flask import Flask, jsonify, request
import traceback
import logging
from functools import wraps 
from opentelemetry import trace, metrics
from opentelemetry.trace.status import StatusCode


from middleware import MwTracker
tracker=MwTracker()

# Initialize Flask app
app = Flask(__name__)

# Trace provider
tracer = trace.get_tracer("custom-tracer")

# Metric provider
meter = metrics.get_meter("custom-meter")

# Setup Python logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Custom Metrics: Counter
request_counter = meter.create_counter(
    name="requests_total",
    description="Total number of requests",
    unit="1"
)

# Custom Traces: Tracing decorator with error handling
def trace_request(func):
    @wraps(func)  # Preserve the original function's name and docstring
    def wrapper(*args, **kwargs):
        with tracer.start_as_current_span(func.__name__) as span:
            span.set_attribute("custom.attribute", "example_value")

            # Log the trace and span IDs
            span_context = span.get_span_context()
            logger.info(f"Start processing {func.__name__}: trace_id={span_context.trace_id}, span_id={span_context.span_id}")
            
            try:
                result = func(*args, **kwargs)

                # Only check status code for POST request handling
                if request.method == 'POST':
                    if result.status_code >= 400:
                        span.set_status(StatusCode.ERROR)
                        logger.error(f"Error occurred in {func.__name__}: status_code={result.status_code}")

                return result

            except Exception as e:
                span.set_status(StatusCode.ERROR)
                span.record_exception(e)
                logger.error(f"Exception occurred in {func.__name__}: {str(e)}")
                logger.error(f"Stack Trace:\n{traceback.format_exc()}")  # Log the full stack trace
                return jsonify({"error": "An internal error occurred"}), 500
    return wrapper

@app.route('/')
@trace_request
def home():
    request_counter.add(1, {"endpoint": "home"})
    logger.info("Home endpoint accessed")
    return jsonify({"message": "Welcome to the Flask app!"})

@app.route('/process', methods=['GET', 'POST'])
@trace_request
def process_data():
    if request.method == 'GET':
        # Render a simple HTML form for demonstration
        return '''
            <form method="POST">
                <label for="data">Enter some data (JSON format):</label><br>
                <textarea id="data" name="data" rows="4" cols="50"></textarea><br>
                <input type="submit" value="Submit">
            </form>
        '''
    
    if request.method == 'POST':
        # Process JSON data submitted via the form
        try:
            data = request.json if request.is_json else request.form.get('data')
            request_counter.add(1, {"endpoint": "process"})
            logger.info(f"Processing data: {data}")
            
            with tracer.start_as_current_span("data_processing") as span:
                span.set_attribute("request.data", str(data))
                # Simulate processing
                processed_data = {"processed": data}
                logger.info("Data processed successfully")

            response = jsonify(processed_data)  # Create response object

            return response  # Return the response object

        except Exception as e:
            span.set_status(StatusCode.ERROR)
            span.record_exception(e)
            logger.error(f"Exception occurred in process_data: {str(e)}")
            logger.error(f"Stack Trace:\n{traceback.format_exc()}")
            return jsonify({"error": "An internal error occurred"}), 500

@app.route('/error')
@trace_request
def error():
    request_counter.add(1, {"endpoint": "error"})
    logger.warning("Error endpoint accessed, simulating an error")
    
    # Simulate an exception to trigger stack trace logging
    raise ValueError("Simulated internal server error")

if __name__ == '__main__':
    app.run(port=5000)