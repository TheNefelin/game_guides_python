import json

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
  DEBUG: bool = False

  SECRET_KEY: str
  DATABASE_URL: str
  API_KEY: str
  TEST_DATABASE_URL: str

  CORS_ORIGINS: str

  CLOUDINARY_CLOUD_NAME: str
  CLOUDINARY_API_KEY: str
  CLOUDINARY_API_SECRET: str

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