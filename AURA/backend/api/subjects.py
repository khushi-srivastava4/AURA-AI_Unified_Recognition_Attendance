from fastapi import APIRouter, Depends, HTTPException

from backend.core.dependencies import get_current_teacher
from backend.schemas.subject import CreateSubjectRequest, SubjectResponse
from backend.services.subject_service import (
    create_teacher_subject,
    get_subjects_for_teacher
)
from backend.services.enrollment_service import (
    get_subject_students,
    get_subject_voice_students
)
from backend.database.supabase import supabase

router = APIRouter(
    prefix="/api/subjects",
    tags=["Subjects"]
)


@router.post(
    "",
    response_model=SubjectResponse,
    status_code=201
)
def create_subject_endpoint(
    request: CreateSubjectRequest,
    current_teacher: dict = Depends(get_current_teacher)
):
    teacher_id = current_teacher["user_id"]

    try:
        result = create_teacher_subject(
            request.subject_code,
            request.name,
            request.section,
            teacher_id
        )

        return result[0]

    except Exception as e:
        if "unique_teacher_subject" in str(e):
            raise HTTPException(
                status_code=409,
                detail="Subject already exists for this teacher"
            )

        raise HTTPException(
            status_code=500,
            detail="Failed to create subject"
        )


@router.get("")
def get_subjects(
    current_teacher: dict = Depends(get_current_teacher)
):
    teacher_id = current_teacher["user_id"]

    return get_subjects_for_teacher(teacher_id)

@router.get("/{subject_id}/students")
def get_students_for_subject(
    subject_id: int,
    current_teacher: dict = Depends(get_current_teacher)
):
    teacher_id = current_teacher["user_id"]

    # Make sure this subject belongs to the logged-in teacher
    subject = (
        supabase
        .table("subjects")
        .select("subject_id")
        .eq("subject_id", subject_id)
        .eq("teacher_id", teacher_id)
        .execute()
    )

    if not subject.data:
        raise HTTPException(
            status_code=403,
            detail="You do not have access to this subject"
        )

    return get_subject_students(subject_id)

@router.get("/{subject_id}/voice-students")
def get_voice_students_for_subject(
    subject_id: int,
    current_teacher: dict = Depends(get_current_teacher)
):
    teacher_id = current_teacher["user_id"]

    # Make sure this subject belongs to the logged-in teacher
    subject = (
        supabase
        .table("subjects")
        .select("subject_id")
        .eq("subject_id", subject_id)
        .eq("teacher_id", teacher_id)
        .execute()
    )

    if not subject.data:
        raise HTTPException(
            status_code=403,
            detail="You do not have access to this subject"
        )

    return get_subject_voice_students(subject_id)