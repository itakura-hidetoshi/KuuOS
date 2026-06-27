#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION = "kuuos_planos_selected_candidate_next_cycle_synthesis_v0_21"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def require_tokens(path: Path, tokens: tuple[str, ...]) -> None:
    text = path.read_text(encoding="utf-8")
    for token in tokens:
        require(token in text, f"{path}: missing {token}")


def main() -> int:
    formal_root = ROOT / "formal/KuuOSPlanOSV0_21.lean"
    aggregate_root = ROOT / "formal/KuuOSFormal.lean"
    formal = ROOT / "formal/KUOS/PlanOS/VacuumExpectationSelectedCandidateNextCycleSynthesisV0_21.lean"
    source = ROOT / "formal/KUOS/DecisionOS/VacuumExpectationAdmissibleCandidateSelectionV0_4.lean"
    docs = ROOT / "docs/KUUOS_PLANOS_SELECTED_CANDIDATE_NEXT_CYCLE_SYNTHESIS_v0_21.md"
    manifest_path = ROOT / "manifests/kuuos_planos_selected_candidate_next_cycle_synthesis_v0_21.json"
    workflow = ROOT / ".github/workflows/plan-os-validation.yml"

    for path in (formal_root, aggregate_root, formal, source, docs, manifest_path, workflow):
        require(path.is_file(), f"missing file: {path}")

    import_token = "KUOS.PlanOS.VacuumExpectationSelectedCandidateNextCycleSynthesisV0_21"
    require_tokens(formal_root, (import_token,))
    require_tokens(aggregate_root, (import_token,))
    require_tokens(
        formal,
        (
            "VacuumExpectationSelectedCandidateNextCycleSynthesisBridge",
            "VacuumExpectationSelectedCandidateNextCycleSynthesisReceipt",
            "synthesis_requires_exact_decision_selection",
            "synthesis_binds_history_qi_learning_and_mission",
            "synthesis_starts_exactly_next_cycle",
            "synthesis_is_future_only_and_inactive",
            "synthesis_commit_requires_next_plan_phase",
            "synthesis_commit_does_not_activate_execute_or_license",
            "synthesis_events_append_strictly",
            "synthesis_history_appends_two_records",
            "synthesis_bridge_preserves_ownership",
            "synthesis_bridge_grants_no_downstream_authority",
            "synthesis_digest_is_exact",
        ),
    )
    require_tokens(
        source,
        (
            "VacuumExpectationAdmissibleCandidateSelectionReceipt",
            "selected_candidate_is_from_admissible_set",
            "selection_is_not_truth_execution_or_license",
        ),
    )
    require_tokens(
        docs,
        (
            "activeFromCycle = currentCycle + 1",
            "basis commitはplan activationではない",
            "candidate selection owner = DecisionOS",
            "plan synthesis owner = PlanOS",
        ),
    )
    require_tokens(
        ROOT / "scripts/run_kuuos_runtime_full_check_v0_51.py",
        ("check_planos_v021",),
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

    print("PlanOS selected candidate next-cycle synthesis v0.21 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
