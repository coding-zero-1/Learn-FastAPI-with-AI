from fastapi import FastAPI
from pydantic import BaseModel,Field # The core
from typing import Optional,Annotated # Optional Used for fields that are allowed to be None

app = FastAPI()

# 1. Define the Pydantic Model (Schema for the data)
class Item(BaseModel):
    name: str
    description: Optional[str] = None # Optional field with a default value of None
    price: float
    tax: Optional[float] = None

# 2. Use the Model in a POST Route Handler
@app.post("/items/")
async def create_item(item: Item): # The type hint 'Item' tells FastAPI to expect the request body to match this schema
    item_dict = item.model_dump() # Converts the Pydantic model instance to a standard Python dict
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict

class ItemAnnotated(BaseModel):
    # 'gt=0' means the value must be greater than 0
    price: Annotated[float, Field(gt=0, description="The price must be positive")]
    # 'max_length=50' ensures the string is not too long
    name: Annotated[str, Field(max_length=50)]
    # 'min_length=3' ensures the password is at least 3 chars
    password: Annotated[str, Field(min_length=3)]

# Annotated is basically a way to add metadata to types like we do with zod in TS
@app.post("/itemsAnnotated/")
async def create_item_annotated(item: ItemAnnotated):
    return item

# A model for the data sent to the client (excludes the other info)
class ItemResponse(BaseModel):
    name: str
    price: float

@app.post("/itemsWithResponse/", response_model=ItemResponse)
async def create_item(item: Item):
    # 'item' still contains the other info from the request
    # but the returned dictionary will be filtered by ItemResponse
    return item # FastAPI converts this to a dict, then filters it

'''
NOTE:
1. Pydantic models are used to define the structure and validation of data in FastAPI.
2. The 'Annotated' type from 'typing' allows adding metadata to fields, such as validation constraints.
3. The 'Field' function from 'pydantic' is used to provide additional validation and metadata for model fields.
4. The 'response_model' parameter in route decorators specifies the model used to filter and validate the response data.
5. FastAPI automatically handles the conversion between Pydantic models and standard Python dictionaries.
6. Optional fields can be defined using 'Optional' from the 'typing' module, allowing them to be None.
7. The 'model_dump()' method converts a Pydantic model instance to a standard Python dictionary.
8. Validation constraints like 'gt', 'max_length', and 'min_length' help ensure data integrity.
9. FastAPI uses type hints to automatically validate and parse request bodies based on Pydantic models.
10. The 'description' parameter in 'Field' can be used to provide additional context for API documentation.
11. Pydantic models can be nested, allowing for complex data structures.
12. FastAPI generates interactive API documentation (Swagger UI and ReDoc) based on Pydantic models.
13. Pydantic models support default values, making it easy to handle optional data.
14. FastAPI automatically generates error responses for validation failures.
'''