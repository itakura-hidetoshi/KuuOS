#!/usr/bin/env python3
"""
Validator for Superstring Emptiness String / Brane / Membrane Runtime v0.2.

v0.2 extends v0.1 with explicit rejection of:
- brane-as-absolute-world collapse,
- membrane-as-final-authority collapse,
- gluing obstruction erasure,
- direct execution authority claims.

Only the Python standard library is used.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

REQUIRED_TOP = ["string_brane_membrane_packet"]
REQUIRED_STRING_TRUE = ["non_reification_guard", "two_truths_gap_guard"]
REQUIRED_MEMBRANE_TRUE = ["authority_non_expansion_guard"]
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
    "direct_execution_authority",
    "graph_only_indranet",
    "obstruction_erasure",
    "silent_strong_upgrade",
}
ALLOWED_WORLD_SCOPES = {
    "conventional_effective_surface",
    "local_effective_world_surface",
    "effective_world_surface_candidate",
}
ALLOWED_ROLLBACK_OR_HOLD = {"HOLD", "ROLLBACK", "HOLD_OR_ROLLBACK"}


def load_packet(path: Path) -> Dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".json":
        return json.loads(text)
    raise ValueError("Only JSON packet validation is supported by this validator.")


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


def require_nonempty(obj: Dict[str, Any], key: str, scope: str, errors: List[str]) -> None:
    val = obj.get(key)
    if val is None or val == "" or val == []:
        errors.append(f"{scope}.{key} must be present and non-empty")


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

    for key in ["string_id", "source_conditions", "target_surface", "vibration_mode", "boundary_conditions", "observer_record_surface", "consistency_witnesses"]:
        require_nonempty(string, key, "string", errors)

    for key in ["brane_id", "world_scope", "supporting_conditions", "admissible_string_ids", "record_surface", "scale_regime", "qi_flow_interface", "indra_gauge_interface", "governance_boundary"]:
        require_nonempty(brane, key, "brane", errors)

    for key in ["membrane_id", "from_layer", "to_layer", "permeability_rule", "obstruction_visibility_rule", "gluing_rule", "backaction_budget", "rollback_or_hold_route"]:
        require_nonempty(membrane, key, "membrane", errors)

    for key in REQUIRED_STRING_TRUE:
        if string.get(key) is not True:
            errors.append(f"string.{key} must be true")

    for key in REQUIRED_MEMBRANE_TRUE:
        if membrane.get(key) is not True:
            errors.append(f"membrane.{key} must be true")

    for key in REQUIRED_ADMISSION_TRUE:
        if admission.get(key) is not True:
            errors.append(f"admission.{key} must be true")

    if brane.get("world_scope") not in ALLOWED_WORLD_SCOPES:
        errors.append("brane.world_scope must remain a conventional/local/candidate effective surface")

    if membrane.get("rollback_or_hold_route") not in ALLOWED_ROLLBACK_OR_HOLD:
        errors.append("membrane.rollback_or_hold_route must be HOLD/ROLLBACK/HOLD_OR_ROLLBACK")

    decision = str(admission.get("decision", "HOLD"))
    if decision not in ALLOWED_DECISIONS:
        errors.append(f"admission.decision is not allowed: {decision}")

    values = set(walk_values(root))
    forbidden_hits = sorted(values.intersection(FORBIDDEN_VALUES))
    for hit in forbidden_hits:
        errors.append(f"forbidden runtime value detected: {hit}")

    if decision == "ADMIT_AS_CONVENTIONAL_RUNTIME_SURFACE":
        if brane.get("world_scope") not in {"conventional_effective_surface", "local_effective_world_surface"}:
            errors.append("conventional admission requires conventional/local effective world surface")

    if errors:
        return False, errors, "HOLD" if decision != "REJECT" else "REJECT"

    return True, [], decision


def main(argv: List[str]) -> int:
    if len(argv) != 2:
        print("usage: validate_superstring_emptiness_string_brane_membrane_v0_2.py packet.json", file=sys.stderr)
        return 2
    try:
        packet = load_packet(Path(argv[1]))
        ok, errors, decision = validate(packet)
    except Exception as exc:
        print(json.dumps({"ok": False, "decision": "REJECT", "errors": [str(exc)]}, ensure_ascii=False, indent=2))
        return 1
    print(json.dumps({"ok": ok, "decision": decision, "errors": errors}, ensure_ascii=False, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
