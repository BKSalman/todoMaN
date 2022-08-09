from fastapi import APIRouter
from .items import routes as items_router

router = APIRouter(
    prefix="/api"
)

router.include_router(items_router.router)