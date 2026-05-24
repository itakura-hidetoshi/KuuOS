#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[1]
POLICY_PATH = ROOT / "policies" / "daemon_core_boundary_policy_v0_1.json"
DAEMON_PATH = ROOT / "runtime" / "kuuos_runtime_daemon_v0_1.py"

FORBIDDEN_IMPORT_PATTERNS = [
    r"validate_.*",
    r"validator_.*",
    r"governance.*validator",
    r"all_governance",
]

FORBIDDEN_CALL_PATTERNS = [
    r"\.unlink\s*\(",
    r"\.rmdir\s*\(",
    r"shutil\.rmtree\s*\(",
    r"os\.remove\s*\(",
    r"os\.unlink\s*\(",
]

FORBIDDEN_AUTHORITY_TRUE_PATTERNS = [
    r"grants_truth_authority\s*=\s*True",
    r"grants_final_commitment_authority\s*=\s*True",
    r"grants_memory_overwrite_authority\s*=\s*True",
    r"grants_clinical_authority\s*=\s*True",
    r"grants_theorem_authority\s*=\s*True",
    r"grants_completed_identity_authority\s*=\s*True",
]

REQUIRED_DAEMON_TOKENS = [
    "max_ticks",
    "STOP_REASONS",
    "write_qi_projection_outputs",
    "NON_AUTHORITY_FLAGS",
]


def load_policy() -> dict:
    return json.loads(POLICY_PATH.read_text(encoding="utf-8"))


def fail(message: str) -> int:
    print(f"ERROR: {message}")
    return 1


def main() -> int:
    if not POLICY_PATH.is_file():
        return fail(f"missing policy: {POLICY_PATH}")
    if not DAEMON_PATH.is_file():
        return fail(f"missing daemon core: {DAEMON_PATH}")

    policy = load_policy()
    text = DAEMON_PATH.read_text(encoding="utf-8")

    if policy.get("policy_status") != "DAEMON_CORE_BOUNDARY_POLICY_ACTIVE":
        return fail("policy is not active")
    if policy.get("core_principle") != "daemon_core_is_minimal_runtime_orchestrator_not_semantic_authority":
        return fail("unexpected daemon core principle")

    for flag, expected in policy.get("authority_invariants", {}).items():
        if expected is not False:
            return fail(f"authority invariant must be false: {flag}")

    for pattern in FORBIDDEN_IMPORT_PATTERNS:
        if re.search(pattern, text):
            return fail(f"daemon core contains forbidden heavy validator import/pattern: {pattern}")

    for pattern in FORBIDDEN_CALL_PATTERNS:
        if re.search(pattern, text):
            return fail(f"daemon core contains forbidden destructive file operation: {pattern}")

    for pattern in FORBIDDEN_AUTHORITY_TRUE_PATTERNS:
        if re.search(pattern, text):
            return fail(f"daemon core grants forbidden authority: {pattern}")

    for token in REQUIRED_DAEMON_TOKENS:
        if token not in text:
            return fail(f"daemon core missing required bounded/non-authority token: {token}")

    if "for tick_index in range(max_ticks)" not in text:
        return fail("daemon core loop must be bounded by range(max_ticks)")

    print("PASS: daemon core boundary policy v0.1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
