<p align="center">
  <img src="assets/aura_logo.png" alt="AURA logo" width="140">
</p>

<h1 align="center">AURA: AI Unified Recognition Attendance</h1>

<p align="center">
  Take a whole class's attendance from a single group photo or a short voice recording.
</p>

---

## Overview

Manual roll call wastes class time and allows proxy attendance. **AURA** replaces it with face and voice recognition:

- A **teacher** creates subjects, shares a QR code or join link, and marks attendance by uploading classroom photos or recording audio.
- A **student** logs in with their face, enrolls in subjects through a QR code or link, and can optionally enroll a voice sample for voice-only attendance.

Both modalities work the same way: convert the face or voice into an **embedding vector**, then match it against the vectors stored for enrolled students.

## Features

- **Group-photo attendance:** detects every face in one or more classroom photos and identifies each student.
- **Voice attendance:** splits a recording on silence and identifies each speaker segment.
- **Face login for students:** no password; the camera feed is matched against stored face embeddings.
- **QR / join-link enrollment:** students join a subject by scanning a QR code or opening a `?join-code=...` link.
- **Role-based access:** separate teacher and student portals, protected with JWT tokens.
- **Subject-wise records:** attendance logs with present/absent status and timestamps, with a results review step before saving.

## How it works

### Face pipeline (`src/pipelines/face_pipeline.py`)

1. **Detect** faces with dlib's HOG-based frontal face detector.
2. **Align** each face using the 68-point landmark predictor.
3. **Encode** each face into a 128-dimensional embedding (dlib's ResNet-based model).
4. **Identify** the student with a linear SVM (`probability=True`, `class_weight="balanced"`) trained on stored embeddings, then **verify** the match: the distance to that student's stored embedding must be at most `0.6`, otherwise the face is treated as unknown.

Student face login uses the same embeddings, matched by Euclidean distance against all stored students with the same `0.6` threshold.

### Voice pipeline (`src/pipelines/voice_pipeline.py`)

1. **Load** audio and resample to 16 kHz.
2. **Segment** the recording on silence (`librosa.effects.split`, `top_db=30`) and drop segments shorter than 0.5 s.
3. **Embed** each segment with Resemblyzer's `VoiceEncoder` (GE2E d-vectors).
4. **Match** each segment to the enrolled student with the highest cosine similarity, accepted if the score is at least `0.65`.

## Architecture

```
┌──────────────────────────┐        HTTP + JWT        ┌─────────────────────────┐        ┌──────────────┐
│ Streamlit frontend (src) │  ─────────────────────>  │ FastAPI backend (backend)│  ───>  │   Supabase   │
│ screens · dialogs        │                          │ routers → services       │        │  (PostgreSQL)│
│ face + voice pipelines   │  <─────────────────────  │ auth · validation        │  <───  │              │
└──────────────────────────┘                          └─────────────────────────┘        └──────────────┘
```

The ML pipelines run inside the Streamlit app. The backend handles authentication, authorization and data access.

## Tech stack

| Area | Tools |
|---|---|
| Frontend | Streamlit, Pillow, pandas, NumPy |
| Backend | FastAPI, Uvicorn, Pydantic / pydantic-settings |
| Database | Supabase (PostgreSQL) |
| Face recognition | dlib, `face_recognition_models`, scikit-learn |
| Voice recognition | Resemblyzer, librosa |
| Auth and security | JWT (`python-jose`), bcrypt |
| Other | segno (QR codes), pytest, httpx |

## Project structure

```
.
├── app.py                  # Streamlit entry point and role routing
├── requirements.txt
├── assets/                 # Logo and portal images
├── src/                    # Frontend
│   ├── screens/            # Home, teacher and student screens
│   ├── components/         # Dialogs, header, footer, subject cards
│   ├── pipelines/          # face_pipeline.py, voice_pipeline.py
│   ├── api/                # HTTP client and API wrappers
│   ├── core/               # Session and role handling
│   └── ui/                 # Layout and styling
└── backend/                # FastAPI service
    ├── main.py             # App and router registration
    ├── config.py           # Settings loaded from .env
    ├── api/                # Routers (auth, subjects, students, enrollments, attendance)
    ├── services/           # Business logic
    ├── schemas/            # Pydantic request/response models
    ├── core/               # JWT security and dependencies
    └── database/           # Supabase client
```

## Getting started

### Prerequisites

- Python 3.11
- A [Supabase](https://supabase.com) project

### 1. Clone and install

```bash
git clone https://github.com/ishara16/aura-ai-unified-recognition-attendance.git
cd aura-ai-unified-recognition-attendance

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure the backend

Create a `.env` file in the project root:

```env
SUPABASE_URL=your-supabase-project-url
SUPABASE_KEY=your-supabase-key
JWT_SECRET_KEY=a-long-random-secret

# optional (defaults shown)
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=60
```

### 3. Configure the frontend

Create `.streamlit/secrets.toml`:

```toml
SUPABASE_URL = "your-supabase-project-url"
SUPABASE_KEY = "your-supabase-key"
API_BASE_URL = "http://127.0.0.1:8000"
```

### 4. Create the database tables

In Supabase, create these tables (column names as used by the code):

| Table | Columns used |
|---|---|
| `teachers` | teacher id and login credentials (hashed password) |
| `students` | `student_id`, `name`, `face_embedding`, `voice_embedding` |
| `subjects` | `subject_id`, `name`, `subject_code`, `section`, `teacher_id` |
| `subject_students` | `subject_id`, `student_id` |
| `attendance_logs` | `student_id`, `subject_id`, `timestamp`, `is_present` |

Store the embeddings as arrays or JSON columns.

### 5. Run

Start the backend:

```bash
uvicorn backend.main:app --reload
```

In a second terminal, start the frontend:

```bash
streamlit run app.py
```

Open the Streamlit URL (http://localhost:8501). The API docs are at http://127.0.0.1:8000/docs.

## API overview

| Prefix | Purpose |
|---|---|
| `POST /api/auth/teacher/register`, `/login`, `GET /api/auth/me` | Teacher authentication |
| `POST /api/auth/student/login`, `/face-login` | Student authentication |
| `/api/subjects` | Create and list subjects, list enrolled students and voice-enrolled students |
| `/api/students` | Create and fetch students |
| `/api/enrollments` | Enroll, unenroll and list a student's subjects |
| `/api/attendance` | Save and fetch attendance logs |
| `GET /health` | Health check |

## Usage

**Teacher**
1. Register or log in and create a subject.
2. Share the subject's QR code or join link with students.
3. Open *Take AI Attendance*, choose the subject, then either add class photos and run face analysis, or use voice attendance.
4. Review the present/absent table and confirm to save it.

**Student**
1. Open the student portal and log in with your face.
2. Join a subject through the QR code or link.
3. Optionally enroll a voice sample for voice-only attendance.

## Limitations and future work

- Recognition uses pretrained models, so accuracy depends on lighting, face size and audio quality.
- There is no liveness / anti-spoofing check yet, so a printed photo or recording could be accepted.
- Voice segmentation assumes one speaker at a time with pauses between speakers.
- Possible next steps: liveness detection, unknown-person handling in voice mode, pgvector for embedding search, automated tests, and deployment.

## Privacy

Face and voice embeddings are biometric data. Deploy AURA only with the informed consent of the people being enrolled, and secure the database and keys accordingly.
