from backend.exceptions.base import BaseAppException

class BusinessRuleViolationException(BaseAppException):
    def __init__(self, message: str):
        super().__init__(message, status_code=422)

class ResourceNotFoundException(BaseAppException):
    def __init__(self, message: str):
        super().__init__(message, status_code=404)
