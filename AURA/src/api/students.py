from src.api.client import api_get, api_post

def get_all_students(token):
    return api_get(
        "/api/students",
        token=token
    )


def get_student(token, student_id):
    return api_get(
        f"/api/students/{student_id}",
        token=token
    )

def create_student(name, face_embedding, voice_embedding=None):
    return api_post(
        "/api/students",
        {
            "name": name,
            "face_embedding": face_embedding,
            "voice_embedding": voice_embedding
        }
    )