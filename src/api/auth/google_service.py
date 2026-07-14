import requests

from src.core.exceptions import UnauthorizedError
from . import schemas


def verify_google_token(access_token: str) -> schemas.GoogleUserInfo:
  # Llamar a la API de Google para obtener info del usuario
  googleResponse = requests.get(
    'https://www.googleapis.com/oauth2/v2/userinfo',
    headers={'Authorization': f'Bearer {access_token}'},
    timeout=10
  )
  
  if googleResponse.status_code != 200:
    raise UnauthorizedError(message="Invalid Google token")

  googleUser = googleResponse.json()

  # Extraer información del usuario
  return schemas.GoogleUserInfo(
    google_id=googleUser['id'],
    email=googleUser['email'],
    name=googleUser.get('name'),
    picture=googleUser.get('picture'),
    email_verified=googleUser.get('verified_email', False)
  )
