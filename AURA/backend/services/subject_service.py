from backend.database.supabase import supabase


def create_teacher_subject(
    subject_code: str,
    name: str,
    section: str,
    teacher_id: int
):
    data = {
        "subject_code": subject_code,
        "name": name,
        "section": section,
        "teacher_id": teacher_id
    }

    response = (
        supabase
        .table("subjects")
        .insert(data)
        .execute()
    )

    return response.data


def get_subjects_for_teacher(teacher_id: int):
    response = (
        supabase
        .table("subjects")
        .select(
            "*, subject_students(count), attendance_logs(timestamp)"
        )
        .eq("teacher_id", teacher_id)
        .execute()
    )

    subjects = response.data

    for sub in subjects:
        sub["total_students"] = (
            sub.get("subject_students", [{}])[0].get("count", 0)
            if sub.get("subject_students")
            else 0
        )

        attendance = sub.get("attendance_logs", [])

        unique_sessions = len(
            set(log["timestamp"] for log in attendance)
        )

        sub["total_classes"] = unique_sessions

        sub.pop("subject_students", None)
        sub.pop("attendance_logs", None)

    return subjects