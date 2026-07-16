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


# GAMES -----------------------------------------------------------
class GameRequest(BaseModel):
  name: str = Field(min_length=1, max_length=100)
  slug: str = Field(min_length=1, max_length=100)
  description: str | None = None
  cover_url: str | None = None
  release_year: int | None = None
  rating: float | None = None
  is_enabled: bool = True
  sort_order: int = 0
  platform_ids: list[int] = []
  genre_ids: list[int] = []


class GameResponse(AppModel):
  id: int
  name: str
  slug: str
  description: str | None
  cover_url: str | None
  release_year: int | None
  rating: float | None
  is_enabled: bool
  sort_order: int
  created_at: str
  updated_at: str
  platforms: list[PlatformsResponse] = []
  genres: list[GenreResponse] = []

