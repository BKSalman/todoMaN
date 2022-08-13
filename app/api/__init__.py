import sys
sys.path.append("..")
from fastapi import APIRouter
from .items import routes as items_routes
from .auth import routes as auth_routes

router = APIRouter(
    prefix="/api"
)

router.include_router(items_routes.router)
router.include_router(auth_routes.router)