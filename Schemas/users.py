from pydantic import BaseModel,Field,EmailStr
class UserCreate(BaseModel):
    firstname: str
    lastname: str
    email: str
    password: str = Field(min_length=8, max_length=72)

class UserResponse(BaseModel):
    id: int
    firstname: str
    lastname: str
    email: str
    class Config:
        from_attributes = True
class LoginCreate(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user: dict
class ChangePasswordRequest(BaseModel):
    current_password: str = Field(min_length=1)
    new_password: str = Field(min_length=6)
    confirm_password: str = Field(min_length=6)





