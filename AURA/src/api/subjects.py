from src.api.client import api_get, api_post


def get_teacher_subjects(token):
    return api_get(
        "/api/subjects",
        token=token
    )


def create_subject(token, subject_code, name, section):
    return api_post(
        "/api/subjects",
        {
            "subject_code": subject_code,
            "name": name,
            "section": section
        },
        token=token
    )

def get_subject_students(token, subject_id):
    return api_get(
        f"/api/subjects/{subject_id}/students",
        token=token
    )

def get_subject_voice_students(token, subject_id):
    return api_get(
        f"/api/subjects/{subject_id}/voice-students",
        token=token
    )