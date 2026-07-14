import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import NullPool

from src.core.database import Base, get_db
from src.core.config import settings
from src.main import app
from src.models.models import Role, User, UserSession, Platforms, Genre


engine = create_engine(settings.DATABASE_URL, poolclass=NullPool)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def _clean_tables(session):
  """Delete all data from test-relevant tables in FK-safe order."""
  session.query(UserSession).delete()
  session.query(User).delete()
  session.query(Platforms).delete()
  session.query(Genre).delete()
  session.query(Role).delete()


@pytest.fixture(scope="session")
def db_engine():
  Base.metadata.create_all(bind=engine)
  yield engine
  Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db(db_engine):
  connection = db_engine.connect()
  transaction = connection.begin()
  session = TestingSessionLocal(bind=connection)

  _clean_tables(session)
  session.add_all([
    Role(id=1, name="user"),
    Role(id=2, name="admin"),
  ])
  session.flush()

  yield session

  session.close()
  transaction.rollback()
  connection.close()


@pytest.fixture
def client(db):
  def override_get_db():
    yield db

  app.dependency_overrides[get_db] = override_get_db
  yield TestClient(app)
  app.dependency_overrides.clear()
