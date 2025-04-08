import logging
import os
from typing import Union
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv

from middleware import mw_tracker, MWOptions

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Set logging level
logging.getLogger().setLevel(logging.INFO)

# Sample APIs
@app.get("/")
def read_root():
    logging.info("Root API accessed")
    return {"message": "Welcome to the API"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    logging.debug("Item ID: %s", item_id)
    return {"item_id": item_id, "query": q}

@app.post("/create")
def create_item(name: str, price: float):
    logging.info("Item created: %s", name)
    return {"name": name, "price": price}

@app.put("/update/{item_id}")
def update_item(item_id: int, name: str):
    logging.info("Item updated: %d", item_id)
    return {"item_id": item_id, "updated_name": name}

@app.delete("/delete/{item_id}")
def delete_item(item_id: int):
    logging.info("Item deleted: %d", item_id)
    return {"message": f"Item {item_id} deleted"}

@app.get("/error")
def generate_error():
    logging.error("Error generated")
    raise HTTPException(status_code=500, detail="Simulated error")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=5002, reload=True)
