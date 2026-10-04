from src.api.client import api_post, api_get


def teacher_login(username, password):
    return api_post(
        "/api/auth/teacher/login",
        {
            "username": username,
            "password": password
        }
    )

def teacher_register(username, name, password):
    return api_post(
        "/api/auth/teacher/register",
        {
            "username": username,
            "name": name,
            "password": password
        }
    )

def get_current_teacher(token):
    return api_get(
        "/api/auth/me",
        token=token
    )