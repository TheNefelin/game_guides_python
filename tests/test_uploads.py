import io

from fastapi import UploadFile
from starlette.datastructures import Headers
import pytest
from PIL import Image

from src.core.exceptions import AppError
from src.core.uploads import validate_image_upload, MAX_IMAGE_SIZE_BYTES, MAX_IMAGE_DIMENSION


def _bytes_for(fmt: str, size: tuple[int, int] = (4, 4)) -> bytes:
  if fmt == "WEBP":
    mode, ext = "RGB", "WEBP"
  elif fmt == "GIF":
    mode, ext = "P", "GIF"
  else:
    mode, ext = "RGB", fmt
  buffer = io.BytesIO()
  Image.new(mode, size).save(buffer, format=ext)
  return buffer.getvalue()


def _upload(content: bytes, content_type: str = "image/png", filename: str = "pic.png") -> UploadFile:
  headers = Headers({"content-type": content_type})
  return UploadFile(file=io.BytesIO(content), filename=filename, headers=headers)


async def test_validate_accepts_png():
  payload = _bytes_for("PNG")
  result = await validate_image_upload(_upload(payload))
  assert result == payload


async def test_validate_accepts_jpeg_and_gif_and_webp():
  for fmt in ("JPEG", "GIF", "WEBP"):
    payload = _bytes_for(fmt)
    result = await validate_image_upload(_upload(payload, content_type=f"image/{fmt.lower()}"))
    assert result == payload


async def test_validate_rejects_wrong_content_type():
  upload = _upload(_bytes_for("PNG"), content_type="text/plain")
  with pytest.raises(AppError, match="Only image files"):
    await validate_image_upload(upload)


async def test_validate_rejects_non_image_bytes():
  upload = _upload(b"MZ\x90\x00" + b"not an image", content_type="image/png")
  with pytest.raises(AppError, match="Invalid image file"):
    await validate_image_upload(upload)


async def test_validate_rejects_oversized_file():
  upload = _upload(b"x" * (MAX_IMAGE_SIZE_BYTES + 1))
  with pytest.raises(AppError, match="maximum size"):
    await validate_image_upload(upload)


async def test_validate_rejects_excessive_dimensions():
  big = _bytes_for("PNG", size=(MAX_IMAGE_DIMENSION + 1, 4))
  with pytest.raises(AppError, match="maximum dimensions"):
    await validate_image_upload(_upload(big))


async def test_delete_image_ok(monkeypatch):
  import cloudinary.uploader as cu
  from src.core import cloudinary as c
  monkeypatch.setattr(cu, "destroy", lambda *a, **k: {"result": "ok"})
  assert c.delete_image("games/abc") is True


async def test_delete_image_not_found_treated_as_success(monkeypatch):
  import cloudinary.uploader as cu
  from src.core import cloudinary as c
  monkeypatch.setattr(cu, "destroy", lambda *a, **k: {"result": "not found"})
  assert c.delete_image("games/abc") is True


async def test_delete_image_unexpected_status_is_false(monkeypatch):
  import cloudinary.uploader as cu
  from src.core import cloudinary as c
  monkeypatch.setattr(cu, "destroy", lambda *a, **k: {"result": "error"})
  assert c.delete_image("games/abc") is False


async def test_delete_image_raises_is_false(monkeypatch):
  import cloudinary.uploader as cu
  from src.core import cloudinary as c
  def boom(*a, **k):
    raise RuntimeError("network")
  monkeypatch.setattr(cu, "destroy", boom)
  assert c.delete_image("games/abc") is False
