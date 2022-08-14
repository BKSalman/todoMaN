from fastapi import APIRouter, HTTPException, Depends
from db.db import get_db
from .schemas import ItemRequest, ItemResponse
from db.db import Session
from db.models import Item


router = APIRouter(
    prefix="/items"
)


@router.get("/")
async def all_items(session: Session = Depends(get_db)):
    all_items = session.query(Item).all()
    return all_items


@router.get("/{item_id}")
async def item(item_id: int, session: Session = Depends(get_db)):
    item = session.query(Item).filter_by(id=item_id).first()
    if not item:
        raise HTTPException(status_code=404)
    return ItemResponse(id= item.id, name= item.name)


@router.put("/{item_id}")
async def update_item(item_id: int, req_item: ItemRequest, session: Session = Depends(get_db)):
    item = session.query(Item).filter_by(id=item_id).first()
    if not item:
        raise HTTPException(status_code=404)
    item.name = req_item.name
    return ItemResponse(id= item.id, name= item.name)


@router.post("/")
async def add_item(item: ItemRequest, session: Session = Depends(get_db)):
    new_item = Item (
        name= item.name
    )
    session.add(new_item)
    session.commit() 
    return ItemResponse(id= new_item.id, name= new_item.name)


@router.delete("/{item_id}")
async def delete_item(item_id: int, session: Session = Depends(get_db)):
    item = session.query(Item).filter_by(id=item_id).delete()
    if not item:
        raise HTTPException(status_code=404)
    return {"Data": f"Deleted item with id {item_id}"}
