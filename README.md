# Quizly – Backend (Django REST Framework)

Quizly automatically converts YouTube videos into quizzes with 10 AI‑generated questions.  
This backend provides the core API for authentication, quiz creation (stub or production AI pipeline), and quiz management.

---

## Features

- User registration & login (JWT via HttpOnly cookies)
- Quiz generation from YouTube URLs (stub mode or Whisper + Gemini)
- Manage own quizzes (List, Detail, Update, Delete)
- Clear error handling and clean API structure
- Full automated test suite with high coverage

---

## Tech Stack

- Python 3.12  
- Django 5 + DRF  
- ffmpeg (must be installed globally)
- yt_dlp  
- Whisper  
- Gemini Flash (via google-genai)

---

## Quickstart (Development)

```bash
# Clone the repository
git clone <repo-url>
cd Quizly-backend

# Create a virtual environment
python -m venv env
.\env\Scripts\activate.ps1  # Windows

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Start the development server
python manage.py runserver
```

API base URL: http://localhost:8000/api/  
Admin panel: http://localhost:8000/admin/

---

## Environment Variables (`.env` setup)

Create a `.env` file in the **project root** (same folder as `manage.py`):

```
SECRET_KEY=your-django-secret-key
GEMINI_API_KEY=your-gemini-api-key
```

`.env` is already excluded from Git via `.gitignore`.

Django loads environment variables automatically via `python-dotenv`.

---

## FFmpeg Note

FFmpeg must be installed globally for Whisper to work:

```bash
ffmpeg -version
```

---

## Tests & Coverage

```bash
coverage erase
coverage run manage.py test
coverage report
```

---

## Authentication

The project uses JWT authentication via HttpOnly cookies.

Available endpoints:

- `POST /api/register/`
- `POST /api/login/`
- `POST /api/logout/`

---

## createQuiz – AI / Stub Pipeline

Endpoint for converting a YouTube URL into a quiz.

**POST `/api/createQuiz/`**

Example request:

```json
{ "url": "https://www.youtube.com/watch?v=XXXXXXXXXXX" }
```

Modes:

- `QUIZLY_PIPELINE_MODE=stub` – deterministic stub output (fast, for development)
- `QUIZLY_PIPELINE_MODE=prod` – Whisper transcription + Gemini Flash quiz generation

---

## Quiz Management Endpoints

Users can only access their own quizzes.  
Accessing quizzes of other users returns `403 Forbidden`.

| Method | Endpoint | Description |
|--------|----------|--------------|
| GET | `/api/quizzes/` | List all quizzes of the authenticated user |
| GET | `/api/quizzes/{id}/` | Retrieve a single quiz |
| PATCH | `/api/quizzes/{id}/` | Update only the `title` field |
| DELETE | `/api/quizzes/{id}/` | Delete a quiz including its questions |

---

## Project Structure

```
quizly-backend/
├── auth_app/
│   ├── api/
│   │   ├── serializer.py
│   │   ├── urls.py
│   │   ├── view.py
│   ├── tests/
├── management_app/
│   ├── api/
│   │   ├── permissions.py
│   │   ├── serializer.py
│   │   ├── urls.py
│   │   ├── view.py
│   ├── services/
│   │   ├── error.py
│   │   ├── helpers.py
│   │   ├── persist_quiz.py
│   │   ├── quiz_pipeline_prod.py
│   │   ├── quiz_pipeline_stub.py
│   ├── tests/
│   ├── models.py
└── quizly/
│   ├── core/
│   │   ├── test.py
│   │   ├── view.py
│   ├── settings.py
│   ├── urls.py
└── manage.py
```
