import logging

from src.host.observability import SafeJsonFormatter


def test_logging_never_emits_secret_or_report_text():
    record = logging.makeLogRecord({
        "msg": "report-text=CONFIDENTIAL password=SECRET", "levelname": "ERROR",
        "levelno": 40, "args": (),
    })
    result = SafeJsonFormatter().format(record)
    assert "CONFIDENTIAL" not in result
    assert "SECRET" not in result
    assert "internal_event" in result
