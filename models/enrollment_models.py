from pydantic import BaseModel
from typing import Optional

class EnrollmentModel(BaseModel):
    studentEmail: str
    courseId: str
    state: bool
    enrolledAt: Optional[datetime] = Field(default_factory=datetime.utcnow)
