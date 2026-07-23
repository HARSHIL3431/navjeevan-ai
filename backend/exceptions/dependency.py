from backend.exceptions.base import BaseAppException

class DependencyFailedException(BaseAppException):
    def __init__(self, message: str):
        super().__init__(message, status_code=502)
