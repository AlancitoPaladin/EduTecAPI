from pydantic import BaseModel, EmailStr
from typing import Optional

# Pydantic model es usado para definir la estructura del usuario
class UserModel(BaseModel):
    name: str
    last_name: str
    email: EmailStr
    password: str
    role: str
    profile_picture: Optional[str] = None  # URL de la imagen
    bio: Optional[str] = None
    is_active: bool = True

    class Config:
        from_attributes = True
