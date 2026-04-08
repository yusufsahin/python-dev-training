from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    email: EmailStr
    username: str = Field(min_length=2, max_length=150)
    password: str = Field(min_length=8, max_length=128)


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True, frozen=True)

    id: int
    email: str
    username: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
