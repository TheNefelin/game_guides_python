import uuid
from datetime import datetime
from sqlalchemy import String, Integer, Boolean, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import DateTime

from src.core.database import Base


# AUTH & USERS ----------------------------------------------------
class Role(Base):
  __tablename__ = "gg_roles"

  id: Mapped[int] = mapped_column(Integer, primary_key=True)
  name: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)

  users: Mapped[list["User"]] = relationship(back_populates="role")


class User(Base):
  __tablename__ = "gg_users"

  id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
  email: Mapped[str] = mapped_column(String(256), unique=True, nullable=False)
  google_sub: Mapped[str | None] = mapped_column(String(256), unique=True, nullable=True)
  role_id: Mapped[int] = mapped_column(Integer, ForeignKey("gg_roles.id"), default=1)
  created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

  role: Mapped["Role"] = relationship(back_populates="users")
  sessions: Mapped[list["UserSession"]] = relationship(back_populates="user")


class UserSession(Base):
  __tablename__ = "gg_user_sessions"

  id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
  user_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("gg_users.id"), nullable=False)
  refresh_token: Mapped[str] = mapped_column(String(512), unique=True, nullable=False)
  expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
  is_revoked: Mapped[bool] = mapped_column(Boolean, default=False)
  created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

  user: Mapped["User"] = relationship(back_populates="sessions")


# GAME ATRIBUTES --------------------------------------------------
class Platforms(Base):
  __tablename__ = 'gg_platforms'

  id: Mapped[int] = mapped_column(Integer, primary_key=True)
  name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)


class Genre(Base):
  __tablename__ = 'gg_genres'

  id: Mapped[int] = mapped_column(Integer, primary_key=True)
  name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

