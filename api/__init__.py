from fastapi import APIRouter
from api.operations import router as operation_router

router = APIRouter()
router.include_router(operation_router)