from uuid import UUID
from typing import Generic, TypeVar
from pydantic import BaseModel, ConfigDict, Field


T = TypeVar("T")


class AppModel(BaseModel):
  model_config = ConfigDict(from_attributes=True)


# PAGINATION ------------------------------------------------------
class PaginationRequest(BaseModel):
  page: int = Field(default=1, ge=1)
  limit: int = Field(default=20, ge=1, le=100)


class PaginationResponse(BaseModel, Generic[T]):
  page: int
  limit: int
  total: int
  items: list[T]


# AUTH & USERS ----------------------------------------------------
class RoleResponse(AppModel):
  id: int
  name: str


class UserResponse(AppModel):
  id: UUID
  email: str
  google_sub: str | None
  role: RoleResponse


# GAME ATRIBUTES --------------------------------------------------
class PlatformsRequest(BaseModel):
  name: str = Field(min_length=1, max_length=50)


class PlatformsResponse(AppModel):
  id: int
  name: str


class GenreRequest(BaseModel):
  name: str = Field(min_length=1, max_length=50)


class GenreResponse(AppModel):
  id: int
  name: str

