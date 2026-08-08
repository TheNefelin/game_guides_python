from fastapi import status
from rfc9457 import BadRequestProblem, ForbiddenProblem, NotFoundProblem, Problem, UnauthorisedProblem


class AppError(Problem):
  def __init__(self, message: str, status_code: int = status.HTTP_400_BAD_REQUEST):
    self.message = message
    super().__init__(title=message, detail=message, status=status_code, type_="app-error")


class NotFoundError(NotFoundProblem):
  type_ = "not-found"
  title = "Resource not found."

  def __init__(self, entity: str = "Resource"):
    super().__init__(detail=f"{entity} not found")
    self.message = self.detail


class DuplicateNameError(BadRequestProblem):
  type_ = "duplicate-name"
  title = "Duplicate resource."

  def __init__(self, name: str):
    super().__init__(detail=f"'{name}' already exists")
    self.message = self.detail


class UnauthorizedError(UnauthorisedProblem):
  type_ = "unauthorized"
  title = "Unauthorized."

  def __init__(self, message: str = "Invalid or expired token"):
    super().__init__(detail=message)
    self.message = message


class ForbiddenError(ForbiddenProblem):
  type_ = "forbidden"
  title = "Forbidden."

  def __init__(self, message: str = "Insufficient permissions"):
    super().__init__(detail=message)
    self.message = message


class InvalidApiKeyError(UnauthorisedProblem):
  type_ = "invalid-api-key"
  title = "Invalid API key."

  def __init__(self, message: str = "Invalid API Key"):
    super().__init__(detail=message)
    self.message = message
