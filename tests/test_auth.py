import uuid
from datetime import datetime, timedelta, timezone
from unittest.mock import AsyncMock, patch

from src.api.auth.schemas import GoogleUserInfo
from src.core.exceptions import UnauthorizedError
from src.models.models import User, UserSession


# /api/auth/google -------------------------------------------------


async def test_auth_google_success(client, db):
  mock_info = GoogleUserInfo(
    google_id="111",
    email="new@user.com",
    name="New User",
    picture="https://example.com/pic.jpg",
    email_verified=True,
  )

  with patch("src.api.auth.google_service.verify_google_token", new=AsyncMock(return_value=mock_info)):
    response = await client.post("/api/auth/google", json={"googleToken": "valid_token"})

  assert response.status_code == 200
  data = response.json()
  assert "token" in data
  assert "refresh_token" in data
  assert data["user"]["email"] == "new@user.com"
  assert data["user"]["name"] == "New User"
  assert data["user"]["role"] == "user"
  assert "id_user" in data["user"]


async def test_auth_google_unverified_email(client):
  mock_info = GoogleUserInfo(
    google_id="222",
    email="unverified@user.com",
    name=None,
    picture=None,
    email_verified=False,
  )

  with patch("src.api.auth.google_service.verify_google_token", new=AsyncMock(return_value=mock_info)):
    response = await client.post("/api/auth/google", json={"googleToken": "valid_token"})

  assert response.status_code == 401
  assert "not verified" in response.json()["detail"]


async def test_auth_google_invalid_token(client):
  with patch(
    "src.api.auth.google_service.verify_google_token",
    new=AsyncMock(side_effect=UnauthorizedError("Invalid Google token")),
  ):
    response = await client.post("/api/auth/google", json={"googleToken": "bad_token"})

  assert response.status_code == 401


async def test_auth_google_existing_user(client, db):
  existing = User(id=uuid.uuid4(), email="existing@user.com", role_id=1)
  db.add(existing)
  await db.flush()

  mock_info = GoogleUserInfo(
    google_id="333",
    email="existing@user.com",
    name="Existing",
    picture=None,
    email_verified=True,
  )

  with patch("src.api.auth.google_service.verify_google_token", new=AsyncMock(return_value=mock_info)):
    response = await client.post("/api/auth/google", json={"googleToken": "valid_token"})

  assert response.status_code == 200
  assert response.json()["user"]["email"] == "existing@user.com"


# verify_google_token (aud/iss check) ---------------------------------


def _mock_tokeninfo(status, payload):
  class FakeResponse:
    def __init__(self, status, payload):
      self.status_code = status
      self._payload = payload

    def json(self):
      return self._payload

  class FakeClient:
    def __init__(self, *args, **kwargs):
      pass

    async def __aenter__(self):
      return self

    async def __aexit__(self, *args):
      return False

    async def get(self, url, **kwargs):
      return FakeResponse(status, payload)

  return FakeClient


async def test_verify_google_token_wrong_aud():
  from src.api.auth.google_service import verify_google_token
  from src.core.exceptions import UnauthorizedError

  payload = {
    "aud": "other-client.apps.googleusercontent.com",
    "iss": "accounts.google.com",
    "sub": "123",
    "email": "user@example.com",
    "email_verified": True,
  }
  with patch("src.api.auth.google_service.settings.GOOGLE_CLIENT_ID", "my-client.apps.googleusercontent.com"):
    with patch("src.api.auth.google_service.httpx.AsyncClient", _mock_tokeninfo(200, payload)):
      try:
        await verify_google_token("token")
      except UnauthorizedError as exc:
        assert exc.message == "Invalid Google token"
      else:
        raise AssertionError("expected UnauthorizedError for wrong aud")


async def test_verify_google_token_wrong_iss():
  from src.api.auth.google_service import verify_google_token
  from src.core.exceptions import UnauthorizedError

  payload = {
    "aud": "my-client.apps.googleusercontent.com",
    "iss": "https://malicious.example.com",
    "sub": "123",
    "email": "user@example.com",
    "email_verified": True,
  }
  with patch("src.api.auth.google_service.settings.GOOGLE_CLIENT_ID", "my-client.apps.googleusercontent.com"):
    with patch("src.api.auth.google_service.httpx.AsyncClient", _mock_tokeninfo(200, payload)):
      try:
        await verify_google_token("token")
      except UnauthorizedError as exc:
        assert exc.message == "Invalid Google token"
      else:
        raise AssertionError("expected UnauthorizedError for wrong iss")


async def test_verify_google_token_valid():
  from src.api.auth.google_service import verify_google_token

  payload = {
    "aud": "my-client.apps.googleusercontent.com",
    "sub": "123",
    "email": "user@example.com",
    "name": "User",
    "email_verified": True,
  }
  with patch("src.api.auth.google_service.settings.GOOGLE_CLIENT_ID", "my-client.apps.googleusercontent.com"):
    with patch("src.api.auth.google_service.httpx.AsyncClient", _mock_tokeninfo(200, payload)):
      info = await verify_google_token("token")

  assert info.email == "user@example.com"
  assert info.google_id == "123"
  assert info.email_verified is True


# /api/auth/refresh ------------------------------------------------


async def _create_session(db, user_id, days_valid=7, revoked=False):
  session = UserSession(
    user_id=user_id,
    refresh_token="test_refresh_" + str(uuid.uuid4()),
    expires_at=datetime.now(tz=timezone.utc) + timedelta(days=days_valid),
    is_revoked=revoked,
  )
  db.add(session)
  await db.flush()
  return session


async def test_auth_refresh_success(client, db):
  user = User(id=uuid.uuid4(), email="refresh@user.com", role_id=1)
  db.add(user)
  await db.flush()
  session = await _create_session(db, user.id)
  saved_token = session.refresh_token

  response = await client.post("/api/auth/refresh", json={"refresh_token": saved_token})

  assert response.status_code == 200
  data = response.json()
  assert "token" in data
  assert "refresh_token" in data
  # New refresh token must differ from old one
  assert data["refresh_token"] != saved_token


async def test_auth_refresh_revoked_token(client, db):
  user = User(id=uuid.uuid4(), email="revoked@user.com", role_id=1)
  db.add(user)
  await db.flush()
  session = await _create_session(db, user.id, revoked=True)

  response = await client.post("/api/auth/refresh", json={"refresh_token": session.refresh_token})

  assert response.status_code == 401
  assert "expired" in response.json()["detail"] or "Invalid" in response.json()["detail"]


async def test_auth_refresh_expired_token(client, db):
  user = User(id=uuid.uuid4(), email="expired@user.com", role_id=1)
  db.add(user)
  await db.flush()
  session = await _create_session(db, user.id, days_valid=-1)  # expired yesterday

  response = await client.post("/api/auth/refresh", json={"refresh_token": session.refresh_token})

  assert response.status_code == 401


async def test_auth_refresh_invalid_token(client):
  response = await client.post("/api/auth/refresh", json={"refresh_token": "non_existent_token"})
  assert response.status_code == 401


# /api/auth/logout -------------------------------------------------


async def test_auth_logout_success(client, db):
  user = User(id=uuid.uuid4(), email="logout@user.com", role_id=1)
  db.add(user)
  await db.flush()
  session = await _create_session(db, user.id)

  response = await client.post("/api/auth/logout", json={"refresh_token": session.refresh_token})

  assert response.status_code == 204


async def test_auth_logout_invalid_token(client):
  response = await client.post("/api/auth/logout", json={"refresh_token": "bad_token"})
  assert response.status_code == 401
