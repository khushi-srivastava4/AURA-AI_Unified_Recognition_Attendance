from fastapi import APIRouter, HTTPException, status

from backend.schemas.student_auth import (
    StudentLoginRequest,
    StudentFaceLoginRequest,
    StudentLoginResponse
)

from backend.services.student_auth_service import (
    get_student_by_id,
    identify_student_by_face
)

from backend.core.security import create_access_token


router = APIRouter(
    prefix="/api/auth/student",
    tags=["Student Authentication"]
)


@router.post(
    "/login",
    response_model=StudentLoginResponse
)
def student_login(data: StudentLoginRequest):

    student = get_student_by_id(data.student_id)

    if not student:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Student not found"
        )

    access_token = create_access_token(
        student["student_id"],
        "student"
    )

    return {
        "message": "Student login successful",
        "access_token": access_token,
        "token_type": "bearer",
        "student": student
    }


@router.post(
    "/face-login",
    response_model=StudentLoginResponse
)
def student_face_login(data: StudentFaceLoginRequest):

    student = identify_student_by_face(
        data.face_embedding
    )

    if not student:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Face not recognized"
        )

    access_token = create_access_token(
        student["student_id"],
        "student"
    )

    return {
        "message": "Student face login successful",
        "access_token": access_token,
        "token_type": "bearer",
        "student": student
    }