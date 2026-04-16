class BusinessException(Exception):
    """
    Base exception for business/application layer errors.
    """

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


class NotFoundException(BusinessException):
    """
    Raised when a requested resource cannot be found.
    """


class ValidationException(BusinessException):
    """
    Raised when input validation at business level fails.
    """

