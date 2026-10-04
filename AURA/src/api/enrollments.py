from src.api.client import api_get, api_post, api_delete


def get_my_subjects(token):
    return api_get(
        "/api/enrollments/me",
        token=token
    )


def enroll_subject(token, subject_code):
    return api_post(
        "/api/enrollments",
        {
            "subject_code": subject_code
        },
        token=token
    )


def unenroll_subject(token, subject_id):
    return api_delete(
        f"/api/enrollments/{subject_id}",
        token=token
    )