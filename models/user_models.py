from pydantic import BaseModel, EmailStr
from typing import Optional

# Pydantic model to define the user data structure
class UserModel(BaseModel):
    name: str
    email: EmailStr
    age: Optional[int] = None

    class Config:
        # This ensures that Pydantic will treat the data as a dictionary
        from_attributes = True
