from pydantic import BaseModel
from typing import Optional

class CourseModel(BaseModel):
    name: str
    duration: str
    teacher: str
    image: str
    stars: Optional[float] = 0.0
