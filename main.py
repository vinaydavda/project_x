import uuid
import uvicorn
import logging
from fastapi import FastAPI
from pydantic import BaseModel
from app.models.events import create_event, fetch_latest_event_sequence
from sqlalchemy import func

_logger = logging.getLogger(__name__)
app = FastAPI()

# Product model declaration
class Product(BaseModel):
    name: str
    price: float

products_db: dict[Product] = {}
latest_id = 0

def get_event_data(aggregate_id, latest_event_sequence, event_type, product_data):
    return {
        "event_id": aggregate_id,
        "event_name": "product",
        "event_type": event_type,
        "event_sequence": latest_event_sequence + 1,
        "event_data": {
            "name": product_data.name,
            "price": product_data.price
        }
    }

# GET - Home page
@app.get("/")
def get_home():
    return {"info": "App is running..."}

# ----- Read Database -----

# GET - all products
@app.get("/products")
def read_products():
    try:
        return {"success": True, "data": products_db}
    except Exception as e:
        _logger.error(f"> [ERROR] - Error returning products: {e}")
        return {"success": False, "error": "Error returning products"}

# ----- Write Database -----

# POST - Add new product
@app.post("/products")
def add_product(product_data: Product):
    try:
        latest_event_sequence = 0  # Add product will be first event on a product
        aggregate_id = f"product_{str(uuid.uuid4())}"
        event_data = get_event_data(aggregate_id, latest_event_sequence, "PRODUCT_CREATE", product_data)
        
        create_event(event_data)
        return {"success": True, "product_id": aggregate_id}
    except Exception as e:
        _logger.error(f"> [ERROR] - Error adding products: {e}")
        return {"success": False, "error": "Error adding products"}
    
@app.put("/products/{product_id}")
def update_product(product_id: int, product_data: Product):
    try:
        latest_event_sequence = fetch_latest_event_sequence(product_id)  # Add product will be first event on a product
        
        if latest_event_sequence:
            event_data = get_event_data(product_id, latest_event_sequence, "PRODUCT_UPDATE", product_data)
            create_event(event_data)
            return {"success": True, "product_id": product_id}
        else:
            return {"success": False, "error": "Product not found"}
    except Exception as e:
        _logger.error(f"> [ERROR] - Error updating products: {e}")
        return {"success": False, "error": "Error updating update"}
    
@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    try:
        latest_event_sequence = fetch_latest_event_sequence(product_id)  # Add product will be first event on a product
        
        if latest_event_sequence:
            event_data = get_event_data(product_id, latest_event_sequence, "PRODUCT_DELETE")
            create_event(event_data)
            return {"success": True, "product_id": product_id}
        else:
            return {"success": False, "error": "Product not found"}
    except Exception as e:
        _logger.error(f"> [ERROR] - Error deleting products: {e}")
        return {"success": False, "error": "Error deleting product"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
