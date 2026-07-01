#!/usr/bin/env python3
from runtime.v119_missing_object_diagnostic import is_missing_object_diagnostic

TARGET_PROBE_OPERATION = "observe-object-before"


def normalize_probe_status(
    operation: str,
    return_code: int,
    timed_out: bool,
    stderr: bytes = b"",
) -> int:
    if operation != TARGET_PROBE_OPERATION:
        return return_code
    if timed_out or return_code in (0, 1, -124, -127):
        return return_code
    return 1 if is_missing_object_diagnostic(stderr) else return_code
