from rest_framework.exceptions import APIException

class AIPipelineError(APIException):
    status_code = 502
    default_detail = "AI pipeline failed"
    default_code = "ai_pipeline_failed"