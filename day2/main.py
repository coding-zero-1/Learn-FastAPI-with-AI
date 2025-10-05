from fastapi import FastAPI
from typing import Optional # Used for optional types

app = FastAPI()

# 1. Basic Path Parameter
# The path segment {item_id} is passed as an argument to the function.
# Analogy: app.get('/items/:item_id', (req, res) => { const id = req.params.item_id; });

@app.get("/items/{item_id}")
# item_id: int - This Type Hint does two things:
# 1. It converts the string from the URL into an actual Python integer.
# 2. It validates the input. If the user navigates to /items/foo, FastAPI
#    automatically returns a 422 Unprocessable Entity error.
async def read_item(item_id: int):
    # In Python, you can now use item_id as a number, no manual parsing needed.
    return {"item_id": item_id, "description": f"This is item number {item_id}"}


# 2. Path Parameters with Types
# FastAPI automatically handles simple data types like int, float, str, and bool.
@app.get("/users/{user_name}")
async def read_user(user_name: str):
    # The string type hint is redundant but good practice.
    return {"user_name": user_name}

# Query Parameters Example
# If the argument is NOT defined in the path, it is treated as a Query Parameter.
# Analogy: const limit = req.query.limit; const skip = req.query.skip;

@app.get("/data/")
async def read_data(limit: int = 10, skip: int = 0):
    # limit: int and skip: int ensures both are converted to integers.
    # The = 10 and = 0 provides default values if the user doesn't specify them.
    
    return {
        "message": f"Fetching data starting at index {skip} with a maximum of {limit} results."
    }

# Test these URLs:
# http://127.0.0.1:8000/data/             (uses defaults: limit=10, skip=0)
# http://127.0.0.1:8000/data/?limit=50    (uses limit=50, skip=0)
# http://127.0.0.1:8000/data/?skip=5&limit=2 (uses skip=5, limit=2)

# Combining Path and Query
@app.get("/items/{item_id}/info")
async def get_item_info(
    item_id: int,               # Defined in the path decorator - Path Parameter
    q: Optional[str] = None,    # Not in the path - Optional Query Parameter
    short: bool = False         # Not in the path - Boolean Query Parameter with default
):
    result = {"item_id": item_id}
    
    # 1. Handle Query Parameter 'q' (optional string)
    if q:
        result.update({"q": q})
        
    # 2. Handle Query Parameter 'short' (boolean)
    if short:
        result.update({"description": "short description"})
    else:
        result.update({"description": "long, detailed description"})
    
    return result

# Test URLs for combined route:
# http://127.0.0.1:8000/items/101/info
# http://127.0.0.1:8000/items/102/info?short=True
# http://127.0.0.1:8000/items/103/info?q=filter_by_name