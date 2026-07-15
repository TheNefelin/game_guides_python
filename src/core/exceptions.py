from fastapi import status


class AppError(Exception):
  def __init__(self, message: str, status_code: int = status.HTTP_400_BAD_REQUEST):
    self.message = message
    self.status_code = status_code


class NotFoundError(AppError):
  def __init__(self, entity: str = "Resource"):
    super().__init__(f"{entity} not found", status.HTTP_404_NOT_FOUND)


class DuplicateNameError(AppError):
  def __init__(self, name: str):
    super().__init__(f"'{name}' already exists", status.HTTP_400_BAD_REQUEST)


class UnauthorizedError(AppError):
  def __init__(self, message: str = "Invalid or expired token"):
    super().__init__(message, status.HTTP_401_UNAUTHORIZED)


class ForbiddenError(AppError):
  def __init__(self, message: str = "Insufficient permissions"):
    super().__init__(message, status.HTTP_403_FORBIDDEN)


class InvalidApiKeyError(AppError):
  def __init__(self, message: str = "Invalid API Key"):
    super().__init__(message, status.HTTP_401_UNAUTHORIZED)
