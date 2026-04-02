from fastapi import APIRouter, HTTPException, Response, status

from app.dependencies import DbSession
from app.schemas.dto import DepartmentCreateDTO, DepartmentReadDTO, DepartmentUpdateDTO
from app.services import department_service

router = APIRouter(prefix="/departments", tags=["departments"])


@router.get("", response_model=list[DepartmentReadDTO])
async def list_departments(db: DbSession) -> list[DepartmentReadDTO]:
    rows = await department_service.list_departments(db)
    return [DepartmentReadDTO.model_validate(r) for r in rows]


@router.post("", response_model=DepartmentReadDTO, status_code=status.HTTP_201_CREATED)
async def create_department(body: DepartmentCreateDTO, db: DbSession) -> DepartmentReadDTO:
    d = await department_service.create_department(db, body.name)
    return DepartmentReadDTO.model_validate(d)


@router.get("/{department_id}", response_model=DepartmentReadDTO)
async def get_department(department_id: int, db: DbSession) -> DepartmentReadDTO:
    d = await department_service.get_department(db, department_id)
    if d is None:
        raise HTTPException(status_code=404, detail="Department not found.")
    return DepartmentReadDTO.model_validate(d)


@router.put("/{department_id}", response_model=DepartmentReadDTO)
async def update_department(
    department_id: int, body: DepartmentUpdateDTO, db: DbSession
) -> DepartmentReadDTO:
    d = await department_service.update_department(db, department_id, body.name)
    return DepartmentReadDTO.model_validate(d)


@router.delete("/{department_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_department(department_id: int, db: DbSession) -> Response:
    await department_service.delete_department(db, department_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
