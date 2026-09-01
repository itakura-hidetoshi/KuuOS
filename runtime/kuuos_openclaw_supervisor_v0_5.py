#!/usr/bin/env python3
"""Serialized public entrypoint for the KuuOS ↔ OpenClaw supervisor v0.5.

The original v0.5 implementation is retained byte-for-byte in
`kuuos_openclaw_supervisor_v0_5_impl.py`.  This entrypoint adds two operational
hardening properties without changing the authority model:

1. all supervisor-internal v0.3 audit reconciliations share one process-local
   lock, preventing periodic and gap-triggered syncs from racing the same
   append-only ledger/checkpoint state;
2. the live JSONL reader never parses a trailing record until its terminating
   newline is present, so a concurrently appended partial tail is retried rather
   than misclassified as corruption.

The wrapper then re-exports the implementation surface so existing v0.5 tests,
commands, and documentation keep one stable public filename.
"""

from __future__ import annotations

import importlib.util
import json
import sys
import threading
from pathlib import Path
from typing import Any

_IMPL_PATH = Path(__file__).with_name("kuuos_openclaw_supervisor_v0_5_impl.py")
_SPEC = importlib.util.spec_from_file_location("kuuos_openclaw_supervisor_v0_5_impl", _IMPL_PATH)
if _SPEC is None or _SPEC.loader is None:
    raise RuntimeError(f"unable to load KuuOS OpenClaw supervisor implementation: {_IMPL_PATH}")
_IMPL = importlib.util.module_from_spec(_SPEC)
sys.modules[_SPEC.name] = _IMPL
_SPEC.loader.exec_module(_IMPL)

_AUDIT_SYNC_LOCK = threading.Lock()
_BASE_RUN_AUDIT_ONCE = _IMPL.run_audit_once


def _serialized_run_audit_once(args: Any, paths: Any) -> dict[str, Any]:
    """Single-writer boundary for supervisor-owned v0.3 reconciliation calls."""
    with _AUDIT_SYNC_LOCK:
        return _BASE_RUN_AUDIT_ONCE(args, paths)


def _robust_read_new_jsonl(path: Path, start_offset: int) -> tuple[int, list[dict[str, Any]]]:
    """Read complete JSONL records only; leave an unterminated tail for retry."""
    if not path.exists():
        return start_offset, []
    with path.open("r", encoding="utf-8") as handle:
        handle.seek(start_offset)
        records: list[dict[str, Any]] = []
        while True:
            record_offset = handle.tell()
            line = handle.readline()
            if not line:
                break
            if not line.endswith("\n"):
                handle.seek(record_offset)
                break
            line = line.strip()
            if not line:
                continue
            try:
                value = json.loads(line)
            except json.JSONDecodeError as error:
                raise RuntimeError(f"corrupt complete v0.4 live hint ledger record: {error}") from error
            if not isinstance(value, dict):
                raise RuntimeError("invalid non-object v0.4 live hint ledger record")
            records.append(value)
        return handle.tell(), records


# Patch the implementation module itself: functions defined there resolve these
# globals at call time, so periodic, triggered, and initial reconciliation all
# pass through the same lock without duplicating the main supervisor logic.
_IMPL.run_audit_once = _serialized_run_audit_once
_IMPL.read_new_jsonl = _robust_read_new_jsonl

# Preserve the stable public module surface used by focused tests and operators.
for _name in dir(_IMPL):
    if _name.startswith("__"):
        continue
    globals().setdefault(_name, getattr(_IMPL, _name))

# Explicitly expose the hardened replacements, even if names are refactored in
# the retained implementation later.
run_audit_once = _serialized_run_audit_once
read_new_jsonl = _robust_read_new_jsonl


if __name__ == "__main__":
    raise SystemExit(_IMPL.main())
