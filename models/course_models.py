from pydantic import BaseModel
from typing import Optional


class CourseModel(BaseModel):
    course: str
    start: str
    end: str
    year: int
    teacherEmail: str
    image: str
    stars: Optional[float] = 0.0
    duration: str
    category: str
    description: str
    level: str
