from fastapi import APIRouter, HTTPException, Response, status

from app.dependencies import DbSession
from app.schemas.dto import StudentCreateDTO, StudentReadDTO, StudentUpdateDTO
from app.services import student_service

router = APIRouter(prefix="/students", tags=["students"])


@router.get("", response_model=list[StudentReadDTO])
async def list_students(db: DbSession) -> list[StudentReadDTO]:
    rows = await student_service.list_students(db)
    return [StudentReadDTO.model_validate(r) for r in rows]


@router.post("", response_model=StudentReadDTO, status_code=status.HTTP_201_CREATED)
async def create_student(body: StudentCreateDTO, db: DbSession) -> StudentReadDTO:
    s = await student_service.create_student(
        db,
        student_number=body.student_number,
        first_name=body.first_name,
        last_name=body.last_name,
        birth_date=body.birth_date,
        department_id=body.department_id,
    )
    return StudentReadDTO.model_validate(s)


@router.get("/{student_id}", response_model=StudentReadDTO)
async def get_student(student_id: int, db: DbSession) -> StudentReadDTO:
    s = await student_service.get_student(db, student_id)
    if s is None:
        raise HTTPException(status_code=404, detail="Student not found.")
    return StudentReadDTO.model_validate(s)


@router.put("/{student_id}", response_model=StudentReadDTO)
async def update_student(
    student_id: int, body: StudentUpdateDTO, db: DbSession
) -> StudentReadDTO:
    s = await student_service.update_student(
        db,
        student_id,
        student_number=body.student_number,
        first_name=body.first_name,
        last_name=body.last_name,
        birth_date=body.birth_date,
        department_id=body.department_id,
    )
    return StudentReadDTO.model_validate(s)


@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_student(student_id: int, db: DbSession) -> Response:
    await student_service.delete_student(db, student_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
