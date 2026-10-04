import numpy as np

from backend.database.supabase import supabase


def get_student_by_id(student_id: int):
    response = (
        supabase
        .table("students")
        .select("student_id, name")
        .eq("student_id", student_id)
        .execute()
    )

    if not response.data:
        return None

    return response.data[0]


def identify_student_by_face(face_embedding: list[float]):
    response = (
        supabase
        .table("students")
        .select("student_id, name, face_embedding")
        .execute()
    )

    if not response.data:
        return None

    input_embedding = np.array(face_embedding)

    best_student = None
    best_score = float("inf")

    for student in response.data:
        stored_embedding = student.get("face_embedding")

        if not stored_embedding:
            continue

        stored_embedding = np.array(stored_embedding)

        score = np.linalg.norm(
            stored_embedding - input_embedding
        )

        if score < best_score:
            best_score = score
            best_student = student

    # Same threshold currently used by your face pipeline
    resemblance_threshold = 0.6

    if best_student and best_score <= resemblance_threshold:
        return {
            "student_id": best_student["student_id"],
            "name": best_student["name"]
        }

    return None