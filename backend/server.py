# just Example
from typing import Union

from fastapi import FastAPI, Query, status
from typing_extensions import Annotated

from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name :str
    price : float
    is_offer: Union[bool, None] = None

@app.get("/")
def read_root():
    return {"Hello": "world"}

@app.get("/items/",status_code=status.HTTP_201_CREATED)
async def read_items(q: Union[str, None] = Query(default=None, max_length=50)):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
async def create_item(item_id: int, item: Item):
    return {"item_id": item_id, **item.dict()}
