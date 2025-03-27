from fastapi import APIRouter, HTTPException

router = APIRouter(
    prefix="/example",
    tags=["exampleAPIRouter"],
)

@router.get("/")
async def read_example():
    return {"message": "Hello from API Router"}

@router.get("/{item_id}")
async def read_item(item_id: int):
    if item_id < 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item_id": item_id, "value": "This is your item"}

@router.post("/")
async def create_item(item: dict):
    return {"message": "Item created", "item": item}

