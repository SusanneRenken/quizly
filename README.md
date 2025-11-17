# Quizly Backend

Quizly is an interactive quiz application that allows users to create, take, and manage quizzes. The backend is built with Django REST Framework and supports AI-powered quiz generation from YouTube videos.

## Features

- **User Authentication**: Register, login, and logout with JWT (HttpOnly cookies)
- **Quiz Generation**: Create quizzes from YouTube URLs (Stub & AI-Pipeline)
- **Quiz Management**: List, detail, edit, delete
- **Quiz Taking**: Multiple-choice questions
- **Results Review**: Correct/incorrect answers

## Requirements

- Python 3.12  
- Django 5 + DRF  
- ffmpeg (must be installed globally)
- yt_dlp  
- Whisper  
- Gemini Flash (via google-genai)

The backend uses **JWT authentication with HttpOnly cookies**:
- Login sets the access token as an HttpOnly cookie  
- Protected routes are authenticated via this cookie  
- The frontend has no direct access to the token  

## Tech Stack
- Python · Django · DRF  
- FFmpeg · yt_dlp · Whisper · Gemini AI  
- pytest + coverage  

## Local Setup

```bash
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Environment Variables (`.env` setup)

Create a `.env` file in the **project root** (same folder as `manage.py`):

```
SECRET_KEY=your-django-secret-key
GEMINI_API_KEY=your-gemini-api-key
```

`.env` is already excluded from Git via `.gitignore`.

Django loads environment variables automatically via `python-dotenv`.

## Running the Development Server

```bash
python manage.py runserver
```

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

## FFmpeg Note

FFmpeg must be installed globally for Whisper to work:

```bash
ffmpeg -version
```

## Tests & Coverage

```bash
python manage.py test
coverage run manage.py test
coverage report
```