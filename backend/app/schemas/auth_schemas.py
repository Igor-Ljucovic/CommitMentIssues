from pydantic import BaseModel, model_validator
import re


def validate_email_rules(value: str) -> str:
    if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", value):
        raise ValueError("Email format is invalid.")

    return value


def validate_password_rules(value: str) -> str:
    if len(value) < 8:
        raise ValueError("Password must contain at least 8 characters.")

    if len(value) > 64:
        raise ValueError("Password must contain at most 64 characters.")

    if len(value.encode("utf-8")) > 72:
        raise ValueError("Password is too long.")

    if not re.search(r"[A-Z]", value):
        raise ValueError("Password must contain at least one uppercase letter.")

    if not re.search(r"\d", value):
        raise ValueError("Password must contain at least one number.")

    return value


class AuthRequestBase(BaseModel):
    email: str
    password: str

    @model_validator(mode="before")
    @classmethod
    def validate_request(cls, data):
        email = data.get("email")
        password = data.get("password")

        data["email"] = validate_email_rules(email)
        data["password"] = validate_password_rules(password)

        return data


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    id: int
    email: str

    class Config:
        from_attributes = True