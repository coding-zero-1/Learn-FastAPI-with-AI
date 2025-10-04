from fastapi import FastAPI

app = FastAPI()

# Simple dictionary acting as an in-memory database
items = {
    1: {"name": "Laptop", "price": 1200},
    2: {"name": "Mouse", "price": 25},
}

# 1. GET (Read): Fetch all items
@app.get("/items")
async def get_items():
    return items

# 2. GET (Read): Fetch a single item
# Analogy: This is similar to Express's app.get('/items/:item_id')
# NOTE: The parameter name in the URL path (item_id) must match the function parameter name.
@app.get("/items/{item_id}")
async def get_item(item_id: int): # The ': int' is a Python Type Hint.
    # We will cover Path Parameters and Type Hints more deeply on Day 2.
    if item_id in items:
        return items[item_id]
    # In Express, you might send res.status(404).send('Not Found').
    # Here, we'll return a simple dict for now; proper error handling comes later.
    return {"message": "Item not found"}

# 3. POST (Create): Add a new item
# Analogy: app.post('/items', handler)
@app.post("/items")
async def create_item():
    # **NOTE:** For now, we are skipping request body parsing.
    # In Day 3-4, **Pydantic Models** will elegantly replace Express's body-parser/validation.
    new_id = max(items.keys()) + 1 if items else 1
    items[new_id] = {"name": f"New Item {new_id}", "price": 0.0}
    return {"message": "Item created (placeholder)", "item_id": new_id}

# 4. PUT (Update): Update an existing item
# Analogy: app.put('/items/:item_id', handler)
@app.put("/items/{item_id}")
async def update_item(item_id: int):
    if item_id in items:
        items[item_id]["price"] = 99.99  # Placeholder update
        return {"message": f"Item {item_id} updated."}
    return {"message": f"Item {item_id} not found."}

# 5. DELETE (Delete): Remove an item
# Analogy: app.delete('/items/:item_id', handler)
@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    if item_id in items:
        del items[item_id]
        return {"message": f"Item {item_id} deleted."}
    return {"message": f"Item {item_id} not found."}