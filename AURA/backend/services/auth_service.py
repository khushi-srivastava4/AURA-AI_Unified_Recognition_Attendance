from backend.database.supabase import supabase
from backend.core.security import create_access_token
import bcrypt


def authenticate_teacher(username: str, password: str):
    response = (
        supabase
        .table("teachers")
        .select("*")
        .eq("username", username)
        .execute()
    )

    if not response.data:
        return None

    teacher = response.data[0]

    if not bcrypt.checkpw(
        password.encode(),
        teacher["password"].encode()
    ):
        return None

    access_token = create_access_token(
        teacher["teacher_id"],
        "teacher"
    )

    return {
        "teacher": teacher,
        "access_token": access_token
    }


def register_teacher(
    username: str,
    password: str,
    name: str
):
    response = (
        supabase
        .table("teachers")
        .select("teacher_id")
        .eq("username", username)
        .execute()
    )

    if response.data:
        return None

    hashed_password = bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    ).decode()

    response = (
        supabase
        .table("teachers")
        .insert({
            "username": username,
            "password": hashed_password,
            "name": name
        })
        .execute()
    )

    return response.data[0]