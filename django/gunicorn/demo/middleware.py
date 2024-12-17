import time
import logging
import uuid

logger = logging.getLogger("django")

class RequestTimingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Start timing the request
        start_time = time.time()

        # Generate a unique transaction ID
        txn_id = str(uuid.uuid4())

        response = self.get_response(request)

        # Calculate the total request time
        end_time = time.time()
        total_time = (end_time - start_time) * 1000  # Convert to milliseconds

        # Collect timing data (this is a placeholder for demonstration)
        timing_data = {
            "UserIdAuthentication.authenticate": 3067.38018989563,
            "MeterInfoSerializer.get_meter_id_method": 0.3600120544433594,
            "get_message_id": 305.07397651672363,
            "VendClient.confirm_meter_request": 921.360969543457,
            "VerifyMeterSerializer.create": 1227.1349430084229,
            "req_overall": total_time,
        }

        # Log the request timing data
        logger.info(
            "req timing stats",
            extra={
                "timing_data": timing_data,
                "req_path": request.path,
                "req_method": request.method,
                "user_id": str(uuid.uuid4()),  # Placeholder for user ID
                "txn_id": txn_id,
            },
        )

        return response
