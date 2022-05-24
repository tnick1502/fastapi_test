import csv
from io import StringIO
from typing import Any, BinaryIO, TextIO

from fastapi import Depends, BackgroundTasks

from services.operations import OperationService
from models.operations import OperationCreate, Operation

class ReportsService:
    report_fields = [
        'date',
        'kind',
        'amount',
        'description',
    ]

    def __init__(self, operations_service: OperationService = Depends()):
        # обращение к сервису операций
        self.operations_service = operations_service

    def import_csv(self, user_id: int, file: Any):
        # получение файла
        reader = csv.DictReader(
            (line.decode() for line in file),
            fieldnames=self.report_fields,
        )
        next(reader) # Пропускаем заголовок
        operations = []
        for row in reader:
            operation_data = OperationCreate.parse_obj(row)
            if operation_data.description == '':
                operation_data.description = None
            operations.append(operation_data)

        self.operations_service.create_many(
            user_id,
            operations,
        )

    def export_csv(self, user_id: int) -> Any:
        output = StringIO()
        writer = csv.DictWriter(
            output,
            fieldnames=self.report_fields,
            extrasaction='ignore',
        )

        operations = self.operations_service.get_many(user_id)

        writer.writeheader()
        for operation in operations:
            operation_data = Operation.from_orm(operation)
            writer.writerow(operation_data.dict())

        output.seek(0)
        return output