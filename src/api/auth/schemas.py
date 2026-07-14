from typing import Optional
from pydantic import BaseModel, EmailStr


# Google OAuth user info (response from Google API)
class GoogleUserInfo(BaseModel):
  google_id: str
  email: str
  name: Optional[str] = None
  picture: Optional[str] = None
  email_verified: bool


# Auth request
class AuthGoogleRequest(BaseModel):
  googleToken: str


# Authenticated user (returned to frontend)
class AuthGoogleUser(BaseModel):
  id_user: str
  email: EmailStr
  name: Optional[str] = None
  picture: Optional[str] = None
  role: str


# Auth response
class AuthGoogleResponse(BaseModel):
  token: str
  refresh_token: str
  user: AuthGoogleUser


# Refresh
class AuthRefreshRequest(BaseModel):
  refresh_token: str


class AuthRefreshResponse(BaseModel):
  token: str
  refresh_token: str