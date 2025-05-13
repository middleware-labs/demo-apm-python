import logging
from fastapi import FastAPI
from dotenv import load_dotenv
import os

from middleware import mw_tracker, MWOptions
mw_tracker(
    MWOptions(
        access_token="whkvkobudfitutobptgonaezuxpjjypnejbb",
        target="https://myapp.middleware.io:443",
        service_name="MyPythonApp",
    )
)

# Import routers
from routers import users, items, orders

app = FastAPI(
    title="E-commerce API",
    description="A FastAPI project with intentional bugs for debugging practice",
    version="1.0.0"
)

# Include routers
app.include_router(users.router)
app.include_router(items.router)
app.include_router(orders.router)

logging.getLogger().setLevel(logging.INFO)

@app.get("/")
def read_root():
    logging.info("Hello World")
    return {
        "message": "Welcome to the E-commerce API",
        "documentation": "/docs",
        "version": "1.0.0"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run('main:app', reload=True)