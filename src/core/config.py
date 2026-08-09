import json

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
  DEBUG: bool = False

  SECRET_KEY: str
  DATABASE_URL: str
  API_KEY: str
  GOOGLE_CLIENT_ID: str | None = None
  TEST_DATABASE_URL: str | None = None

  CORS_ORIGINS: str

  CLOUDINARY_CLOUD_NAME: str
  CLOUDINARY_API_KEY: str
  CLOUDINARY_API_SECRET: str

  BREVO_API_KEY: str
  BREVO_FROM_EMAIL: str
  BREVO_FROM_NAME: str
  TEST_BREVO_EMAIL: str | None = None

  @property
  def cors_origins_list(self) -> list[str]:
    return json.loads(self.CORS_ORIGINS)

  model_config = SettingsConfigDict(
    env_file=".env",
    env_file_encoding="utf-8",
    case_sensitive=False,
    extra="ignore",
  )


settings = Settings()