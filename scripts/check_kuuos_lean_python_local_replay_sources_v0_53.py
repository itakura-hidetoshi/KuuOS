#!/usr/bin/env python3
"""v0.53 exact original git-blob and new declaration static source checker.

This is not a substitute for Strict Lean, SQLite transaction verification,
cryptographic MAC security, or actual issuer authority.
"""
from __future__ import annotations

import ast
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PINNED = {
    "formal/KUOS/Architecture/LeanPythonLocallyMacBoundPlanClaimsV0_52.lean":
        "925d550004f0fcc9fb73e51db7d6bf065d168dcc",
    "runtime/kuuos_lean_python_local_mac_bound_plan_claims_v0_52.py":
        "37f1c4a47368012d7fbe597bf149ba5a441a982d",
    "formal/KUOS/Architecture/LeanPythonTwoDeclaredPlanResultClaimsV0_51.lean":
        "1236dc54b37181b660fddbe6f388d7db385d64f1",
    "formal/KUOS/PlanOS/MiddleWayBoundedSynthesisIntakeV1_03.lean":
        "ef7e9be80685cecf39630f53ac0e837c43abd828",
    "runtime/kuuos_planos_middle_way_bounded_synthesis_intake_kernel_v0_1.py":
        "d4e720d949022eb08e287362a4e5dc973241f408",
}
NEW_LEAN = "formal/KUOS/Architecture/LeanPythonLocalReplayLedgerBoundaryV0_53.lean"
NEW_RUNTIME = "runtime/kuuos_lean_python_local_replay_reservation_v0_53.py"
NEW_TEST = "tests/lean_python_extensions/test_local_replay_reservation_v0_53.py"
EXPECTED_IMPORTS = (
    "import Mathlib",
    "import KUOS.Architecture.LeanPythonLocallyMacBoundPlanClaimsV0_52",
    "import KUOS.Architecture.LeanPythonTwoDeclaredPlanResultClaimsV0_51",
    "import KUOS.PlanOS.MiddleWayBoundedSynthesisIntakeV1_03",
)
DECLARATIONS = (
    "structure LocalReplayTicket",
    "def sequenceKey",
    "def nonceKey",
    "structure LocalReplayLedger",
    "def locallyFresh",
    "def pairFresh",
    "def appendTicket",
    "def reserveIfPairFresh",
    "theorem rejected_pair_leaves_ledger_unchanged",
    "theorem successful_pair_retains_previous_sequences",
    "theorem successful_pair_contains_both_keys",
    "theorem fresh_pair_has_distinct_keys",
    "theorem local_replay_reservation_grants_no_original_execution",
)


def _blob(raw: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\x00" + raw).hexdigest()


def check(root: Path = ROOT) -> tuple[str, ...]:
    if type(root) is not type(ROOT) or root != ROOT:
        return ("trusted_root_required",)
    problems: list[str] = []
    for path, expected in PINNED.items():
        try:
            if _blob((ROOT / path).read_bytes()) != expected:
                problems.append("changed_pinned_source:" + path)
        except OSError:
            problems.append("missing_pinned_source:" + path)
    try:
        source = (ROOT / NEW_LEAN).read_text(encoding="utf-8")
        lines = tuple(line.strip() for line in source.splitlines())
        for token in EXPECTED_IMPORTS:
            if token not in lines:
                problems.append("missing_import:" + token)
        for token in DECLARATIONS:
            if not any(line == token or line.startswith(token + " ") for line in lines):
                problems.append("missing_declaration:" + token)
        if source.count("#print axioms ") != len(DECLARATIONS) - 2:
            problems.append("incomplete_axiom_audit")
        for bad in ("\nsorry", "\nadmit", "\naxiom ", "\nunsafe"):
            if bad in source:
                problems.append("forbidden_lean_escape")
    except (OSError, UnicodeError):
        problems.append("new_lean_source_unavailable")
    for path in (NEW_RUNTIME, NEW_TEST):
        try:
            ast.parse((ROOT / path).read_text(encoding="utf-8"))
        except (OSError, UnicodeError, SyntaxError, ValueError, RecursionError):
            problems.append("new_python_source_unavailable_or_invalid:" + path)
    return tuple(problems)


if __name__ == "__main__":
    issues = check()
    if issues:
        raise SystemExit("\n".join(issues))
    print("V053_SOURCE_GIT_BLOBS_MATCH; strict Lean and native CI separate")
