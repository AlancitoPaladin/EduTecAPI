from pydantic import BaseModel
from typing import Optional

class EnrollmentModel(BaseModel):
    studentEmail: str
    courseId: str  # ObjectId en string
    enrolledAt: Optional[datetime] = Field(default_factory=datetime.utcnow)
