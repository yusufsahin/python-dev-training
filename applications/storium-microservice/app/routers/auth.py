from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
from app.repositories import user_repo
from app.schemas.auth import Token, UserCreate, UserOut
from app.security import create_access_token, hash_password, verify_password
from app.deps import get_current_user
from app.models import User

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserOut)
def register(body: UserCreate, db: Session = Depends(get_db)) -> UserOut:
    if user_repo.user_get_by_email(db, body.email):
        raise HTTPException(status_code=400, detail="Bu e-posta kayıtlı.")
    if user_repo.user_get_by_username(db, body.username):
        raise HTTPException(status_code=400, detail="Bu kullanıcı adı alınmış.")
    u = user_repo.user_create(
        db,
        email=body.email,
        username=body.username,
        hashed_password=hash_password(body.password),
    )
    db.commit()
    db.refresh(u)
    return UserOut.model_validate(u)


@router.post("/login", response_model=Token)
def login(
    form: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
) -> Token:
    user = user_repo.user_get_by_username(db, form.username)
    if not user or not verify_password(form.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Kullanıcı adı veya parola hatalı.",
        )
    if not user.is_active:
        raise HTTPException(status_code=403, detail="Hesap devre dışı.")
    token = create_access_token(user.id, {"username": user.username})
    return Token(access_token=token)


@router.get("/me", response_model=UserOut)
def me(user: User = Depends(get_current_user)) -> UserOut:
    return UserOut.model_validate(user)
