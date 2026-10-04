from fastapi import APIRouter, Depends, HTTPException, status

from backend.core.dependencies import get_current_student

from backend.schemas.enrollment import (
    EnrollmentCreate,
    EnrollmentResponse
)

from backend.services.enrollment_service import (
    get_subject_by_code,
    check_enrollment,
    enroll_student,
    unenroll_student,
    get_student_subjects
)


router = APIRouter(
    prefix="/api/enrollments",
    tags=["Enrollments"]
)


@router.post(
    "",
    response_model=EnrollmentResponse,
    status_code=status.HTTP_201_CREATED
)
def create_enrollment(
    data: EnrollmentCreate,
    student_id: int = Depends(get_current_student)
):
    subject = get_subject_by_code(data.subject_code)

    if not subject:
        raise HTTPException(
            status_code=404,
            detail="Subject code not found"
        )

    if check_enrollment(
        student_id,
        subject["subject_id"]
    ):
        raise HTTPException(
            status_code=409,
            detail="You are already enrolled in this subject"
        )

    enroll_student(
        student_id,
        subject["subject_id"]
    )

    return subject


@router.delete("/{subject_id}")
def delete_enrollment(
    subject_id: int,
    student_id: int = Depends(get_current_student)
):
    if not check_enrollment(student_id, subject_id):
        raise HTTPException(
            status_code=404,
            detail="You are not enrolled in this subject"
        )

    unenroll_student(student_id, subject_id)

    return {
        "message": "Successfully unenrolled"
    }


@router.get("/me")
def get_my_subjects(
    student_id: int = Depends(get_current_student)
):
    return get_student_subjects(student_id)