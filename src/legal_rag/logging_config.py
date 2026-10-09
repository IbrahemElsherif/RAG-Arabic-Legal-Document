"""JSON logging. Every log line carries the `correlation_id` of the current request."""

import json
import logging
import sys
from contextvars import ContextVar
from datetime import UTC, datetime

# The API middleware sets this value per request (Phase 12).
# A ContextVar keeps the value separate for each concurrent async request.
correlation_id: ContextVar[str] = ContextVar("correlation_id", default="-")

# Attributes that every LogRecord has. Anything else came from `extra=` and goes into the JSON.
_STANDARD_ATTRS = set(vars(logging.makeLogRecord({}))) | {"message", "asctime"}


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "timestamp": datetime.fromtimestamp(record.created, tz=UTC).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "correlation_id": correlation_id.get(),
        }
        for key, value in vars(record).items():
            if key not in _STANDARD_ATTRS and not key.startswith("_"):
                payload[key] = value
        if record.exc_info:
            payload["exc_info"] = self.formatException(record.exc_info)
        return json.dumps(payload, ensure_ascii=False, default=str)


def setup_logging(level: str = "INFO") -> None:
    """Send JSON logs to stdout. Call this once at startup."""
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonFormatter())
    root = logging.getLogger()
    root.handlers = [handler]
    root.setLevel(level.upper())
