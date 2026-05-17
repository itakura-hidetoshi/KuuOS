#!/usr/bin/env python3
"""Validator for Superstring Emptiness Observer-Record-Scale Bridge v0.6."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

REQUIRED_TOP = "observer_record_scale_bridge_packet"
REQUIRED_BRIDGE_TRUE = [
    "observer_context_present",
    "record_surface_present",
    "scale_regime_present",
    "backaction_visibility",
    "two_truths_gap_guard",
    "non_reification_guard",
    "obstruction_visibility_rule",
    "authority_non_expansion_guard",
]
REQUIRED_BRIDGE_NONEMPTY = [
    "bridge_id",
    "coarse_graining_rule",
    "readability_rule",
    "uncertainty_policy",
    "rollback_or_hold_route",
]
REQUIRED_ADMISSION_TRUE = [
    "readability_rule_present",
    "uncertainty_policy_present",
    "rollback_or_hold_route_present",
]
ALLOWED_DECISIONS = {
    "REJECT",
    "HOLD",
    "ADMIT_AS_OBSERVER_RECORD_SCALE_CANDIDATE",
    "ADMIT_AS_CONVENTIONAL_READABILITY_BRIDGE",
}
ALLOWED_ROUTES = {"HOLD", "ROLLBACK", "HOLD_OR_ROLLBACK"}
FORBIDDEN_VALUES = {
    "observer_record_opens_substance",
    "record_surface_equals_ultimate_truth",
    "scale_bridge_erases_uncertainty",
    "observation_erases_backaction",
    "readability_opens_execution_authority",
    "conventional_surface_as_absolute_world",
    "candidate_vibration_as_public_fact",
    "missing_record_surface_admitted",
}


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
    root = packet.get(REQUIRED_TOP)
    if not isinstance(root, dict):
        return False, [f"missing or invalid top-level key: {REQUIRED_TOP}"], "REJECT"

    bridge = root.get("bridge", {})
    admission = root.get("admission", {})
    if not isinstance(bridge, dict):
        errors.append("bridge must be an object")
        bridge = {}
    if not isinstance(admission, dict):
        errors.append("admission must be an object")
        admission = {}

    for key in REQUIRED_BRIDGE_NONEMPTY:
        val = bridge.get(key)
        if val is None or val == "" or val == []:
            errors.append(f"bridge.{key} must be present and non-empty")

    for key in REQUIRED_BRIDGE_TRUE:
        if bridge.get(key) is not True:
            errors.append(f"bridge.{key} must be true")

    for key in REQUIRED_ADMISSION_TRUE:
        if admission.get(key) is not True:
            errors.append(f"admission.{key} must be true")

    route = bridge.get("rollback_or_hold_route")
    if route not in ALLOWED_ROUTES:
        errors.append("bridge.rollback_or_hold_route must be HOLD/ROLLBACK/HOLD_OR_ROLLBACK")

    decision = str(admission.get("decision", "HOLD"))
    if decision not in ALLOWED_DECISIONS:
        errors.append(f"admission.decision is not allowed: {decision}")

    values = set(walk_values(root))
    for hit in sorted(values.intersection(FORBIDDEN_VALUES)):
        errors.append(f"forbidden observer-record-scale value detected: {hit}")

    if decision == "ADMIT_AS_CONVENTIONAL_READABILITY_BRIDGE" and bridge.get("record_surface_present") is not True:
        errors.append("conventional readability bridge requires record_surface_present=true")

    if errors:
        return False, errors, "HOLD" if decision != "REJECT" else "REJECT"
    return True, [], decision


def main(argv: List[str]) -> int:
    if len(argv) != 2:
        print("usage: validate_superstring_emptiness_observer_record_scale_bridge_v0_6.py packet.json", file=sys.stderr)
        return 2
    try:
        packet = json.loads(Path(argv[1]).read_text(encoding="utf-8"))
        ok, errors, decision = validate(packet)
    except Exception as exc:
        ok, errors, decision = False, [str(exc)], "REJECT"
    print(json.dumps({"ok": ok, "decision": decision, "errors": errors}, ensure_ascii=False, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
