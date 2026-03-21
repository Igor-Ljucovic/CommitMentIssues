from sqlalchemy.orm import Session

from backend.app.schemas.auth_schemas import AuthRequestBase
from app.core.security import hash_password, verify_password, create_access_token
from app.repositories.user_repository import create_user, get_user_by_email


class DuplicateEmailError(Exception):
    pass


def authenticate_user(db: Session, login_data: AuthRequestBase):
    normalized_email = login_data.email.strip().lower()
    user = get_user_by_email(db, normalized_email)

    if user is None:
        raise ValueError("Invalid email or password.")

    if not verify_password(login_data.password, user.password_hash):
        raise ValueError("Invalid email or password.")

    return user


def signup_user(db: Session, signup_data: AuthRequestBase) -> dict:
    normalized_email = signup_data.email.strip().lower()

    existing_user = get_user_by_email(db, normalized_email)
    if existing_user:
        raise DuplicateEmailError("A user with this email already exists.")

    password_hash = hash_password(signup_data.password)

    user = create_user(
        db=db,
        email=normalized_email,
        password_hash=password_hash,
    )

    access_token = create_access_token(
        data={
            "sub": user.email,
            "user_id": user.id,
        }
    )

    return {
        "message": "Signup successful.",
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
        },
    }


def login_user(db: Session, login_data: AuthRequestBase) -> dict:
    user = authenticate_user(db, login_data)

    access_token = create_access_token(
        data={
            "sub": user.email,
            "user_id": user.id,
        }
    )

    return {
        "message": "Login successful.",
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
        },
    }