# Quizly Backend

Quizly is an interactive quiz application that allows users to create, take, and manage quizzes. The application features a modern UI with a dark theme and green accents, providing an engaging user experience.

## Features

- **User Authentication**: Register, login, and logout functionality
- **Quiz Generation**: Create quizzes from Youtube-URLs
- **Quiz Taking**: Interactive quiz interface with multiple-choice questions
- **Results Review**: View quiz results with correct/incorrect answers
- **Quiz Management**: View, edit, and delete quizzes

## Requirements

- The backend must support **JWT authentication** with **HttpOnly cookies**. This means:
    - The login response must set the JWT access token as an HttpOnly cookie.
    - Requests to protected routes must be authenticated via this cookie.
    - The frontend must not have direct access to the token (e.g., no localStorage or Authorization header).
    - Make sure your backend correctly allows cross-origin requests (CORS) for the local frontend.

## Tech Stack  
- Python 3.12 + Django 5 + DRF  
- pytest + coverage (testing)  
- ffmpeg (required for later AI integration)  
- yt_dlp · Whisper · Gemini Flash (for AI-based quiz generation)

## Local Setup
```bash
python -m venv venv
venv\Scripts\activate  # (Windows)
pip install -r requirements.txt
python manage.py runserver
```

## Project Structure
```
quizly-backend/│
├── auth_app/                 # Authentifizierung
│   ├── api/                  # 
│   │   ├── permissions.py    # 
│   │   ├── serializer.py     # 
│   │   ├── urls.py           # 
│   │   ├── view.py           # 
├── manage_app/               # Quiz-Logik
│   ├── api/                  # 
│   │   ├── permissions.py    # 
│   │   ├── serializer.py     # 
│   │   ├── urls.py           # 
│   │   ├── view.py           # 
└── quizly/                   # Hilfsfunktionen
│   ├── core/                 # 
│   │   ├── test.py           # 
│   │   ├── view.py           # 
│   ├── settings.py           # 
│   ├── urls.py               # 
└── manage.py                 # 
└── manage.py                 # 

```

## Note
FFmpeg must be installed globally for Whisper AI to work.
Check your installation with:
ffmpeg -version

## Setup and Installation



## Tests & Coverage

Tests are written using **Django's built-in TestCase** and  **REST framework's APITestCase** classes.

Run all tests:
```bash
python manage.py test

coverage run manage.py test
coverage report
```

