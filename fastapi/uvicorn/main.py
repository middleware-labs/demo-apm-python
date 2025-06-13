import logging
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
import os
import time
import random
import httpx
from typing import Dict, List
# Import routers
from routers import users, items, orders

# from opentelemetry import trace
# from opentelemetry.propagate import set_global_textmap
# from opentelemetry.propagators.cloud_trace_propagator import (
#     CloudTraceFormatPropagator,
# )

app = FastAPI(
    title="E-commerce API",
    description="A FastAPI project with intentional bugs for debugging practice",
    version="1.0.0"
)

# # trace.get_tracer_provider().add_span_processor(CloudTraceSpanExporter())
# set_global_textmap(CloudTraceFormatPropagator())

# Include routers
app.include_router(users.router)
app.include_router(items.router)
app.include_router(orders.router)

logging.getLogger().setLevel(logging.INFO)

# Internal API endpoints
@app.get("/internal/user/{user_id}")
async def get_user_details(user_id: str):
    time.sleep(random.uniform(0.1, 0.2))
    return {"user_id": user_id, "name": f"User {user_id}", "preferences": {"theme": "dark"}}

@app.get("/internal/orders/{user_id}")
async def get_user_orders(user_id: str):
    time.sleep(random.uniform(0.15, 0.25))
    return {"orders": [{"id": f"ORD{i}", "amount": random.randint(100, 1000)} for i in range(3)]}

@app.get("/internal/analytics/{user_id}")
async def get_user_analytics(user_id: str):
    time.sleep(random.uniform(0.2, 0.3))
    return {
        "total_orders": random.randint(5, 20),
        "average_order_value": random.randint(50, 200),
        "last_purchase": "2024-03-15"
    }

@app.get("/internal/recommendations/{user_id}")
async def get_recommendations(user_id: str):
    time.sleep(random.uniform(0.1, 0.2))
    return {
        "recommendations": [
            {"id": f"PROD{i}", "score": random.uniform(0.5, 1.0)}
            for i in range(5)
        ]
    }

@app.get("/")
def read_root():
    logging.info("Hello World")
    return {
        "message": "Welcome to the E-commerce API",
        "documentation": "/docs",
        "version": "1.0.0"
    }

def simulate_database_query():
    time.sleep(random.uniform(0.1, 0.3))
    return {"rows": 100, "status": "success"}

def simulate_api_call():
    time.sleep(random.uniform(0.2, 0.4))
    return {"status": "success", "data": {"id": 123, "name": "test"}}

def process_data(data):
    time.sleep(random.uniform(0.1, 0.2))
    return {"processed": True, "data": data}

def transform_data(data):
    time.sleep(random.uniform(0.05, 0.1))
    return {"transformed": True, "data": data}

def cache_operation():
    time.sleep(random.uniform(0.05, 0.1))
    return {"cached": True}

async def fetch_user_data(user_id: str) -> Dict:
    async with httpx.AsyncClient() as client:
        # Fetch user details
        user_details = await client.get(f"http://localhost:8000/internal/user/{user_id}")
        user_data = user_details.json()
        
        # Fetch user orders
        orders = await client.get(f"http://localhost:8000/internal/orders/{user_id}")
        user_data["orders"] = orders.json()["orders"]
        
        # Fetch user analytics
        analytics = await client.get(f"http://localhost:8000/internal/analytics/{user_id}")
        user_data["analytics"] = analytics.json()
        
        return user_data

async def process_user_recommendations(user_id: str, user_data: Dict) -> List[Dict]:
    async with httpx.AsyncClient() as client:
        # Get recommendations
        recommendations = await client.get(f"http://localhost:8000/internal/recommendations/{user_id}")
        recs = recommendations.json()["recommendations"]
        
        # Process recommendations based on user data
        processed_recs = []
        for rec in recs:
            if user_data["analytics"]["total_orders"] > 10:
                rec["score"] *= 1.2
            processed_recs.append(rec)
        
        return processed_recs

@app.get("/complex-operation")
async def complex_operation():

    print(os.getenv("MW_API_KEY", "default_value"))
    print(os.getenv("MW_TARGET", "default"))
    print(os.getenv("MW_SERVICE_NAME", "default"))
    print(os.getenv("OTEL_PROPAGATORS", "default"))
    # Generate a random user ID
    user_id = f"user_{random.randint(1000, 9999)}"
    
    # Simulate database query
    db_result = simulate_database_query()
    
    # Simulate external API call
    api_result = simulate_api_call()
    
    # Fetch user data (this will make multiple internal API calls)
    user_data = await fetch_user_data(user_id)
    
    # Process user data
    process_result = process_data(user_data)
    
    # Transform data
    transform_result = transform_data(process_result)
    
    # Get and process recommendations
    recommendations = await process_user_recommendations(user_id, user_data)
    
    # Simulate cache operation
    cache_result = cache_operation()
    
    return {
        "status": "success",
        "message": "Complex operation completed",
        "details": {
            "database_operation": db_result,
            "api_call": api_result,
            "user_data": user_data,
            "data_processing": process_result,
            "data_transformation": transform_result,
            "recommendations": recommendations,
            "cache_operation": cache_result
        }
    }

if __name__ == "__main__":
    import uvicorn

    uvicorn.run('main:app', reload=True)