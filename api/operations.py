from fastapi import APIRouter, Depends
from typing import List

from models.operations import Operation
from database import Session, get_session
from services.operations import OperationService
import tables

router = APIRouter(
    prefix="/operations"
)

@router.get("/", response_model=List[Operation])
# response_model=List[Operation] - указали возвращаемое значение
def get_operations(service: OperationService = Depends()):
    return service.get_list()
