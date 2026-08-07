from uuid import uuid4

import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.pool import NullPool

from src.core.database import Base, get_db
from src.core.config import settings
from src.core.dependencies import verify_api_key
from src.core.security import create_access_token
from src.main import app
from src.models.models import Role, User, UserSession, Platforms, Genre, Game, GamePlatform, GameGenre, Character, Source

ADMIN_TOKEN = create_access_token(uuid4(), "admin")


engine = create_async_engine(settings.TEST_DATABASE_URL, poolclass=NullPool)
TestingSessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)


async def _clean_tables(session: AsyncSession):
  """Delete all data from test-relevant tables in FK-safe order."""
  await session.execute(UserSession.__table__.delete())
  await session.execute(User.__table__.delete())
  await session.execute(Source.__table__.delete())
  await session.execute(Character.__table__.delete())
  await session.execute(GameGenre.__table__.delete())
  await session.execute(GamePlatform.__table__.delete())
  await session.execute(Game.__table__.delete())
  await session.execute(Platforms.__table__.delete())
  await session.execute(Genre.__table__.delete())
  await session.execute(Role.__table__.delete())


TEST_TABLES = [
  "gg_screenshots", "gg_maps", "gg_sources", "gg_characters",
  "gg_game_genres", "gg_game_platforms", "gg_games", "gg_genres",
  "gg_platforms", "gg_user_adventures", "gg_adventure_images", "gg_adventures",
  "gg_user_guides", "gg_guides", "gg_user_sessions", "gg_users", "gg_roles",
]


async def _drop_test_tables(conn):
  for table in TEST_TABLES:
    await conn.execute(text(f"DROP TABLE IF EXISTS {table} CASCADE"))


@pytest.fixture(scope="module")
async def setup_db():
  async with engine.begin() as conn:
    await _drop_test_tables(conn)
    await conn.run_sync(Base.metadata.create_all)
  yield
  # Solo dropear las tablas de este proyecto (gg_*) para no tocar las de otros
  # proyectos que comparten la BD de testing.
  async with engine.begin() as conn:
    await _drop_test_tables(conn)
  # OPCIONAL: si se quisiera borrar TODAS las tablas de la BD (incluidas las de
  # otros proyectos), descomentar y comentar lo anterior:
  # async with engine.begin() as conn:
  #   await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def db(setup_db):
  async with TestingSessionLocal() as session:
    await _clean_tables(session)
    session.add_all([
      Role(id=1, name="user"),
      Role(id=2, name="admin"),
    ])
    await session.flush()

    yield session


@pytest.fixture
async def client(db):
  async def override_get_db():
    yield db

  async def override_verify_api_key():
    return True

  app.dependency_overrides[get_db] = override_get_db
  app.dependency_overrides[verify_api_key] = override_verify_api_key
  async with AsyncClient(
    transport=ASGITransport(app=app),
    base_url="http://test",
    headers={"Authorization": f"Bearer {ADMIN_TOKEN}"},
  ) as ac:
    yield ac
  app.dependency_overrides.clear()
