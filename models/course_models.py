from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class CourseModel(BaseModel):
    course: str
    start: str
    end: str
    year: int
    teacherEmail: str
    image: str
    stars: Optional[float] = 0.0
    category: str
    description: str
    level: str


class Course(BaseModel):
    id: Optional[str] = None
    name: str
    description: Optional[str] = None
    created_by: str  # Email o id del maestro
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class Announcement(BaseModel):
    id: Optional[int] = None
    course_id: str
    title: str
    content: str
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class Assignment(BaseModel):
    id: Optional[int] = None
    course_id: str
    title: str
    description: str
    due_date: datetime
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
