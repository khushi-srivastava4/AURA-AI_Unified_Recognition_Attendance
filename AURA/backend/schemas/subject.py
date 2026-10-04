from pydantic import BaseModel, Field


class CreateSubjectRequest(BaseModel):
    subject_code: str = Field(min_length=1)
    name: str = Field(min_length=1)
    section: str = Field(min_length=1)


class SubjectResponse(BaseModel):
    subject_id: int
    subject_code: str
    name: str
    section: str
    teacher_id: int