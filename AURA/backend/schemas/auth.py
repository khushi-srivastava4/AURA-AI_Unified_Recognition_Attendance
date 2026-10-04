from pydantic import BaseModel, Field


class TeacherLoginRequest(BaseModel):
    username: str = Field(min_length=1)
    password: str = Field(min_length=1)


class TeacherRegisterRequest(BaseModel):
    username: str = Field(min_length=1)
    name: str = Field(min_length=1)
    password: str = Field(min_length=1)