import uvicorn
import logging
from fastapi import FastAPI
from pydantic import BaseModel

_logger = logging.getLogger(__name__)
app = FastAPI()

# Product model declaration
class Product(BaseModel):
    name: str
    price: float

products_db: dict[Product] = {}
latest_id = 0

# GET - Home page
@app.get("/")
def get_home():
    return {"info": "App is running..."}

# GET - all products
@app.get("/products")
def read_products():
    try:
        return {"success": True, "data": products_db}
    except Exception as e:
        _logger.error(f"> [ERROR] - Error returning products: {e}")
        return {"success": False, "error": "Error returning products"}

# POST - Add new product
@app.post("/products")
def add_product(product_data: Product):
    try:
        global latest_id
        new_id = latest_id + 1
        products_db[new_id] = product_data
        latest_id = new_id
        return {"success": True, "product_id": latest_id}
    except Exception as e:
        _logger.error(f"> [ERROR] - Error adding products: {e}")
        return {"success": False, "error": "Error adding products"}
    
@app.put("/products/{product_id}")
def add_product(product_id: int, product_data: Product):
    try:
        if product_id in products_db:
            products_db[product_id] = product_data
            return {"success": True}
        return {"success": False, "error": "Product not found"}
    except Exception as e:
        _logger.error(f"> [ERROR] - Error updating products: {e}")
        return {"success": False, "error": "Error updating update"}
    
@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    try:
        if product_id in products_db:
            del products_db[product_id]
            return {"success": True}
        return {"success": False, "error": "Product not found"}
    except Exception as e:
        _logger.error(f"> [ERROR] - Error deleting products: {e}")
        return {"success": False, "error": "Error deleting product"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
