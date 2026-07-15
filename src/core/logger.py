import json
import logging
import sys
from contextvars import ContextVar
from datetime import datetime, timezone

_request_id: ContextVar[str] = ContextVar("request_id", default="")


def set_request_id(request_id: str) -> None:
  _request_id.set(request_id)


def get_request_id() -> str:
  return _request_id.get()


class JsonFormatter(logging.Formatter):
  def format(self, record: logging.LogRecord) -> str:
    log_entry = {
      "timestamp": datetime.now(tz=timezone.utc).isoformat(),
      "level": record.levelname,
      "logger": record.name,
      "message": record.getMessage(),
      "request_id": get_request_id(),
    }
    if hasattr(record, "props"):
      log_entry.update(record.props)
    return json.dumps(log_entry, ensure_ascii=False)


def setup_logger() -> logging.Logger:
  _logger = logging.getLogger("game_guides")
  _logger.setLevel(logging.INFO)

  handler = logging.StreamHandler(sys.stdout)
  handler.setFormatter(JsonFormatter())

  _logger.addHandler(handler)
  return _logger


logger = setup_logger()
