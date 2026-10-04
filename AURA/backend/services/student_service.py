from backend.database.supabase import supabase

def create_student(
    name: str,
    face_embedding: list[float],
    voice_embedding: list[float] | None = None
):
    data = {
        "name": name,
        "face_embedding": face_embedding,
        "voice_embedding": voice_embedding
    }

    response = (
        supabase
        .table("students")
        .insert(data)
        .execute()
    )

    return response.data

def get_all_students():
    response = (
        supabase
        .table("students")
        .select("student_id, name, face_embedding")
        .order("student_id")
        .execute()
    )

    return response.data


def get_student_by_id(student_id: int):
    response = (
        supabase
        .table("students")
        .select("student_id, name, face_embedding")
        .eq("student_id", student_id)
        .execute()
    )

    if not response.data:
        return None

    return response.data[0]