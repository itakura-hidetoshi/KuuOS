#!/usr/bin/env python3

TARGET_PROBE_OPERATION = "observe-object-before"


def normalize_probe_status(operation: str, return_code: int, timed_out: bool) -> int:
    if operation != TARGET_PROBE_OPERATION:
        return return_code
    if timed_out or return_code in (0, -124, -127):
        return return_code
    return 1
