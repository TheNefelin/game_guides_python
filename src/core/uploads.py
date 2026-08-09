import io

from fastapi import UploadFile
from PIL import Image

from src.core.exceptions import AppError

MAX_IMAGE_SIZE_BYTES = 5 * 1024 * 1024  # 5 MB
MAX_IMAGE_DIMENSION = 8192  # px, evita decompression bombs / reventar memoria
ALLOWED_FORMATS = {"JPEG", "PNG", "GIF", "WEBP"}
CHUNK_SIZE = 1024 * 1024  # 1 MB por lectura


def _looks_like_image(data: bytes) -> bool:
  if data.startswith(b"\xff\xd8\xff"):  # JPEG
    return True
  if data.startswith(b"\x89PNG\r\n\x1a\n"):  # PNG
    return True
  if data.startswith((b"GIF87a", b"GIF89a")):  # GIF
    return True
  if len(data) >= 12 and data[:4] == b"RIFF" and data[8:12] == b"WEBP":  # WebP
    return True
  return False


# Valida que el archivo sea una imagen real y segura. Tres capas:
#   1. content-type image/* + magic bytes (filtro barato, evita leer basura)
#   2. decodificación real con Pillow (verify) — rechaza header+basura falsos
#   3. dimensiones máximas + formato permitido — evita decompression bombs
async def validate_image_upload(file: UploadFile) -> bytes:
  if not file.content_type or not file.content_type.startswith("image/"):
    raise AppError("Only image files are allowed")

  data = bytearray()
  while True:
    chunk = await file.read(CHUNK_SIZE)
    if not chunk:
      break
    data.extend(chunk)
    if len(data) > MAX_IMAGE_SIZE_BYTES:
      raise AppError("Image exceeds the maximum size of 5MB")

  content = bytes(data)
  if not _looks_like_image(content):
    raise AppError("Invalid image file")

  try:
    with Image.open(io.BytesIO(content)) as image:
      image.verify()
      if image.format not in ALLOWED_FORMATS:
        raise AppError(f"Unsupported image format: {image.format}")
      if image.width > MAX_IMAGE_DIMENSION or image.height > MAX_IMAGE_DIMENSION:
        raise AppError(f"Image exceeds the maximum dimensions of {MAX_IMAGE_DIMENSION}px")
  except AppError:
    raise
  except Exception:
    raise AppError("Invalid image file")

  return content
