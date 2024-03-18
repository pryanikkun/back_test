from fastapi import APIRouter, HTTPException, Depends
from tortoise.contrib.fastapi import HTTPNotFoundError

from ...dependency import login_required
from ...models import Employee
from ..schemas import Employee_Pydantic, UpdateEmployee

employees = APIRouter(
    prefix="/employees",
    tags=["employees"],
    dependencies=[Depends(login_required), ]
)


# @employees.post('')
# async def create_employee(employee: EmployeePost_Pydantic):
#     """"""
#     try:
#         employee_obj = await Employee.create(**employee.dict(exclude_unset=True))
#     except InterruptedError:
#         raise HTTPException(
#             status_code=400,
#             detail=f"Employee {employee.username} already exists"
#         )
#     return await Employee_Pydantic.from_tortoise_orm(employee_obj)


@employees.get('')
async def get_employees():
    return await Employee_Pydantic.from_queryset(Employee.all())


@employees.put('/{employee_id}',
               response_model=UpdateEmployee,
               responses={404: {"model": HTTPNotFoundError}})
async def update_employee(employee_id: int,
                          data: UpdateEmployee):
    """  Изменение информации о сотруднике """
    employee_obj = await Employee.get_or_none(id=employee_id)
    if employee_obj:
        employee_obj = await Employee.update_from_dict(
            employee_obj,
            data={
                "first_name": data.first_name,
                "last_name": data.last_name,
                "username": data.username
            }
        )
        await employee_obj.save()
        return {"first_name": data.first_name,
                "last_name": data.last_name,
                "username": data.username}
    else:
        raise HTTPException(
            status_code=404,
            detail=f"Сотрудника с id {employee_id} не существует"
        )
