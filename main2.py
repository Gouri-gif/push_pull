from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

# -----------------------------
# 1. Define Data Model
# -----------------------------
class Item(BaseModel):
    id: int
    name: str
    price: float
    in_stock: bool = True

# In-memory database (list)
items_db: List[Item] = []

# -----------------------------
# 2. Create (POST)
# -----------------------------
@app.post("/items/", response_model=Item)
def create_item(item: Item):
    # Check if ID already exists
    for existing_item in items_db:
        if existing_item.id == item.id:
            raise HTTPException(status_code=400, detail="Item with this ID already exists")
    items_db.append(item)
    return item

# -----------------------------
# 3. Read All (GET)
# -----------------------------
@app.get("/items/", response_model=List[Item])
def get_items():
    return items_db

# -----------------------------
# 4. Read One (GET by ID)
# -----------------------------
@app.get("/items/{item_id}", response_model=Item)
def get_item(item_id: int):
    for item in items_db:
        if item.id == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")

# -----------------------------
# 5. Update (PUT)
# -----------------------------
@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, updated_item: Item):
    for index, item in enumerate(items_db):
        if item.id == item_id:
            items_db[index] = updated_item
            return updated_item
    raise HTTPException(status_code=404, detail="Item not found")

# -----------------------------
# 6. Delete (DELETE)
# -----------------------------
@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    for index, item in enumerate(items_db):
        if item.id == item_id:
            del items_db[index]
            return {"message": f"Item {item_id} deleted successfully"}
    raise HTTPException(status_code=404, detail="Item not found")
