from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps_internal import verify_internal_token
from app.repositories import user_repo
from app.schemas.auth import InternalUserOut

router = APIRouter(tags=["internal"])


@router.get("/internal/users/{user_id}", response_model=InternalUserOut)
def internal_user(
    user_id: int,
    db: Session = Depends(get_db),
    _: None = Depends(verify_internal_token),
) -> InternalUserOut:
    u = user_repo.user_get_by_id(db, user_id)
    if not u:
        raise HTTPException(status_code=404, detail="Kullanıcı yok")
    return InternalUserOut(id=u.id, email=u.email, username=u.username)
