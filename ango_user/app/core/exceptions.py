from fastapi import status


class AngoException(Exception):
    def __init__(self, status_code: int, message: str):
        super(Exception, self).__init__(message)
        self.status_code = status_code


class AuthException(AngoException):
    def __init__(
        self,
        status_code: int = status.HTTP_401_UNAUTHORIZED,
        message: str = "Unauthorized",
        headers: dict[str, str] = None,
    ):
        super(AuthException, self).__init__(status_code, message)
        self.headers = {"WWW-Authenticate": "Bearer"} if not headers else headers


class NotFoundException(AngoException):
    def __init__(self, status_code: int = status.HTTP_404_NOT_FOUND, message: str = "Not Found"):
        super(AngoException, self).__init__(status_code, message)


class BadRequestException(AngoException):
    def __init__(self, status_code: int = status.HTTP_400_BAD_REQUEST, message: str = "Bad Request"):
        super(AngoException, self).__init__(status_code, message)


class DuplicateRecordException(AngoException):
    def __init__(self, status_code: int = status.HTTP_409_CONFLICT, message: str = "Record already exists"):
        super(AngoException, self).__init__(status_code, message)
