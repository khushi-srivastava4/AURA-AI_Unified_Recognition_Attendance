from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from backend.core.security import verify_access_token


security = HTTPBearer()


def get_current_teacher(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> dict:
    return verify_access_token(credentials.credentials)


def get_current_student(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> int:
    user = verify_access_token(credentials.credentials)

    if user["role"] != "student":
        from fastapi import HTTPException

        raise HTTPException(
            status_code=403,
            detail="Student access required"
        )

    return user["user_id"]