#!/usr/bin/env python3
from dataclasses import replace

from runtime.kuuos_repository_live_object_materialization_types_v1_19 import (
    live_object_git_command_receipt_digest,
)
from runtime.v119_live_object_git_adapter import (
    run_bounded_object_git_command as run_original,
)
from runtime.v119_probe_status import normalize_probe_status


def run_bounded_object_git_command(*args, **kwargs):
    receipt, stdout, stderr = run_original(*args, **kwargs)
    code = normalize_probe_status(
        kwargs.get("operation", ""),
        receipt.return_code,
        receipt.timed_out,
        stderr,
    )
    if code != receipt.return_code:
        receipt = replace(receipt, return_code=code, receipt_digest="")
        receipt = replace(
            receipt,
            receipt_digest=live_object_git_command_receipt_digest(receipt),
        )
    return receipt, stdout, stderr
