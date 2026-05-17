#!/usr/bin/env python3
"""Release/finality packet-chain validator for Superstring Emptiness SBM Runtime v0.2."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List

REQUIRED_RELEASE_KEYS = ["id", "version", "depends_on", "release_claim", "admission_surface", "required_guards", "blocked_collapses", "decision"]
REQUIRED_FINALITY_KEYS = ["id", "version", "finality_type", "declaration", "locked_invariants", "future_update_policy", "decision"]
REQUIRED_ADMISSION_FALSE = ["strong_release_allowed", "execute_authority", "world_update_authority"]
REQUIRED_FUTURE_TRUE = ["additive_only", "tighten_only_default", "same_root_required", "overwrite_forbidden", "destructive_replacement_forbidden"]
REQUIRED_LOCKED = {
    "non_reification_required",
    "dependent_origination_required",
    "two_truths_gap_required",
    "observer_record_surface_required",
    "authority_non_expansion_required",
    "obstruction_visibility_required",
    "rollback_or_hold_route_required",
    "execution_authority_not_opened",
}


def load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_release(data: Dict[str, Any], repo_root: Path) -> List[str]:
    errors: List[str] = []
    for key in REQUIRED_RELEASE_KEYS:
        if key not in data:
            errors.append(f"release missing key: {key}")
    for dep in data.get("depends_on", []):
        if not (repo_root / dep).exists():
            errors.append(f"release dependency missing: {dep}")
    admission = data.get("admission_surface", {})
    for key in REQUIRED_ADMISSION_FALSE:
        if admission.get(key) is not False:
            errors.append(f"release.admission_surface.{key} must be false")
    if data.get("decision") != "RELEASE_AS_CANDIDATE_RUNTIME_BRIDGE":
        errors.append("release.decision must be RELEASE_AS_CANDIDATE_RUNTIME_BRIDGE")
    return errors


def validate_finality(data: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    for key in REQUIRED_FINALITY_KEYS:
        if key not in data:
            errors.append(f"finality missing key: {key}")
    if data.get("finality_type") != "non_mutating_declaration":
        errors.append("finality.finality_type must be non_mutating_declaration")
    locked = set(data.get("locked_invariants", []))
    for inv in sorted(REQUIRED_LOCKED - locked):
        errors.append(f"finality missing locked invariant: {inv}")
    future = data.get("future_update_policy", {})
    for key in REQUIRED_FUTURE_TRUE:
        if future.get(key) is not True:
            errors.append(f"finality.future_update_policy.{key} must be true")
    if data.get("decision") != "FINALIZE_V0_1_AS_BASELINE_CANDIDATE":
        errors.append("finality.decision must be FINALIZE_V0_1_AS_BASELINE_CANDIDATE")
    return errors


def main(argv: List[str]) -> int:
    if len(argv) != 3:
        print("usage: validate_superstring_emptiness_sbm_packet_chain_v0_2.py release.json finality.json", file=sys.stderr)
        return 2
    repo_root = Path.cwd()
    errors: List[str] = []
    try:
        release = load_json(Path(argv[1]))
        finality = load_json(Path(argv[2]))
        errors.extend(validate_release(release, repo_root))
        errors.extend(validate_finality(finality))
    except Exception as exc:
        errors.append(str(exc))
    ok = not errors
    print(json.dumps({"ok": ok, "errors": errors}, ensure_ascii=False, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
