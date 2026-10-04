from src.api.client import api_post


def student_login(student_id):
    return api_post(
        "/api/auth/student/login",
        {
            "student_id": student_id
        }
    )


def student_face_login(face_embedding):
    return api_post(
        "/api/auth/student/face-login",
        {
            "face_embedding": face_embedding
        }
    )