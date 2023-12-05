from src.auth.constants import ErrorCode
from src.exceptions import BadRequest


class AuthRequired(BadRequest):
    DETAIL = ErrorCode.AUTHENTICATION_REQUIRED
