import time
import requests
import asyncio
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor, ConsoleSpanExporter
from opentelemetry.instrumentation.aws_lambda import AwsLambdaInstrumentor

# Initialize OpenTelemetry tracing
provider = TracerProvider()
processor = SimpleSpanProcessor(ConsoleSpanExporter())  # Exports to console for debugging
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)

# Instrument the tracer provider with OpenTelemetry for Lambda
AwsLambdaInstrumentor().instrument_tracer_provider()

# Get the OpenTelemetry tracer
tracer = trace.get_tracer(__name__)

# Function to make an HTTP GET request
def get_request():
    url = "https://opentelemetry.io/"
    try:
        start_time = time.time()
        response = requests.get(url, timeout=(2, 5))  # (connection timeout, read timeout)
        duration = time.time() - start_time
        print(f"Request completed in {duration:.2f} seconds")
        return response.status_code
    except requests.Timeout:
        raise Exception("Request timed out")
    except requests.RequestException as err:
        raise Exception(f"HTTP Request failed: {err}")

# Lambda handler function
def lambda_handler(event, context):
    try:
        # Start a tracing span for the Lambda function execution
        with tracer.start_as_current_span("LambdaFunctionExecution"):
            # Log the start time of the Lambda execution
            start_time = time.time()

            # Make the external HTTP request
            result = get_request()

            # Log the total execution time
            print(f"Total execution time: {time.time() - start_time:.2f} seconds")

            # Add a custom event and attributes to the current span
            current_span = trace.get_current_span()
            current_span.add_event("CustomEvent", {"description": "This is a custom event"})
            current_span.set_attribute("http.status_code", result)

        # Return the successful response
        return {
            "statusCode": 200,
            "body": f"Request completed with status code {result}"
        }

    # Handle any exceptions and return a 400 response
    except Exception as error:
        return {
            "statusCode": 400,
            "body": str(error)
        }

