#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
SPEC = ROOT / "specs" / "kuuos_qi_runtime_binding_os_bridge_v0_1.json"
REMOVED = [
    ROOT / "specs" / "kuuos_qi_sanjiao_os_bridge_v0_1.json",
    ROOT / "scripts" / "validate_kuuos_qi_sanjiao_os_bridge_v0_1_min.py",
    ROOT / ".github" / "workflows" / "kuuos_qi_sanjiao_validation.yml",
    ROOT / "specs" / "kuuos_qi_meridian_os_bridge_v0_1.json",
    ROOT / "scripts" / "validate_kuuos_qi_meridian_os_bridge_v0_1_min.py",
    ROOT / ".github" / "workflows" / "kuuos_qi_meridian_validation.yml",
]
FORBIDDEN_TEXT = ["qi_meridian", "Qi Meridian", "meridian", "sanjiao", "Sanjiao"]
REQUIRED_HOOKS = [
    "QI_HOOK_PRE_CYCLE",
    "QI_HOOK_POLICY_GATE",
    "QI_HOOK_LINEAGE_GATE",
    "QI_HOOK_BOUNDARY_GATE",
    "QI_HOOK_DELIVERY_GATE",
]
REQUIRED_SIGNALS = [
    "ALLOW_CANDIDATE",
    "HOLD",
    "REOBSERVE",
    "LINEAGE_RECHECK",
    "DELIVERY_RECHECK",
    "BOUNDARY_RECHECK",
    "QUARANTINE",
]
REQUIRED_RULES = [
    "QIR_boundary_first",
    "QIR_candidate_marker_required",
    "QIR_policy_flow_required",
    "QIR_lineage_flow_required",
    "QIR_delivery_flow_required",
    "QIR_all_visible",
]


def main() -> int:
    errors: list[str] = []
    for path in REMOVED:
        if path.exists():
            errors.append(f"removed Qi naming-only file still exists: {path.relative_to(ROOT)}")

    if not SPEC.is_file():
        print("ERROR: missing Qi Runtime Binding OS bridge spec")
        return 1

    text = SPEC.read_text(encoding="utf-8")
    for forbidden in FORBIDDEN_TEXT:
        if forbidden in text:
            errors.append(f"runtime binding spec still contains forbidden naming-only reference: {forbidden}")

    data = json.loads(text)

    if data.get("bridge_id") != "kuuos_qi_runtime_binding_os_bridge_v0_1":
        errors.append("bridge_id mismatch")
    if data.get("status") != "QI_RUNTIME_BINDING_OS_BRIDGE_BASELINE":
        errors.append("status mismatch")
    replaced = data.get("replaces_removed_layers", [])
    if "naming_only_channel_bridge" not in replaced:
        errors.append("must mark naming-only channel bridge as replaced")
    if "naming_only_membrane_bridge" not in replaced:
        errors.append("must mark naming-only membrane bridge as replaced")
    if data.get("attached_qi_circulation_bridge") != "kuuos_qi_circulation_os_bridge_v0_1":
        errors.append("qi circulation attachment mismatch")

    principle = data.get("runtime_binding_principle", {})
    if "operational" not in principle.get("statement", ""):
        errors.append("principle must state Qi is operational")
    if "qi_runtime_binding" not in principle.get("runtime_formula", ""):
        errors.append("runtime formula missing qi_runtime_binding")
    if "changes OS candidate flow state" not in principle.get("non_reification_rule", ""):
        errors.append("non-reification rule must bind to OS candidate flow state")

    hooks = {item.get("hook_id"): item for item in data.get("runtime_hooks", []) if isinstance(item, dict)}
    for hook_id in REQUIRED_HOOKS:
        item = hooks.get(hook_id)
        if item is None:
            errors.append(f"missing runtime hook: {hook_id}")
        elif not item.get("emits"):
            errors.append(f"runtime hook emits no signal: {hook_id}")

    outputs = {item.get("signal"): item for item in data.get("binding_outputs", []) if isinstance(item, dict)}
    for signal in REQUIRED_SIGNALS:
        if signal not in outputs:
            errors.append(f"missing Qi signal: {signal}")

    rules = {item.get("rule_id"): item for item in data.get("binding_rules", []) if isinstance(item, dict)}
    for rule_id in REQUIRED_RULES:
        item = rules.get(rule_id)
        if item is None:
            errors.append(f"missing binding rule: {rule_id}")
        elif item.get("emit") not in REQUIRED_SIGNALS:
            errors.append(f"binding rule emits invalid signal: {rule_id}")

    receipt = data.get("runtime_receipt_surface", {})
    for field in ["cycle_id", "kernel_state", "qi_binding_inputs", "qi_signal", "qi_reason", "opened_notices", "blocked_boundaries", "allowed_projection"]:
        if field not in receipt.get("required_fields", []):
            errors.append(f"missing runtime receipt field: {field}")
    for projection in ["truth_commit", "execution_commit", "memory_overwrite_commit", "completed_os_identity_commit", "world_identity_commit", "silent_pass_commit"]:
        if projection not in receipt.get("forbidden_projection", []):
            errors.append(f"missing forbidden projection: {projection}")

    invariants = data.get("required_invariants", [])
    if "qi runtime binding must not be a classification-only layer" not in invariants:
        errors.append("missing anti-classification-only invariant")
    if "boundary risk is evaluated before candidate continuation" not in invariants:
        errors.append("missing boundary-first invariant")
    if "qi runtime binding must not depend on naming-only channel layers" not in invariants:
        errors.append("missing no naming-only channel invariant")

    boundary = data.get("authority_boundary", {})
    for key in ["validation_only", "candidate_only", "runtime_binding_required", "two_truths_gap_required", "qi_circulation_required"]:
        if boundary.get(key) is not True:
            errors.append(f"boundary must be true: {key}")
    for key in ["grants_execution_authority", "grants_truth_authority", "grants_memory_overwrite_authority", "grants_governance_bypass_authority"]:
        if boundary.get(key) is not False:
            errors.append(f"boundary must be false: {key}")
    for forbidden_key in ["qi_meridian_required", "qi_sanjiao_required"]:
        if forbidden_key in boundary:
            errors.append(f"boundary must not require naming-only layer: {forbidden_key}")

    for rel in data.get("integration_points", []):
        for forbidden in ["qi_meridian", "qi_sanjiao"]:
            if forbidden in rel:
                errors.append(f"integration point must not reference naming-only layer: {rel}")
        if not isinstance(rel, str) or not (ROOT / rel).is_file():
            errors.append(f"missing integration point: {rel}")

    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1

    print("PASS: KuuOS Qi Runtime Binding OS bridge v0.1 minimal validation")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
