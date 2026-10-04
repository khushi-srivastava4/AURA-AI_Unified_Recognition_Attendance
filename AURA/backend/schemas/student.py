from pydantic import BaseModel


class StudentResponse(BaseModel):
    student_id: int
    name: str
    face_embedding: list[float] | None = None

class CreateStudentRequest(BaseModel):
    name: str
    face_embedding: list[float]
    voice_embedding: list[float] | None = None
