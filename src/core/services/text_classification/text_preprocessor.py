"""Versioned, offset-preserving Persian Unicode preprocessing.

Offsets are zero-based half-open Python Unicode code-point indexes, never bytes.
No transliteration, digit conversion, punctuation removal or case-folding occurs.
"""
from __future__ import annotations

from dataclasses import dataclass

PREPROCESSOR_VERSION = "fa-offset-v1"
_LETTERS = str.maketrans({"ي": "ی", "ى": "ی", "ك": "ک"})
_LINE_BREAKS = frozenset("\r\n\u0085\u2028\u2029")


@dataclass(frozen=True)
class OriginalSpan:
    start: int
    end: int


@dataclass(frozen=True)
class PreprocessedText:
    original_text: str
    normalized_text: str
    offsets: tuple[OriginalSpan, ...]
    version: str = PREPROCESSOR_VERSION

    def __post_init__(self) -> None:
        if len(self.normalized_text) != len(self.offsets):
            raise ValueError("Each normalized code point requires one origin span")
        previous_end = 0
        for span in self.offsets:
            if not previous_end <= span.start < span.end <= len(self.original_text):
                raise ValueError("Invalid or overlapping origin spans")
            previous_end = span.end

    def source_span(self, start: int, end: int) -> OriginalSpan:
        """Map a non-empty normalized interval onto exact original code points."""
        if not (0 <= start < end <= len(self.offsets)):
            raise ValueError("Normalized interval must be non-empty and in bounds")
        return OriginalSpan(self.offsets[start].start, self.offsets[end - 1].end)

    def source_slice(self, start: int, end: int) -> str:
        span = self.source_span(start, end)
        return self.original_text[span.start:span.end]

    def segments(self) -> tuple[OriginalSpan, ...]:
        """Return original spans for non-empty lines, preserving source boundaries."""
        segments: list[OriginalSpan] = []
        start = 0
        for index, char in enumerate(self.normalized_text):
            if char == "\n":
                if index > start:
                    segments.append(self.source_span(start, index))
                start = index + 1
        if start < len(self.normalized_text):
            segments.append(self.source_span(start, len(self.normalized_text)))
        return tuple(segments)


def preprocess_text(text: str) -> PreprocessedText:
    """Normalize Arabic Yeh/Kaf and horizontal whitespace without losing evidence offsets.

    Consecutive horizontal whitespace maps to one ASCII space covering its full
    source interval. CRLF and other Unicode line breaks map to one LF. ZWNJ
    (U+200C) is always retained. Letter normalization is deliberately 1:1.
    Unicode composition is NOT applied because it can alter offset cardinality.
    """
    if not isinstance(text, str):
        raise TypeError("text must be str")
    result: list[str] = []
    offsets: list[OriginalSpan] = []
    index = 0
    while index < len(text):
        char = text[index]
        if char in _LINE_BREAKS:
            end = index + 2 if char == "\r" and text[index:index + 2] == "\r\n" else index + 1
            result.append("\n")
            offsets.append(OriginalSpan(index, end))
        elif char.isspace():
            end = index + 1
            while end < len(text) and text[end].isspace() and text[end] not in _LINE_BREAKS:
                end += 1
            result.append(" ")
            offsets.append(OriginalSpan(index, end))
        else:
            end = index + 1
            result.append(char.translate(_LETTERS))
            offsets.append(OriginalSpan(index, end))
        index = end
    return PreprocessedText(text, "".join(result), tuple(offsets))
