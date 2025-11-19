from unittest.mock import patch, MagicMock
from django.test import SimpleTestCase
from management_app.services.quiz_pipeline_prod import (
    build_quiz_prod,
    extract_audio,
    transcribe_audio,
    generate_quiz,
)
from management_app.services.error import AIPipelineError


class QuizPipelineProdExtractAudioTests(SimpleTestCase):
    @patch("management_app.services.quiz_pipeline_prod.tempfile.mkdtemp", return_value="/tmp/quizly_123")
    @patch("management_app.services.quiz_pipeline_prod.yt_dlp.YoutubeDL")
    def test_extract_audio_uses_temp_dir_and_returns_path(self, mock_yt, mock_mkdtemp):
        ydl_instance = MagicMock()
        mock_yt.return_value.__enter__.return_value = ydl_instance

        fake_info = {"id": "abc"}
        ydl_instance.extract_info.return_value = fake_info
        ydl_instance.prepare_filename.return_value = "/tmp/quizly_123/temp_audio.webm"

        path = extract_audio("https://www.youtube.com/watch?v=abcdefghijk")

        mock_mkdtemp.assert_called_once()
        mock_yt.assert_called_once()
        ydl_instance.extract_info.assert_called_once()
        ydl_instance.prepare_filename.assert_called_once_with(fake_info)

        self.assertEqual(path, "/tmp/quizly_123/temp_audio.webm")


class QuizPipelineProdTranscribeTests(SimpleTestCase):
    @patch("management_app.services.quiz_pipeline_prod.whisper.load_model")
    def test_transcribe_audio_uses_whisper_model(self, mock_load_model):
        model = MagicMock()
        mock_load_model.return_value = model
        model.transcribe.return_value = {"text": "hello world"}

        text = transcribe_audio("/tmp/some_audio.webm")

        mock_load_model.assert_called_once_with("base")
        model.transcribe.assert_called_once_with("/tmp/some_audio.webm")
        self.assertEqual(text, "hello world")


class QuizPipelineProdBuildTests(SimpleTestCase):
    @patch("management_app.services.quiz_pipeline_prod.generate_quiz")
    @patch("management_app.services.quiz_pipeline_prod.transcribe_audio")
    @patch("management_app.services.quiz_pipeline_prod.extract_audio")
    @patch("management_app.services.quiz_pipeline_prod.os.rmdir")
    @patch("management_app.services.quiz_pipeline_prod.os.path.isdir", return_value=True)
    @patch("management_app.services.quiz_pipeline_prod.os.remove")
    @patch("management_app.services.quiz_pipeline_prod.os.path.exists", return_value=True)
    def test_build_quiz_prod_calls_steps_and_cleans_up(
        self,
        mock_exists,
        mock_remove,
        mock_isdir,
        mock_rmdir,
        mock_extract,
        mock_transcribe,
        mock_generate,
    ):
        mock_extract.return_value = "/tmp/quizly_123/temp_audio.webm"
        mock_transcribe.return_value = "fake transcript"
        fake_payload = {"title": "T", "description": "D", "questions": []}
        mock_generate.return_value = fake_payload

        result = build_quiz_prod("https://www.youtube.com/watch?v=abcdefghijk")

        mock_extract.assert_called_once()
        mock_transcribe.assert_called_once_with(
            "/tmp/quizly_123/temp_audio.webm")
        mock_generate.assert_called_once_with("fake transcript")
        self.assertEqual(result, fake_payload)

        mock_exists.assert_called_once_with("/tmp/quizly_123/temp_audio.webm")
        mock_remove.assert_called_once_with("/tmp/quizly_123/temp_audio.webm")
        mock_isdir.assert_called_once_with("/tmp/quizly_123")
        mock_rmdir.assert_called_once_with("/tmp/quizly_123")

    @patch("management_app.services.quiz_pipeline_prod.generate_quiz")
    @patch("management_app.services.quiz_pipeline_prod.transcribe_audio")
    @patch("management_app.services.quiz_pipeline_prod.extract_audio")
    @patch("management_app.services.quiz_pipeline_prod.os.rmdir", side_effect=OSError("rm dir fail"))
    @patch("management_app.services.quiz_pipeline_prod.os.path.isdir", return_value=True)
    @patch("management_app.services.quiz_pipeline_prod.os.remove", side_effect=OSError("rm file fail"))
    @patch("management_app.services.quiz_pipeline_prod.os.path.exists", return_value=True)
    def test_build_quiz_prod_cleanup_ignores_oserrors(
        self,
        mock_exists,
        mock_remove,
        mock_isdir,
        mock_rmdir,
        mock_extract,
        mock_transcribe,
        mock_generate,
    ):
        """
        Deckt die except OSError: pass-Zweige im Cleanup ab.
        """
        mock_extract.return_value = "/tmp/quizly_123/temp_audio.webm"
        mock_transcribe.return_value = "fake transcript"
        fake_payload = {"title": "T", "description": "D", "questions": []}
        mock_generate.return_value = fake_payload

        result = build_quiz_prod("https://www.youtube.com/watch?v=abcdefghijk")

        self.assertEqual(result, fake_payload)
        mock_exists.assert_called_once_with("/tmp/quizly_123/temp_audio.webm")
        mock_remove.assert_called_once()
        mock_isdir.assert_called_once_with("/tmp/quizly_123")
        mock_rmdir.assert_called_once()


class QuizPipelineProdGenerateQuizTests(SimpleTestCase):
    @patch("management_app.services.quiz_pipeline_prod.genai.Client")
    def test_generate_quiz_parses_json_from_model_response(self, mock_client_cls):
        class FakeResponse:
            text = '{"title": "T", "description": "D", "questions": []}'

        client_instance = MagicMock()
        mock_client_cls.return_value = client_instance
        client_instance.models.generate_content.return_value = FakeResponse()

        result = generate_quiz("some transcript")

        mock_client_cls.assert_called_once()
        client_instance.models.generate_content.assert_called_once()

        self.assertEqual(result["title"], "T")
        self.assertEqual(result["description"], "D")
        self.assertIn("questions", result)

    @patch("management_app.services.quiz_pipeline_prod.genai.Client")
    def test_generate_quiz_strips_markdown_code_fence(self, mock_client_cls):
        class FakeResponse:
            text = """```json
{"title": "T", "description": "D", "questions": []}
```"""

        client_instance = MagicMock()
        mock_client_cls.return_value = client_instance
        client_instance.models.generate_content.return_value = FakeResponse()

        result = generate_quiz("some transcript")

        self.assertEqual(result["title"], "T")

    @patch("management_app.services.quiz_pipeline_prod.genai.Client")
    def test_generate_quiz_raises_aipipelineerror_on_503(self, mock_client_cls):
        client_instance = MagicMock()
        mock_client_cls.return_value = client_instance
        client_instance.models.generate_content.side_effect = Exception("503 backend error")

        with self.assertRaises(AIPipelineError) as ctx:
            generate_quiz("some transcript")

        self.assertIn("model overloaded", str(ctx.exception))

    @patch("management_app.services.quiz_pipeline_prod.genai.Client")
    def test_generate_quiz_raises_aipipelineerror_on_invalid_json(self, mock_client_cls):
        class FakeResponse:
            text = "NOT JSON"

        client_instance = MagicMock()
        mock_client_cls.return_value = client_instance
        client_instance.models.generate_content.return_value = FakeResponse()

        with self.assertRaises(AIPipelineError) as ctx:
            generate_quiz("some transcript")

        self.assertIn("invalid JSON output", str(ctx.exception))