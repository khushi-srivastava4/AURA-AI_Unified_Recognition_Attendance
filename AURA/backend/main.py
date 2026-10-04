from fastapi import FastAPI

from backend.api.auth import router as auth_router
from backend.api.subjects import router as subjects_router
from backend.api.attendance import router as attendance_router
from backend.api import students
from backend.api.student_auth import router as student_auth_router
from backend.api.enrollments import router as enrollment_router

app = FastAPI(
    title="AURA API",
    description="AI Unified Recognition Attendance API",
    version="1.0.0"
)

app.include_router(auth_router)
app.include_router(subjects_router)
app.include_router(attendance_router)
app.include_router(students.router)
app.include_router(student_auth_router)
app.include_router(enrollment_router)

@app.get("/")
def root():
    return {
        "message": "AURA API is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }