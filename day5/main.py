from fastapi import FastAPI, Depends, HTTPException, Header, Query
from typing import Annotated

app = FastAPI()

# 1. The Dependency Function
def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
    """
    Simulates common parameters for multiple list-retrieving endpoints.
    """
    return {"q": q, "skip": skip, "limit": limit}

# 2. The Route Handler uses Depends()
# The return value of common_parameters is passed to the 'commons' argument
@app.get("/items/")
async def read_items(commons: dict = Depends(common_parameters)):
    # 'commons' now holds the dictionary returned by common_parameters
    return {"message": "Items found!", **commons}

@app.get("/users/")
async def read_users(commons: dict = Depends(common_parameters)):
    # Same logic, reused dependency
    return {"message": "Users found!", "query_data": commons}
# A dependency function to check for a required 'X-Token' header
async def verify_token(x_token: str = Header()):
    if x_token != "fake-secret-token":
        # If the check fails, raise an exception, stopping the request
        raise HTTPException(status_code=400, detail="X-Token header invalid")

# A dependency function to check for a required 'X-Key' header (simulating another check)
async def verify_key(x_key: str = Header()):
    if x_key != "fake-api-key":
        raise HTTPException(status_code=400, detail="X-Key header invalid")
    return x_key # Returns the key if valid

# Route Protected by a Single Dependency
@app.get("/protected-route/", dependencies=[Depends(verify_token)])
async def secure_route():
    # This code only runs if verify_token did NOT raise an HTTPException
    return {"message": "Access granted!"}

# Route Protected by Multiple Dependencies
@app.get("/super-protected-route/")
async def super_secure_route(
    # Both dependencies run before the route handler
    token_valid: bool = Depends(verify_token), # Result is ignored, only used for validation
    key: str = Depends(verify_key) # Result is passed to 'key'
):
    return {"message": f"Access granted! Key used: {key}"}


'''
TASK: 
Implement a get_current_user Dependency:

Create a dependency function get_current_user(user_id: int) that takes a required query parameter called user_id.

If user_id is less than 1, raise an HTTPException (e.g., status 403).

Otherwise, return a dictionary: {"id": user_id, "is_active": True}.

Use the Dependency: Create a route /profile/ that uses get_current_user and prints the returned user dictionary.
'''

def get_current_user(user_id:Annotated[int|None,Query()]=None):
    if(user_id is None):
        raise HTTPException(
            status_code=400,
            detail="User ID is required as a query parameter."
        )
    if(user_id<1):
        raise HTTPException(status_code=403,detail='user_id is not provided properly')
    return {"id":user_id,"is_active":True}

@app.get("/profile")
async def uses_user_id(user_data:dict = Depends(get_current_user)):
    return user_data