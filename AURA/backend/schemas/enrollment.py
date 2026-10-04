from pydantic import BaseModel


class EnrollmentCreate(BaseModel):
    subject_code: str


class EnrollmentResponse(BaseModel):
    subject_id: int
    subject_code: str
    name: str
    section: str | None = None