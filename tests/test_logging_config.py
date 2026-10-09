import json
import logging
import sys

from legal_rag.logging_config import JsonFormatter, correlation_id, setup_logging


def _format(record: logging.LogRecord) -> dict:
    return json.loads(JsonFormatter().format(record))


def test_json_line_has_required_fields():
    record = logging.makeLogRecord(
        {"name": "t", "levelname": "INFO", "msg": "hello %s", "args": ("x",)}
    )
    line = _format(record)
    assert line["message"] == "hello x"
    assert line["level"] == "INFO"
    assert line["logger"] == "t"
    assert line["correlation_id"] == "-"
    assert "timestamp" in line


def test_correlation_id_and_extra_fields():
    token = correlation_id.set("req-123")
    try:
        record = logging.makeLogRecord({"msg": "المادة ١٤٧", "article": 147})
        line = _format(record)
    finally:
        correlation_id.reset(token)
    assert line["correlation_id"] == "req-123"
    assert line["article"] == 147
    assert line["message"] == "المادة ١٤٧"


def test_exception_is_logged():
    try:
        raise ValueError("boom")
    except ValueError:
        record = logging.makeLogRecord({"msg": "failed", "exc_info": sys.exc_info()})
    assert "ValueError: boom" in _format(record)["exc_info"]


def test_setup_logging_writes_json(capsys):
    setup_logging("debug")
    logging.getLogger("legal_rag.test").debug("ready")
    out = capsys.readouterr().out.strip()
    assert json.loads(out)["message"] == "ready"
