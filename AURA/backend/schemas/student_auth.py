from pydantic import BaseModel


class StudentLoginRequest(BaseModel):
    student_id: int


class StudentFaceLoginRequest(BaseModel):
    face_embedding: list[float]

class StudentResponse(BaseModel):
    student_id: int
    name: str


class StudentLoginResponse(BaseModel):
    message: str
    access_token: str
    token_type: str
    student: StudentResponse