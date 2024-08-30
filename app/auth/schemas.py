
from pydantic import EmailStr, BaseModel


class SchemasForRegister(BaseModel):
    email: EmailStr
    password: str
    username: str


class SchemasForView(BaseModel):
    email: EmailStr
    username: str
    id: int