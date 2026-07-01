#!/usr/bin/env python3


def normalize_probe_status(operation: str, return_code: int, timed_out: bool) -> int:
    if operation != "observe-object-before":
        return return_code
    if timed_out or return_code in (0, -124, -127):
        return return_code
    return 1
