import pytest

from src.core.services.text_classification.text_preprocessor import (
    PREPROCESSOR_VERSION, OriginalSpan, preprocess_text,
)


@pytest.mark.parametrize("text,expected", [
    ("كتاب عربي", "کتاب عربی"),
    ("می\u200cرود و  API-42", "می\u200cرود و API-42"),
    ("رويداد\u00a0\u2009جدید", "رویداد جدید"),
    ("line1\r\nline2\u2028line3", "line1\nline2\nline3"),
    ("۱۴۰۳/۰۲/۰۱ \u200c v1.2.3", "۱۴۰۳/۰۲/۰۱ \u200c v1.2.3"),
    ("\u0643\u064a: 2026-10-21!", "کی: 2026-10-21!"),
    ("", ""),
])
def test_normalizes_preserving_technical_tokens(text, expected):
    processed = preprocess_text(text)
    assert processed.normalized_text == expected
    assert processed.original_text == text
    assert processed.version == PREPROCESSOR_VERSION
    assert len(processed.offsets) == len(expected)
    for i in range(len(expected)):
        assert preprocess_text(processed.source_slice(i, i + 1)).normalized_text == expected[i]


def test_half_open_spans_roundtrip_with_collapsed_spaces():
    obj = preprocess_text("ك  \tي\r\nAPI\u00a0v2")
    assert obj.normalized_text == "ک ی\nAPI v2"
    assert obj.source_slice(1, 2) == "  \t"
    assert obj.source_slice(3, 4) == "\r\n"
    assert obj.source_span(0, 3) == OriginalSpan(0, 5)
    assert obj.segments() == (OriginalSpan(0, 5), OriginalSpan(7, 13))


def test_invalid_spans_and_input_rejected():
    obj = preprocess_text("یک")
    for pair in [(-1, 1), (0, 0), (1, 3), (2, 1)]:
        with pytest.raises(ValueError):
            obj.source_span(*pair)
    with pytest.raises(TypeError):
        preprocess_text(None)


def test_long_document_complete_mapping():
    text = ("گزارش\u200cهای فني\u00a0\u00a0API ۲۰۲۶\n" * 1000) + "پایان"
    obj = preprocess_text(text)
    assert len(obj.segments()) == 1001
    assert obj.source_slice(0, len(obj.normalized_text)) == text
    assert obj.normalized_text.endswith("پایان")
