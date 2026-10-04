from fastapi import APIRouter, HTTPException, Depends

from backend.schemas.auth import (
    TeacherLoginRequest,
    TeacherRegisterRequest
)

from backend.services.auth_service import (
    authenticate_teacher,
    register_teacher
)

from backend.core.dependencies import get_current_teacher
from backend.database.supabase import supabase


router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"]
)


@router.post("/teacher/login")
def teacher_login(request: TeacherLoginRequest):
    result = authenticate_teacher(
        request.username,
        request.password
    )

    if result is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    teacher = result["teacher"]
    access_token = result["access_token"]

    teacher.pop("password", None)

    return {
        "message": "Teacher login successful",
        "access_token": access_token,
        "token_type": "bearer",
        "teacher": teacher
    }

@router.post("/teacher/register")
def teacher_register(request: TeacherRegisterRequest):

    result = register_teacher(
        request.username,
        request.password,
        request.name
    )

    if result is None:
        raise HTTPException(
            status_code=409,
            detail="Username already taken"
        )

    result.pop("password", None)

    return {
        "message": "Teacher registered successfully",
        "teacher": result
    }

@router.get("/me")
def get_current_teacher_info(
    current_teacher: dict = Depends(get_current_teacher)
):
    teacher_id = current_teacher["user_id"]

    response = (
        supabase
        .table("teachers")
        .select("teacher_id, username, name")
        .eq("teacher_id", teacher_id)
        .execute()
    )

    if not response.data:
        raise HTTPException(
            status_code=404,
            detail="Teacher not found"
        )

    return response.data[0]