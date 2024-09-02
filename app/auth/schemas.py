
from pydantic import EmailStr, BaseModel


class SchemasForRegister(BaseModel):
    email: EmailStr
    password: str
    username: str

class SchemasForLogin(BaseModel):
    email: EmailStr
    password: str

class SchemasToken(BaseModel):
    refresh: str
    access: str


class SchemasForView(BaseModel):
    email: EmailStr
    username: str
    id: int