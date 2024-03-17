from fastapi import APIRouter, Response, status, HTTPException
from tortoise.contrib.fastapi import HTTPNotFoundError

from ...models import Employee
from ..schemas import Employee_Pydantic, EmployeePost_Pydantic, Status

employees = APIRouter(
    prefix="/employees",
    tags=["employees"]
)

@employees.post('')
async def create_employee(employee: EmployeePost_Pydantic):
    try:
        employee_obj = await Employee.create(**employee.dict(exclude_unset=True))
    except InterruptedError:
        raise HTTPException(
            status_code=400,
            detail=f"Employee {employee.username} already exists"
        )
    return await Employee_Pydantic.from_tortoise_orm(employee_obj)


@employees.get('')
async def get_employees():
    return await Employee_Pydantic.from_queryset(Employee.all())

