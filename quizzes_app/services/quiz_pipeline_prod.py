"""
Production quiz generation pipeline.

This module implements the end-to-end "prod" pipeline:
- Download audio from a YouTube video (yt_dlp).
- Transcribe the audio using Whisper.
- Generate a quiz from the transcript using Gemini.
- Return the quiz as a validated Python dict.
"""

import yt_dlp
import whisper
import json
import os
import tempfile
from google import genai

from quizzes_app.services.error import AIPipelineError


def build_quiz_prod(video_url: str) -> dict:
    """
    Build a quiz for the given YouTube video URL using the production pipeline.

    Steps:
    - Extract audio from the YouTube video.
    - Transcribe the audio using Whisper.
    - Generate a quiz JSON payload using Gemini.
    - Clean up temporary files and directories.

    Returns:
        dict: Parsed quiz payload.
    """
    audio_path = extract_audio(video_url)

    try:
        transcript = transcribe_audio(audio_path)
    finally:
        # Best-effort cleanup of audio file and temp directory
        try:
            if os.path.exists(audio_path):
                os.remove(audio_path)
        except OSError:
            pass

        temp_dir = os.path.dirname(audio_path)
        try:
            if os.path.isdir(temp_dir):
                os.rmdir(temp_dir)
        except OSError:
            pass

    payload = generate_quiz(transcript)
    return payload


def extract_audio(video_url: str) -> str:
    """
    Download the audio track from a YouTube video into a temporary file.

    Args:
        video_url (str): The URL of the YouTube video.

    Returns:
        str: Path to the downloaded audio file.
    """
    tmp_dir = tempfile.mkdtemp(prefix="quizly_")
    tmp_filename = os.path.join(tmp_dir, "temp_audio.%(ext)s")

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": tmp_filename,
        "quiet": True,
        "noplaylist": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=True)
        audio_file = ydl.prepare_filename(info)

    return audio_file


def transcribe_audio(audio_path: str) -> str:
    """
    Transcribe an audio file to text using Whisper.

    Args:
        audio_path (str): Path to the audio file.

    Returns:
        str: The transcribed text.
    """
    model = whisper.load_model("base")
    result = model.transcribe(audio_path)
    return result["text"]


def generate_quiz(transcript: str) -> dict:
    """
    Generate a quiz payload from a transcript using Gemini.

    The model is instructed to return strictly valid JSON with:
    - title
    - description
    - questions (10 questions, each with 4 options and one correct answer)

    Args:
        transcript (str): The transcript text.

    Returns:
        dict: Parsed quiz payload.

    Raises:
        AIPipelineError: If the model is overloaded or returns invalid JSON.
    """
    prompt = (
        "Based on the following transcript, generate a quiz in valid JSON format.\n\n"
        "The quiz must follow this exact structure:\n\n"
        "{\n"
        "  \"title\": \"Create a concise quiz title based on the topic of the transcript.\",\n"
        "  \"description\": \"Summarize the transcript in no more than 150 characters. Do not include any quiz questions or answers.\",\n"
        "  \"questions\": [\n"
        "    {\n"
        "      \"question_title\": \"The question goes here.\",\n"
        "      \"question_options\": [\"Option A\", \"Option B\", \"Option C\", \"Option D\"],\n"
        "      \"answer\": \"The correct answer from the above options\"\n"
        "    }\n"
        "    ...(exactly 10 questions)\n"
        "  ]\n"
        "}\n\n"
        "Requirements:\n"
        "- Each question must have exactly 4 distinct answer options.\n"
        "- Only one correct answer is allowed per question, and it must be present in 'question_options'.\n"
        "- The output must be valid JSON and parsable as-is (e.g., using Python's json.loads).\n"
        "- Do not include explanations, comments, or any text outside the JSON.\n\n"
        "Transcript below:\n\n"
        f"{transcript}"
    )

    client = genai.Client()

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )

        content = response.text or ""
        content = content.strip()

        # Handle cases where the model wraps JSON in Markdown code fences
        if content.startswith("```"):
            lines = content.splitlines()
            if lines and lines[0].startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].startswith("```"):
                lines = lines[:-1]
            content = "\n".join(lines).strip()

        payload = json.loads(content)
        return payload

    except Exception as e:
        message = str(e)
        if "503" in message or "model is overloaded" in message:
            raise AIPipelineError(
                "AI pipeline failed: model overloaded, try again later."
            ) from e

        raise AIPipelineError("AI pipeline failed: invalid JSON output") from e
