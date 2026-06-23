#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION = "kuuos_decisionos_admissible_candidate_selection_v0_4"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def require_tokens(path: Path, tokens: tuple[str, ...]) -> None:
    text = path.read_text(encoding="utf-8")
    for token in tokens:
        require(token in text, f"{path}: missing {token}")


def main() -> int:
    formal_root = ROOT / "formal/KuuOSDecisionOSV0_4.lean"
    aggregate_root = ROOT / "formal/KuuOSFormal.lean"
    formal = ROOT / "formal/KUOS/DecisionOS/VacuumExpectationAdmissibleCandidateSelectionV0_4.lean"
    source = ROOT / "formal/KUOS/PlanOS/VacuumExpectationHysteresisConstraintDecisionHandoffV0_20.lean"
    docs = ROOT / "docs/KUUOS_DECISIONOS_ADMISSIBLE_CANDIDATE_SELECTION_v0_4.md"
    manifest_path = ROOT / "manifests/kuuos_decisionos_admissible_candidate_selection_v0_4.json"
    workflow = ROOT / ".github/workflows/decisionos-admissible-candidate-selection-v0-4.yml"

    for path in (formal_root, aggregate_root, formal, source, docs, manifest_path, workflow):
        require(path.is_file(), f"missing file: {path}")

    import_token = "KUOS.DecisionOS.VacuumExpectationAdmissibleCandidateSelectionV0_4"
    require_tokens(formal_root, (import_token,))
    require_tokens(
        formal,
        (
            "VacuumExpectationAdmissibleCandidateSelectionBridge",
            "VacuumExpectationAdmissibleCandidateSelectionReceipt",
            "selection_requires_unselected_decisionos_handoff",
            "selected_candidate_is_from_admissible_set",
            "selection_preserves_admissibility_identity_and_alternatives",
            "selected_constraint_is_admissible_and_non_authoritative",
            "robust_certificate_separates_every_alternative",
            "wa_gate_preserves_dissent_minority_and_identity",
            "wa_plurality_forbids_silent_substitution",
            "selection_preserves_two_truths_and_middle_way",
            "selection_is_not_truth_execution_or_license",
            "selection_event_and_history_append_once",
            "selection_bridge_grants_no_downstream_authority",
            "selection_digest_is_exact",
        ),
    )
    require_tokens(
        source,
        (
            "DecisionOSAdmissibleSetHandoff",
            "handoff_is_not_selection_or_synthesis",
            "handoff_preserves_admissible_set",
        ),
    )
    require_tokens(
        docs,
        (
            "selected candidateは次のいずれか",
            "DecisionOS selection != plan synthesis",
            "false harmony",
            "Two Truths",
        ),
    )
    require_tokens(
        ROOT / "scripts/run_kuuos_runtime_full_check_v0_51.py",
        ("check_decisionos_v04",),
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

    print("DecisionOS admissible candidate selection v0.4 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
