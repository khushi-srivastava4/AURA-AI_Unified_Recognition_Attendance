from fastapi import APIRouter, Depends, HTTPException, status

from backend.core.dependencies import (
    get_current_teacher,
    get_current_student
)

from backend.schemas.attendance import (
    CreateAttendanceRequest,
    AttendanceResponse,
    AttendanceWithSubjectResponse
)

from backend.services.attendance_service import (
    get_subject_for_teacher,
    student_exists,
    create_attendance_record,
    get_teacher_attendance,
    get_student_attendance
)


router = APIRouter(
    prefix="/api/attendance",
    tags=["Attendance"]
)


@router.post(
    "",
    response_model=AttendanceResponse,
    status_code=status.HTTP_201_CREATED
)
def create_attendance(
    request: CreateAttendanceRequest,
    current_teacher: dict = Depends(get_current_teacher)
):
    teacher_id = current_teacher["user_id"]

    # Check that the subject belongs to the logged-in teacher
    subject = get_subject_for_teacher(
        request.subject_id,
        teacher_id
    )

    if not subject:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to this subject"
        )

    # Check that the student exists
    if not student_exists(request.student_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )

    try:
        attendance = create_attendance_record(
            subject_id=request.subject_id,
            student_id=request.student_id,
            is_present=request.is_present,
            timestamp=request.timestamp
        )

        return attendance

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create attendance record"
        )


@router.get(
    "",
    response_model=list[AttendanceWithSubjectResponse]
)
def get_attendance(
    current_teacher: dict = Depends(get_current_teacher)
):
    teacher_id = current_teacher["user_id"]

    return get_teacher_attendance(teacher_id)


@router.get(
    "/me",
)
def get_my_attendance(
    student_id: int = Depends(get_current_student)
):
    return get_student_attendance(student_id)