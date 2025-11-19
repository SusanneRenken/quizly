"""
Stub quiz generation pipeline.

This module provides a deterministic stub implementation of the quiz
generation pipeline. It is used for fast end-to-end testing without
calling external services like yt-dlp, Whisper, or Gemini.
"""


def build_quiz_stub(video_url: str) -> dict:
    """
    Return a static quiz payload for testing purposes.

    Args:
        video_url (str): The YouTube URL (ignored in stub mode).

    Returns:
        dict: A deterministic quiz structure with 10 questions,
              each having 4 options and a single correct answer.
    """
    return {
        "title": "Stub vs. Prod: Understand & Apply",
        "description": "Test your knowledge of stub and production pipelines: purpose, differences, usage, and common pitfalls.",
        "questions": [
            {
                "question_title": "What is the purpose of a stub pipeline in projects?",
                "question_options": [
                    "Fast end-to-end testing without real AI/infrastructure",
                    "Permanent production logic",
                    "Optimizing frontend styles",
                    "Creating a database backup",
                ],
                "answer": "Fast end-to-end testing without real AI/infrastructure",
            },
            {
                "question_title": "What best describes a production pipeline?",
                "question_options": [
                    "Returns dummy data",
                    "Runs actual processing using real services",
                    "Disables all validations",
                    "Produces only random results",
                ],
                "answer": "Runs actual processing using real services",
            },
            {
                "question_title": "When is a stub pipeline particularly useful?",
                "question_options": [
                    "When external services are not yet available",
                    "Only during UI deployments",
                    "Only after go-live",
                    "When production is already stable",
                ],
                "answer": "When external services are not yet available",
            },
            {
                "question_title": "What is a key difference between stub and production?",
                "question_options": [
                    "Stub is deterministic; production can vary",
                    "Both produce identical outputs",
                    "Production has no dependencies",
                    "Stub always requires a GPU",
                ],
                "answer": "Stub is deterministic; production can vary",
            },
            {
                "question_title": "What is a risk of testing with stub data for too long?",
                "question_options": [
                    "Too many costs from real API calls",
                    "The UI becomes too fast",
                    "Lack of coverage for real-world error cases",
                    "Too few unit tests are possible",
                ],
                "answer": "Lack of coverage for real-world error cases",
            },
            {
                "question_title": "What is typically required for a production pipeline?",
                "question_options": [
                    "No credentials needed",
                    "External tools like ffmpeg/yt-dlp/Whisper properly installed",
                    "Offline-only operation",
                    "No logging required",
                ],
                "answer": "External tools like ffmpeg/yt-dlp/Whisper properly installed",
            },
            {
                "question_title": "Why is @transaction.atomic useful during persistence?",
                "question_options": [
                    "Enables dark mode in the admin panel",
                    "All-or-nothing saving for Quiz + Questions",
                    "Boosts GPU performance",
                    "Allows GET requests without authentication",
                ],
                "answer": "All-or-nothing saving for Quiz + Questions",
            },
            {
                "question_title": "What does NOT belong in a stub pipeline?",
                "question_options": [
                    "Fixed test data",
                    "Real API calls to Gemini",
                    "Deterministic responses",
                    "Fast execution",
                ],
                "answer": "Real API calls to Gemini",
            },
            {
                "question_title": "How does a stub pipeline help during testing?",
                "question_options": [
                    "Reduces flakiness through stable outputs",
                    "Disables all tests",
                    "Forces timeouts",
                    "Prevents logging",
                ],
                "answer": "Reduces flakiness through stable outputs",
            },
            {
                "question_title": "When should you switch from stub to production?",
                "question_options": [
                    "When the basic end-to-end path works and dependencies are ready",
                    "Never; stub is always enough",
                    "Immediately at project start",
                    "Only after release",
                ],
                "answer": "When the basic end-to-end path works and dependencies are ready",
            },
        ],
    }
