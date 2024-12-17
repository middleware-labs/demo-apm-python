import time
import logging
import uuid
from django.http import JsonResponse

logger = logging.getLogger("django")

def extra_endpoint(request):
    # Start timing the request
    start_time = time.time()
    
    # Generate unique transaction and user IDs (placeholders)
    user_id = str(uuid.uuid4())
    txn_id = str(uuid.uuid4())

    # Simulate some processing logic
    time.sleep(0.2)  # Simulated delay

    # Collect timing data
    timing_data = {
        "ExtraEndpoint.process": (time.time() - start_time) * 1000  # Time in milliseconds
    }

    # Log the request timing data
    logger.info(
        "req timing stats",
        extra={
            "timing_data": timing_data,
            "req_path": request.path,
            "req_method": request.method,
            "user_id": user_id,
            "txn_id": txn_id,
        },
    )

    # Prepare response data
    data = {
        "message": "This is an extra endpoint!",
        "txn_id": txn_id,
        "user_id": user_id,
    }
    return JsonResponse(data)
