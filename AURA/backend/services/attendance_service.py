from backend.database.supabase import supabase


def get_subject_for_teacher(subject_id: int, teacher_id: int):
    response = (
        supabase
        .table("subjects")
        .select("*")
        .eq("subject_id", subject_id)
        .eq("teacher_id", teacher_id)
        .execute()
    )

    if not response.data:
        return None

    return response.data[0]


def student_exists(student_id: int):
    response = (
        supabase
        .table("students")
        .select("student_id")
        .eq("student_id", student_id)
        .execute()
    )

    return bool(response.data)


def create_attendance_record(
    subject_id: int,
    student_id: int,
    is_present: bool,
    timestamp
):
    data = {
        "subject_id": subject_id,
        "student_id": student_id,
        "is_present": is_present,
        "timestamp": timestamp.isoformat()
    }

    response = (
        supabase
        .table("attendance_logs")
        .insert(data)
        .execute()
    )

    return response.data[0]


def get_teacher_attendance(teacher_id: int):
    response = (
        supabase
        .table("attendance_logs")
        .select(
            "id, timestamp, subject_id, student_id, is_present, "
            "subjects!inner(name, subject_code)"
        )
        .eq("subjects.teacher_id", teacher_id)
        .order("timestamp", desc=True)
        .execute()
    )

    return response.data

def get_student_attendance(student_id: int):
    response = (
        supabase
        .table("attendance_logs")
        .select("*, subjects(subject_id, name, subject_code, section)")
        .eq("student_id", student_id)
        .order("timestamp", desc=True)
        .execute()
    )

    return response.data
