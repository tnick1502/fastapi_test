from pydantic import BaseModel
from decimal import Decimal
from enum import Enum
from typing import Optional
from datetime import date

class OperationKind(str, Enum):
    # Создаем список. При валидации значения могут быть только из этого списка
    INCOME = "income"
    OUTCOME = "outcome"

class OperationBase(BaseModel):
    date: date
    kind: OperationKind
    amount: Decimal
    description: Optional[str]

    class Config:
        orm_mode = True

class Operation(OperationBase):
    id: int

class OperationCreate(OperationBase):
    pass

class OperationUpdate(OperationBase):
    pass