#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION = "kuuos_planos_compiler_materialization_v0_22"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def require_tokens(path: Path, tokens: tuple[str, ...]) -> None:
    text = path.read_text(encoding="utf-8")
    for token in tokens:
        require(token in text, f"{path}: missing {token}")


def main() -> int:
    formal_root = ROOT / "formal/KuuOSPlanOSV0_22.lean"
    aggregate_root = ROOT / "formal/KuuOSFormal.lean"
    formal = ROOT / "formal/KUOS/PlanOS/VacuumExpectationCompilerMaterializationV0_22.lean"
    source = ROOT / "formal/KUOS/PlanOS/VacuumExpectationSelectedCandidateNextCycleSynthesisV0_21.lean"
    adapter = ROOT / "formal/KUOS/PlanOS/NextCycleBasisCompilerAdapterV0_3.lean"
    docs = ROOT / "docs/KUUOS_PLANOS_COMPILER_MATERIALIZATION_v0_22.md"
    manifest_path = ROOT / "manifests/kuuos_planos_compiler_materialization_v0_22.json"
    workflow = ROOT / ".github/workflows/planos-compiler-materialization-v0-22.yml"

    for path in (
        formal_root,
        aggregate_root,
        formal,
        source,
        adapter,
        docs,
        manifest_path,
        workflow,
    ):
        require(path.is_file(), f"missing file: {path}")

    import_token = "KUOS.PlanOS.VacuumExpectationCompilerMaterializationV0_22"
    require_tokens(formal_root, (import_token,))
    require_tokens(aggregate_root, (import_token,))
    require_tokens(
        formal,
        (
            "compilerRouteOfCandidate",
            "VacuumExpectationCompilerMaterializationBridge",
            "VacuumExpectationCompilerMaterializationReceipt",
            "materialization_requires_committed_next_plan_basis",
            "compiler_route_is_exact_and_projected",
            "hold_selection_projects_to_hold",
            "termination_selection_projects_to_handover",
            "exact_next_cycle_gate_matches_synthesis",
            "exact_next_cycle_gate_uses_source_active_cycle",
            "compiler_reuses_v01_and_all_guards",
            "materialization_preserves_templates_identity_and_recovery",
            "hold_materializes_zero_executable_steps",
            "materialization_preserves_dual_lineage_and_digest_bindings",
            "materialization_is_single_use_and_replay_safe",
            "materialization_events_append_strictly",
            "materialization_history_appends_two_records",
            "materialization_bridge_preserves_ownership",
            "materialization_bridge_grants_no_activation_or_execution",
            "materialization_digest_is_exact",
        ),
    )
    require_tokens(
        source,
        (
            "VacuumExpectationSelectedCandidateNextCycleSynthesisReceipt",
            "synthesis_commit_requires_next_plan_phase",
            "synthesis_commit_does_not_activate_execute_or_license",
        ),
    )
    require_tokens(
        adapter,
        (
            "ReplanAdapterRoute",
            "ExactNextCycleGate",
            "MaterializationBoundary",
            "HoldMaterializationBoundary",
            "CompilerReuseBoundary",
            "SingleUseBoundary",
            "AdapterNonAuthority",
        ),
    )
    require_tokens(
        docs,
        (
            "route projectionは候補identityの置換ではない",
            "executable step count = 0",
            "exact replay idempotent = true",
            "materialization != plan activation",
        ),
    )
    require_tokens(
        ROOT / "scripts/run_kuuos_runtime_full_check_v0_51.py",
        ("check_planos_v022",),
    )

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    require(manifest["version"] == VERSION, "manifest version mismatch")
    require(manifest["formal_module"] == str(formal.relative_to(ROOT)), "formal module mismatch")
    require(manifest["documentation"] == str(docs.relative_to(ROOT)), "documentation mismatch")
    require(manifest["workflow"] == str(workflow.relative_to(ROOT)), "workflow mismatch")
    for field, value in manifest["required"].items():
        require(value is True, f"required boundary missing: {field}")
    for field, value in manifest["forbidden"].items():
        require(value is False, f"forbidden promotion: {field}")

    print("PlanOS compiler materialization v0.22 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
