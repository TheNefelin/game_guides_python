import cloudinary
import cloudinary.uploader

from src.core.config import settings
from src.core.logger import logger

cloudinary.config(
  cloud_name=settings.CLOUDINARY_CLOUD_NAME,
  api_key=settings.CLOUDINARY_API_KEY,
  api_secret=settings.CLOUDINARY_API_SECRET,
  secure=True,
)

# UPLOAD 16:9 (1280x720 recortado) ------------------------------------
def upload_image_16_9(file_bytes: bytes, folder: str, public_id: str = None) -> tuple[str, str]:
  result = cloudinary.uploader.upload(
    file_bytes,
    folder=folder,
    public_id=public_id,
    resource_type="image",
    format="webp",
    transformation={
      "width": 1280,
      "height": 720,
      "crop": "fill",
      "gravity": "center",
      "quality": "auto",
    },
  )
  return result["secure_url"], result["public_id"]


# UPLOAD 1:1 (512x512 recortado) --------------------------------------
def upload_image_1_1(file_bytes: bytes, folder: str, public_id: str = None) -> tuple[str, str]:
  result = cloudinary.uploader.upload(
    file_bytes,
    folder=folder,
    public_id=public_id,
    resource_type="image",
    format="webp",
    transformation={
      "width": 512,
      "height": 512,
      "crop": "fill",
      "gravity": "center",
      "quality": "auto",
    },
  )
  return result["secure_url"], result["public_id"]


# UPLOAD LIBRE (proporción original) ----------------------------------
def upload_image_free(file_bytes: bytes, folder: str, public_id: str = None) -> tuple[str, str]:
  result = cloudinary.uploader.upload(
    file_bytes,
    folder=folder,
    public_id=public_id,
    resource_type="image",
    format="webp",
  )
  return result["secure_url"], result["public_id"]


# DELETE IMAGE (con reintentos) ---------------------------------------
def delete_image(public_id: str, retries: int = 2) -> bool:
  for attempt in range(retries):
    try:
      result = cloudinary.uploader.destroy(public_id, resource_type="image")
    except Exception as exc:
      if attempt < retries - 1:
        continue
      logger.error(f"Cloudinary destroy failed for {public_id}: {exc}")
      return False
    status = result.get("result") if isinstance(result, dict) else None
    if status in ("ok", "not found"):
      return True
    if attempt < retries - 1:
      continue
    logger.error(f"Cloudinary destroy returned unexpected status for {public_id}: {result}")
    return False
  return False


# EXTRACT PUBLIC ID (del URL, saltando transformaciones) --------------
def extract_public_id(url: str) -> str | None:
  if not url:
    return None
  try:
    after_upload = url.split("/upload/")[1]
    # Saltar el bloque de transformación opcional (c_fill,h_720,q_auto,w_1280,f_webp)
    # hasta llegar a la versión (v<timestamp>). Sin esto, destroy() recibe un
    # public_id inválido ("v.../folder/file") y Cloudinary no borra el archivo.
    while after_upload and not after_upload.startswith("v"):
      after_upload = after_upload.split("/", 1)[1]
    parts = after_upload.split("/", 1)[1] if "/" in after_upload else after_upload
    public_id = parts.rsplit(".", 1)[0]
    return public_id
  except Exception:
    return None
