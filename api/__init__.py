from fastapi import APIRouter
from api.operations import router as operation_router
from api.auth import router as auth_router
from api.reports import router as report_router

router = APIRouter()
router.include_router(operation_router)
router.include_router(auth_router)
router.include_router(report_router)