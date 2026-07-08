#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION = "kuuos_planos_qi_blocker_foresight_plan_gate_v0_24"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def require_tokens(path: Path, tokens: tuple[str, ...]) -> None:
    text = path.read_text(encoding="utf-8")
    for token in tokens:
        require(token in text, f"{path}: missing {token}")


def main() -> int:
    formal_root = ROOT / "formal/KuuOSPlanOSV0_24.lean"
    aggregate_root = ROOT / "formal/KuuOSFormal.lean"
    formal = ROOT / "formal/KUOS/PlanOS/VacuumExpectationQiBlockerForesightPlanGateV0_24.lean"
    source = ROOT / "formal/KUOS/PlanOS/VacuumExpectationActivationAdmissionActOSHandoffV0_23.lean"
    qi_runtime = ROOT / "runtime/qi_process_tensor_v0_1.py"
    docs = ROOT / "docs/KUUOS_PLANOS_QI_BLOCKER_FORESIGHT_PLAN_GATE_v0_24.md"
    manifest_path = ROOT / "manifests/kuuos_planos_qi_blocker_foresight_plan_gate_v0_24.json"
    workflow = ROOT / ".github/workflows/plan-os-validation.yml"

    for path in (formal_root, aggregate_root, formal, source, qi_runtime, docs, manifest_path, workflow):
        require(path.is_file(), f"missing file: {path}")

    import_token = "KUOS.PlanOS.VacuumExpectationQiBlockerForesightPlanGateV0_24"
    require_tokens(formal_root, (import_token,))
    require_tokens(aggregate_root, (import_token,))
    require_tokens(
        formal,
        (
            "QiProcessTensorForesightEvidence",
            "PlanOSBlockerTheoryBoundary",
            "AgentTheorySelectionBinding",
            "QiBlockerForesightPlanGateBoundary",
            "VacuumExpectationQiBlockerForesightPlanGateBridge",
            "VacuumExpectationQiBlockerForesightPlanGateReceipt",
            "source_handoff_remains_non_authoritative",
            "requires_qi_process_tensor_foresight",
            "requires_causal_reward_and_verifier_trace",
            "requires_blocker_classification_without_release",
            "requires_agent_theory_selection_binding",
            "gate_filters_to_replan_without_authority",
            "bridge_grants_no_execution_truth_memory_or_blocker_release",
            "events_append_strictly",
            "history_appends_three_records",
            "digest_is_exact",
        ),
    )
    require_tokens(
        source,
        (
            "VacuumExpectationActivationAdmissionActOSHandoffReceipt",
            "handoff_is_not_activation_authorization_or_execution",
            "bridge_grants_no_activation_execution_or_commit",
        ),
    )
    require_tokens(
        qi_runtime,
        (
            "process_tensor_visible",
            "transition_continuity_visible",
            "memory_continuity_visible",
            "nonmarkov_memory_visible",
            "grants_execution_authority",
        ),
    )
    require_tokens(
        docs,
        (
            "WorldEvolver / self-evolving world model",
            "Agent Process Reward Model",
            "test-time scaling for agents",
            "agent memory governance",
            "graph-based agent memory",
            "causal world model",
            "blocker release granted = false",
            "candidate weights advisory only = true",
            "replan signal only = true",
        ),
    )
    require_tokens(
        ROOT / "scripts/run_kuuos_runtime_full_check_v0_51.py",
        ("check_planos_v024",),
    )
    require_tokens(
        ROOT / "scripts/run_plan_os_full_checks.py",
        ("check_planos_qi_blocker_foresight_plan_gate_v0_24.py", "v0.1-v0.24"),
    )

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    require(manifest["version"] == VERSION, "manifest version mismatch")
    require(manifest["formal_module"] == str(formal.relative_to(ROOT)), "formal module mismatch")
    require(manifest["documentation"] == str(docs.relative_to(ROOT)), "documentation mismatch")
    require(manifest["workflow"] == str(workflow.relative_to(ROOT)), "workflow mismatch")
    require(manifest["source_version"] == "kuuos_planos_activation_admission_actos_handoff_v0_23", "source version mismatch")
    require(manifest["upstream_runtime"] == "runtime/qi_process_tensor_v0_1.py", "upstream runtime mismatch")
    require(manifest["history_delta"] == 3, "history delta mismatch")
    for field, value in manifest["literature_mapping"].items():
        require(value is True, f"literature mapping missing: {field}")
    for field, value in manifest["required"].items():
        require(value is True, f"required boundary missing: {field}")
    for field, value in manifest["closed"].items():
        require(value is False, f"closed boundary promoted: {field}")

    print("PlanOS Qi blocker foresight plan gate v0.24 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
