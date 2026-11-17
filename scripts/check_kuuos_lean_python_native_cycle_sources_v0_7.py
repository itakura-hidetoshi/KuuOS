#!/usr/bin/env python3
"""Source-byte guard for native full-cycle deterministic receipt reconstruction.

The original fixture and receipt constructors must not drift without reviewing
the v0.7 fixed reconstruction constants. This only checks selected Git blobs,
not Lean elaboration, Python equivalence, or real-world receipt provenance.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SOURCE_GIT_BLOBS = {
    "runtime/kuuos_qi_world_native_full_cycle_v1_3.py": "9830b98746fbe8cf550562a0719374471ed6e0e5",
    "runtime/kuuos_act_os_store_v0_1.py": "24ebc89667c493498926e8d03bb21f952f448cce",
    "runtime/kuuos_plan_os_kernel_v0_1.py": "6942b32353b476fe8848d39c548d3cd2fe93ccff",
    "runtime/kuuos_decision_os_wa_kernel_v0_3.py": "0ebc222ac5c73da86fea8c4e09f03782f84314b3",
    "runtime/kuuos_act_os_kernel_v0_1.py": "db91d45cefd8982309f4a8d58e792f0df0c2c5d4",
    "runtime/kuuos_lean_python_os_path_composition_v0_6.py": "068158c2e4f90f5040f83504218e60752a5472ed",
    "runtime/kuuos_lean_python_os_registry_v0_5.py": "7bb5e7cf2e0fea1a14029a00301708604510b371",
    "runtime/kuuos_belief_os_types_v0_1.py": "32eac0fa0b1cb52a999f0a17e67015905a541ba7",
}

REQUIRED_PATHS = (
    "runtime/kuuos_lean_python_native_cycle_ledger_replay_v0_7.py",
    "tests/test_kuuos_lean_python_native_cycle_ledger_replay_v0_7.py",
    "docs/KUUOS_LEAN_PYTHON_NATIVE_CYCLE_LEDGER_REPLAY_v0_7.md",
)


def check_sources(root: Path = ROOT) -> tuple[str, ...]:
    errors: list[str] = []
    for path, expected in SOURCE_GIT_BLOBS.items():
        full = root / path
        if not full.is_file():
            errors.append("source_missing:" + path)
            continue
        data = full.read_bytes()
        actual = hashlib.sha1(
            b"blob " + str(len(data)).encode("ascii") + b"\0" + data
        ).hexdigest()
        if actual != expected:
            errors.append("source_byte_drift:" + path)
    for path in REQUIRED_PATHS:
        if not (root / path).is_file():
            errors.append("candidate_file_missing:" + path)
    return tuple(sorted(errors))


def main() -> int:
    errors = check_sources()
    for issue in errors:
        print("BLOCKED:", issue)
    if not errors:
        print("SOURCE_BYTES_MATCH: 8 source blobs and three v0.7 files; "
              "source guard, not Lean/Python refinement certification")
    return int(bool(errors))


if __name__ == "__main__":
    raise SystemExit(main())
