from src.api.client import api_get, api_post


def get_teacher_attendance(token):
    return api_get(
        "/api/attendance",
        token=token
    )


def get_student_attendance(token):
    return api_get(
        "/api/attendance/me",
        token=token
    )

def create_attendance(token, subject_id, student_id, is_present,timestamp):
    return api_post(
        "/api/attendance",
        {
            "subject_id": subject_id,
            "student_id": student_id,
            "is_present": is_present,
            "timestamp": timestamp
        },
        token=token
    )