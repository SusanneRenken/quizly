"""
Custom exception for handling AI pipeline failures.

Raised when the quiz generation pipeline (stub or prod)
encounters an unexpected error.
"""

from rest_framework.exceptions import APIException


class AIPipelineError(APIException):
    """
    Represents a failure inside the AI quiz generation pipeline.

    Returns:
    - HTTP 502 Bad Gateway
    - A consistent error structure for the client
    """

    status_code = 502
    default_detail = "AI pipeline failed"
    default_code = "ai_pipeline_failed"
