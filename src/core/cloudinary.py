import cloudinary
import cloudinary.uploader

from src.core.config import settings

cloudinary.config(
  cloud_name=settings.CLOUDINARY_CLOUD_NAME,
  api_key=settings.CLOUDINARY_API_KEY,
  api_secret=settings.CLOUDINARY_API_SECRET,
  secure=True,
)

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


def delete_image(public_id: str):
  cloudinary.uploader.destroy(public_id, resource_type="image")


def extract_public_id(url: str) -> str | None:
  if not url:
    return None
  try:
    after_upload = url.split("/upload/")[1]
    parts = after_upload.split("/", 1)[1]
    public_id = parts.rsplit(".", 1)[0]
    return public_id
  except Exception:
    return None
