from fastapi import APIRouter, HTTPException
from .schemas import Item

router = APIRouter(
    prefix="/items"
)


items = [
{
    "id": 0,
    "name": "Clean the house",
},
{
    "id": 1,
    "name": "Clean the house",
},
{
    "id": 2,
    "name": "Clean the house",
},
{
    "id": 3,
    "name": "Clean the house",
},
]

@router.get("/")
async def all_items():
    return items


@router.get("/{item_id}")
async def item(item_id: int):
    for item in items:
        if item["id"] == item_id:
            return item
    raise HTTPException(status_code=404)


@router.put("/{item_id}")
async def update_item(item_id: int, req_item: Item):
    for item in items:
        if item["id"] == item_id:
            item.update({
                        "id": req_item.id,
                        "name": req_item.name,
                    })
            return items
    raise HTTPException(status_code=404)


@router.post("/add")
async def add_item(item: Item):
    for i, x in enumerate(items):
        if i != x["id"]:
            items.append({
                            "id": i,
                            "name": item.name
                        })
        else:
            items.append({
                            "id": len(items),
                            "name": item.name
                        })
        return item


@router.delete("/{item_id}")
async def delete_item(item_id: int):
    for item in items:
        if item["id"] == item_id:
            items.remove(item)
            return items
    raise HTTPException(status_code=404)

