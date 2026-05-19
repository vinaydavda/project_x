from app.db.mongodb import mongo_db, products_collection


def create_product(data):
    products_collection.insert_one(data)


def update_product(product_id, data):
    print(" -- UPDATE IN DB --")
    products_collection.update_one(
        {"id": product_id},
        {
            "$set": data
        }
    )

def delete_product(product_id):
    products_collection.update_one(
        {"id": product_id},
        {
            "$set": {"active": False}
        }
    )


def get_product(product_id):
    return products_collection.find_one({
        "id": product_id
    })


def get_all_products(limit=None):
    result = products_collection.find().sort("name",1)
    if limit:
        return result.limit(limit)
    return result