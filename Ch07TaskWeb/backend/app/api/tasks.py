"""Görevler API router."""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload

from app.api.deps import get_db
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate

router = APIRouter(prefix="/tasks", tags=["tasks"])


def _task_to_response(task: Task) -> TaskResponse:
    """ORM Task -> TaskResponse (category_name, category_color dahil)."""
    return TaskResponse(
        id=task.id,
        title=task.title,
        description=task.description or "",
        priority=task.priority,
        status=task.status,
        due_date=task.due_date,
        category_id=task.category_id,
        created_at=task.created_at,
        updated_at=task.updated_at,
        category_name=task.category.name if task.category else None,
        category_color=task.category.color if task.category else None,
    )


@router.get("", response_model=list[TaskResponse])
def list_tasks(
    db: Session = Depends(get_db),
    status: str | None = Query(None, description="Durum filtresi"),
    priority: int | None = Query(None, description="Öncelik filtresi (1-4)"),
    category_id: int | None = Query(None, description="Kategori id"),
    search: str | None = Query(None, description="Başlık/açıklama arama"),
):
    """Görev listesi; filtreler uygulanır."""
    q = db.query(Task).options(joinedload(Task.category))
    if status:
        q = q.filter(Task.status == status)
    if priority is not None:
        q = q.filter(Task.priority == priority)
    if category_id is not None:
        q = q.filter(Task.category_id == category_id)
    if search and search.strip():
        term = f"%{search.strip()}%"
        q = q.filter((Task.title.ilike(term)) | (Task.description.ilike(term)))
    q = q.order_by(Task.priority.desc(), Task.due_date.asc(), Task.created_at.desc())
    tasks = q.all()
    return [_task_to_response(t) for t in tasks]


@router.get("/stats")
def task_stats(db: Session = Depends(get_db)):
    """Toplam ve tamamlanan görev sayısı."""
    total = db.query(Task).count()
    done = db.query(Task).filter(Task.status == "done").count()
    return {"total": total, "done": done}


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)):
    """Tek görev getir."""
    task = db.query(Task).options(joinedload(Task.category)).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Görev bulunamadı")
    return _task_to_response(task)


@router.post("", response_model=TaskResponse, status_code=201)
def create_task(body: TaskCreate, db: Session = Depends(get_db)):
    """Yeni görev oluştur (created_at/updated_at sunucuda)."""
    task = Task(
        title=body.title,
        description=body.description or "",
        priority=body.priority,
        status=body.status,
        due_date=body.due_date,
        category_id=body.category_id,
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    db.refresh(task)  # load category if any
    if task.category_id:
        task = db.query(Task).options(joinedload(Task.category)).filter(Task.id == task.id).first()
    return _task_to_response(task)


@router.put("/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, body: TaskUpdate, db: Session = Depends(get_db)):
    """Görev güncelle (updated_at sunucuda)."""
    task = db.query(Task).options(joinedload(Task.category)).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Görev bulunamadı")
    data = body.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(task, key, value)
    db.commit()
    db.refresh(task)
    return _task_to_response(task)


@router.delete("/{task_id}", status_code=204)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    """Görev sil."""
    task = db.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Görev bulunamadı")
    db.delete(task)
    db.commit()
    return None
