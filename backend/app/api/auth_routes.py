from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.auth_schemas import AuthRequestBase
from app.services.api.auth_service import (
    DuplicateEmailError,
    login_user,
    signup_user,
)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup", status_code=status.HTTP_201_CREATED)
def signup(payload: AuthRequestBase, db: Session = Depends(get_db)):
    try:
        return signup_user(db, payload)
    except DuplicateEmailError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc


@router.post("/login", status_code=status.HTTP_200_OK)
def login(payload: AuthRequestBase, db: Session = Depends(get_db)):
    try:
        return login_user(db, payload)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
        ) from exc