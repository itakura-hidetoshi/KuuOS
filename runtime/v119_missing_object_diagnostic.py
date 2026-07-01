#!/usr/bin/env python3

_MARKERS = (
    "not a valid object name",
    "bad object",
    "could not get object info",
)


def is_missing_object_diagnostic(stderr: bytes) -> bool:
    text = stderr.decode("utf-8", errors="replace").lower()
    return any(marker in text for marker in _MARKERS)
