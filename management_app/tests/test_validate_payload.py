from rest_framework.test import APITestCase
from management_app.services.persist_quiz import validate_payload
from management_app.services.error import AIPipelineError


class ValidatePayloadTests(APITestCase):
    def test_raises_error_when_not_10_questions(self):
        payload = {"questions": [{"question_title": "Q1", "question_options": ["A", "B", "C", "D"], "answer": "A"}]}
        with self.assertRaises(AIPipelineError) as ctx:
            validate_payload(payload)
        self.assertIn("expected 10 questions", str(ctx.exception))

    def test_raises_error_when_answer_not_in_options(self):
        payload = {
            "questions": [
                {"question_title": f"Q{i}", "question_options": ["A", "B", "C", "D"], "answer": "X"}
                for i in range(1, 11)
            ]
        }
        with self.assertRaises(AIPipelineError) as ctx:
            validate_payload(payload)
        self.assertIn("invalid answer", str(ctx.exception))
