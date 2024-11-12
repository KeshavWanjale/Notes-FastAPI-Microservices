from pydantic import BaseModel , field_validator, EmailStr
import re


class RegisterUser(BaseModel):
    username: str
    email: EmailStr
    password:str
    is_verified: bool = False

    @field_validator("username")
    def validate_username(cls, value : str) -> str:
        if len(value) < 3:
            raise ValueError("username must be at least 3 characters long")
        if not value[0].isupper():
            raise ValueError("username must start with a capital letter")
        return value
    
    @field_validator("password")
    def validate_password(cls, value : str) -> str:
        pattern = re.compile(r'^(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+={}\[\]:;"\'<>,.?/\\|-])[a-zA-Z\d!@#$%^&*()_+={}\[\]:;"\'<>,.?/\\|-]{8,}$')
        if pattern.match(value):
            return value
        else:
            raise ValueError("Invalid Password format")

class LoginUser(BaseModel):
    email: EmailStr
    password: str