from fastapi import APIRouter, HTTPException, Response, status

from app.dependencies import TaskCollection
from app.schemas.dto import TaskCreateDTO, TaskReadDTO, TaskUpdateDTO
from app.services import task_service

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("", response_model=list[TaskReadDTO])
async def list_tasks(coll: TaskCollection) -> list[TaskReadDTO]:
    return await task_service.list_tasks(coll)


@router.get("/{task_id}", response_model=TaskReadDTO)
async def get_task(task_id: str, coll: TaskCollection) -> TaskReadDTO:
    row = await task_service.get_task(coll, task_id)
    if row is None:
        raise HTTPException(status_code=404, detail="Task not found.")
    return row


@router.post("", response_model=TaskReadDTO, status_code=status.HTTP_201_CREATED)
async def create_task(body: TaskCreateDTO, coll: TaskCollection) -> TaskReadDTO:
    return await task_service.create_task(coll, body)


@router.put("/{task_id}", response_model=TaskReadDTO)
async def update_task(
    task_id: str,
    body: TaskUpdateDTO,
    coll: TaskCollection,
) -> TaskReadDTO:
    return await task_service.update_task(coll, task_id, body)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: str, coll: TaskCollection) -> Response:
    await task_service.delete_task(coll, task_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
