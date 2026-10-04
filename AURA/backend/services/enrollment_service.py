from backend.database.supabase import supabase


def get_subject_by_code(subject_code: str):
    response = (
        supabase
        .table("subjects")
        .select("subject_id, subject_code, name, section")
        .eq("subject_code", subject_code)
        .execute()
    )

    if not response.data:
        return None

    return response.data[0]


def check_enrollment(student_id: int, subject_id: int):
    response = (
        supabase
        .table("subject_students")
        .select("*")
        .eq("student_id", student_id)
        .eq("subject_id", subject_id)
        .execute()
    )

    return len(response.data) > 0


def enroll_student(student_id: int, subject_id: int):
    response = (
        supabase
        .table("subject_students")
        .insert({
            "student_id": student_id,
            "subject_id": subject_id
        })
        .execute()
    )

    return response.data


def unenroll_student(student_id: int, subject_id: int):
    response = (
        supabase
        .table("subject_students")
        .delete()
        .eq("student_id", student_id)
        .eq("subject_id", subject_id)
        .execute()
    )

    return response.data


def get_student_subjects(student_id: int):
    response = (
        supabase
        .table("subject_students")
        .select("*, subjects(*)")
        .eq("student_id", student_id)
        .execute()
    )

    return response.data

def get_subject_students(subject_id: int):
    response = (
        supabase
        .table("subject_students")
        .select("student_id, students(student_id, name)")
        .eq("subject_id", subject_id)
        .execute()
    )

    return response.data

def get_subject_voice_students(subject_id: int):
    response = (
        supabase
        .table("subject_students")
        .select(
            "student_id, students(student_id, name, voice_embedding)"
        )
        .eq("subject_id", subject_id)
        .execute()
    )

    return response.data
