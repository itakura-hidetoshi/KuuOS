#!/usr/bin/env python3
"""
Validator for Superstring Emptiness String / Brane / Membrane Runtime v0.1.

This validator is intentionally dependency-light and uses only the Python standard library.
It checks the minimal runtime packet invariants:
- strings are non-reified relational vibration traces
- branes are local world-support surfaces, not absolute worlds
- membranes preserve authority non-expansion and obstruction visibility
- missing evidence fails closed to HOLD/REJECT
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

REQUIRED_TOP = ["string_brane_membrane_packet"]

REQUIRED_STRING_TRUE = [
    "non_reification_guard",
    "two_truths_gap_guard",
]

REQUIRED_MEMBRANE_TRUE = [
    "authority_non_expansion_guard",
]

REQUIRED_ADMISSION_TRUE = [
    "dependent_origination_trace_present",
    "observer_record_surface_present",
    "obstruction_visibility_preserved",
]

ALLOWED_DECISIONS = {
    "REJECT",
    "HOLD",
    "ADMIT_AS_CANDIDATE",
    "ADMIT_AS_CONVENTIONAL_RUNTIME_SURFACE",
    "HOLD_OR_ADMIT_AS_CANDIDATE",
}

FORBIDDEN_VALUES = {
    "independent_substance",
    "absolute_world",
    "final_authority",
    "direct_execute_authority",
    "graph_only_indranet",
    "obstruction_erasure",
    "silent_strong_upgrade",
}


def load_packet(path: Path) -> Dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() in {".json"}:
        return json.loads(text)
    # Minimal YAML-like fallback: for CI examples, prefer JSON.
    raise ValueError("Only JSON packet validation is supported by this minimal validator.")


def walk_values(obj: Any) -> List[str]:
    values: List[str] = []
    if isinstance(obj, dict):
        for v in obj.values():
            values.extend(walk_values(v))
    elif isinstance(obj, list):
        for v in obj:
            values.extend(walk_values(v))
    else:
        values.append(str(obj))
    return values


def validate(packet: Dict[str, Any]) -> Tuple[bool, List[str], str]:
    errors: List[str] = []

    for key in REQUIRED_TOP:
        if key not in packet:
            errors.append(f"missing top-level key: {key}")

    root = packet.get("string_brane_membrane_packet", {})
    if not isinstance(root, dict):
        errors.append("string_brane_membrane_packet must be an object")
        return False, errors, "REJECT"

    string = root.get("string", {})
    brane = root.get("brane", {})
    membrane = root.get("membrane", {})
    admission = root.get("admission", {})

    for name, obj in [("string", string), ("brane", brane), ("membrane", membrane), ("admission", admission)]:
        if not isinstance(obj, dict):
            errors.append(f"{name} must be an object")

    for key in REQUIRED_STRING_TRUE:
        if string.get(key) is not True:
            errors.append(f"string.{key} must be true")

    for key in REQUIRED_MEMBRANE_TRUE:
        if membrane.get(key) is not True:
            errors.append(f"membrane.{key} must be true")

    for key in REQUIRED_ADMISSION_TRUE:
        if admission.get(key) is not True:
            errors.append(f"admission.{key} must be true")

    if not membrane.get("rollback_or_hold_route"):
        errors.append("membrane.rollback_or_hold_route must be present")

    decision = str(admission.get("decision", "HOLD"))
    if decision not in ALLOWED_DECISIONS:
        errors.append(f"admission.decision is not allowed: {decision}")

    values = set(walk_values(root))
    forbidden_hits = sorted(values.intersection(FORBIDDEN_VALUES))
    for hit in forbidden_hits:
        errors.append(f"forbidden runtime value detected: {hit}")

    if errors:
        return False, errors, "HOLD" if decision != "REJECT" else "REJECT"

    if decision == "ADMIT_AS_CONVENTIONAL_RUNTIME_SURFACE":
        if brane.get("world_scope") not in {"conventional_effective_surface", "local_effective_world_surface"}:
            errors.append("conventional admission requires conventional/local effective world surface")
            return False, errors, "HOLD"

    return True, [], decision


def main(argv: List[str]) -> int:
    if len(argv) != 2:
        print("usage: validate_superstring_emptiness_string_brane_membrane_v0_1.py packet.json", file=sys.stderr)
        return 2

    path = Path(argv[1])
    try:
        packet = load_packet(path)
        ok, errors, decision = validate(packet)
    except Exception as exc:
        print(json.dumps({"ok": False, "decision": "REJECT", "errors": [str(exc)]}, ensure_ascii=False, indent=2))
        return 1

    print(json.dumps({"ok": ok, "decision": decision, "errors": errors}, ensure_ascii=False, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
