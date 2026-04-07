from typing import Annotated

from fastapi import Depends, Request
from motor.motor_asyncio import AsyncIOMotorCollection


def get_task_collection(request: Request) -> AsyncIOMotorCollection:
    return request.app.state.task_collection


TaskCollection = Annotated[AsyncIOMotorCollection, Depends(get_task_collection)]
