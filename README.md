# 🧠 Quizly Backend

With **Quizly**, you can transform YouTube videos into exciting quizzes.  
The backend is built with **Django REST Framework (DRF)** and provides a REST API  
for communication with the frontend.

## 🚀 Project Status  
🔹 Current: **Setup Phase (Milestone 1 – Project Architecture)**  
🔹 Next Step: Implementing Authentication using JWT + HttpOnly Cookies  

## 🛠️ Tech Stack  
- Python 3.12 + Django 5 + DRF  
- pytest + coverage (testing)  
- ffmpeg (required for later AI integration)  
- yt_dlp · Whisper · Gemini Flash (for AI-based quiz generation)

## ⚙️ Local Setup
```bash
python -m venv venv
venv\Scripts\activate  # (Windows)
pip install -r requirements.txt
python manage.py runserver
```

## Project Structure
quizly/
│
├── auth_app/      # Authentifizierung
├── manage_app/    # Quiz-Logik
└── utils.py       # Hilfsfunktionen

## Note
FFmpeg must be installed globally for Whisper AI to work.
Check your installation with:
ffmpeg -version

## Setup and Installation