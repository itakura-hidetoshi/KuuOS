"""KuuOS Lean→Python v0.30 — real original CodeAI selection boundary.

Checks EXACT original Python CodeAI's sealed plan, independent-test evidence,
selection request/policy, deterministic output decision and bounded receipt.
Only selected candidate scorecards are projected into the existing v0.27
CodeAI Lean-derived data checker; ineligible scorecards are independently
audited without turning nonselection into an abstention decision.

No test is executed, no repair or Git effect is requested, no original
CodeAI kernel modified. Original source authenticity and complete
Lean↔Python refinement are NOT established by local hashes or replay.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from runtime.kuuos_lean_python_os_path_composition_v0_6 import (
    _finite_json, _fingerprint,
)
from runtime.kuuos_lean_python_codeai_obligations_v0_27 import (
    audit_witness as audit_lean_condition_data,
)
from runtime.kuuos_lean_python_contract_bridge_v0_1 import (
    codeai_selection_boundary_check,
    PASSED as ORIGINAL_PASSED,
)
from runtime.kuuos_codeai_evidence_weighted_selection_abstention_v0_1 import (
    build_codeai_evidence_weighted_selection_abstention as native_select,
)
from runtime.kuuos_codeai_evidence_weighted_selection_abstention_schema_v0_1 import (
    DECISION_SELECTED, DECISION_ABSTAINED, STATUS_READY,
    DECISION_DIGEST_FIELD, RECEIPT_DIGEST_FIELD, digest_ok,
)
from runtime.kuuos_codeai_candidate_static_admissibility_preflight_schema_v0_1 import (
    DISPOSITION_ADMISSIBLE, DISPOSITION_REPAIRABLE,
    DISPOSITION_HOLD, DISPOSITION_REJECTED,
)

VERSION = "kuuos_lean_python_native_codeai_selection_v0_30"
SOURCE_MAIN = "52691b7a98a289dc154950dfef097bef7ecb4fb4"
PASS = "SOURCE_BOUND_LOCAL_CHECKED"
NO_DATA = "NO_DATA"
BLOCKED = "BLOCKED"
SOURCE_CLASS_MAP = {
    DISPOSITION_ADMISSIBLE: "admissible",
    DISPOSITION_REPAIRABLE: "repairable",
    DISPOSITION_HOLD: "hold",
    DISPOSITION_REJECTED: "rejected",
}

EXPECTED_NON_AUTHORITY = {
    "test_execution_performed_by_kernel": False,
    "repair_executed": False,
    "repository_mutation_performed": False,
    "git_effect_performed": False,
    "verification_authority_granted": False,
    "repair_authority_granted": False,
    "execution_authority_granted": False,
    "git_authority_granted": False,
    "score_treated_as_probability": False,
    "score_treated_as_correctness_proof": False,
    "selection_treated_as_correctness_proof": False,
    "abstention_treated_as_rejection": False,
}


@dataclass(frozen=True)
class CodeAINativeSelectionAudit:
    status: str
    issues: tuple[str, ...] = ()
    source_digest: str | None = None
    selection_case: str | None = None
    source_scorecards_checked: int = 0
    selected_lean_condition_checked: bool = False
    original_selection_replayed: bool = False
    original_output_digest_checked: bool = False
    original_source_modified: bool = False
    source_issuer_authenticated: bool = False
    original_independent_runner_attested_by_model: bool = False
    formal_lean_python_refinement_proved: bool = False
    lean_proof_term_constructed: bool = False
    truth_authority_granted: bool = False
    execution_authority_granted: bool = False
    repair_authority_granted: bool = False
    git_authority_granted: bool = False


def _hold(status: str, problem: str) -> CodeAINativeSelectionAudit:
    return CodeAINativeSelectionAudit(status=status, issues=(problem,))


def _strict_nat(value: Any, label: str) -> int:
    if type(value) is not int or value < 0:
        raise ValueError(label + ":natural_required")
    return value


def _packet(input_value: Any, label: str) -> dict:
    if input_value is None:
        raise KeyError(label + ":missing")
    if type(input_value) is not dict:
        raise ValueError(label + ":plain_object_required")
    value = _finite_json(input_value)
    if type(value) is not dict:
        raise ValueError(label + ":exact_plain_object_required")
    return value


def audit_native_codeai_selection(
    source_inputs: Any,
    recorded_decision: Any,
    recorded_receipt: Any,
) -> CodeAINativeSelectionAudit:
    """Verify an ORIGINAL original-kernel result and its selected Lean data.

    Missing independently supplied original output is NO_DATA; a locally
    self-consistent sealed record is still not evidence of a real issuer.
    """
    if any(value is None for value in (
        source_inputs, recorded_decision, recorded_receipt,
    )):
        return _hold(NO_DATA, "original_codeai_source_or_output_missing")
    try:
        sources = _packet(source_inputs, "CodeAI.inputs")
        expected_keys = {
            "strengthening_plan", "strengthening_receipt", "evidence_packet",
            "selection_request", "selection_policy",
        }
        if set(sources) != expected_keys:
            raise ValueError("CodeAI:exact_five_source_packets_required")
        inputs = {key: _packet(sources[key], "CodeAI." + key)
                  for key in expected_keys}
        decision = _packet(recorded_decision, "CodeAI.decision")
        receipt = _packet(recorded_receipt, "CodeAI.receipt")
        source_fingerprint = _fingerprint([sources, decision, receipt])
        native = native_select(**inputs)
        if native.status != STATUS_READY or native.decision is None or native.receipt is None:
            return _hold(BLOCKED, "CodeAI:original_source_validator_failed:" +
                         ";".join(native.issues))
        if not digest_ok(decision, DECISION_DIGEST_FIELD):
            raise ValueError("CodeAI:original_decision_digest_invalid")
        if not digest_ok(receipt, RECEIPT_DIGEST_FIELD):
            raise ValueError("CodeAI:original_receipt_digest_invalid")
        if native.decision != decision or native.receipt != receipt:
            raise ValueError("CodeAI:actual_original_selector_replay_mismatch")
        original_boundary = codeai_selection_boundary_check(receipt)
        if original_boundary.status != ORIGINAL_PASSED:
            raise ValueError("CodeAI:original_receipt_authority_boundary_failed")
        for key, required in EXPECTED_NON_AUTHORITY.items():
            if type(decision.get(key)) is not bool or decision[key] is not required:
                raise ValueError("CodeAI:decision_boundary:" + key)
            if type(receipt.get(key)) is not bool or receipt[key] is not required:
                raise ValueError("CodeAI:receipt_boundary:" + key)
        if decision.get("external_test_execution_evidence_consumed") is not True:
            raise ValueError("CodeAI:external_evidence_not_consumed")
        if decision.get("ranking_performed") is not True:
            raise ValueError("CodeAI:ranking_not_recorded")
        if decision.get("selection_decision_recorded") is not True:
            raise ValueError("CodeAI:decision_not_recorded")
        if decision.get("selection_authority_bounded_to_decision") is not True:
            raise ValueError("CodeAI:selection_authority_unbounded")
        cards = decision.get("candidate_scorecards")
        plans = sources["strengthening_plan"].get("candidate_plans")
        if type(cards) is not list or type(plans) is not list:
            raise ValueError("CodeAI:original_candidate_inventory_missing")
        if len(cards) != _strict_nat(decision.get("candidate_count"),
                                     "CodeAI.candidate_count"):
            raise ValueError("CodeAI:source_card_count_mismatch")
        if len(cards) != len(plans):
            raise ValueError("CodeAI:source_plan_count_mismatch")
        plan_by_id = {p["candidate_id"]: p for p in plans}
        if len(plan_by_id) != len(plans):
            raise ValueError("CodeAI:duplicate_plan_candidate")
        selected_id = decision.get("selected_candidate_id")
        value = decision.get("decision")
        if value not in (DECISION_SELECTED, DECISION_ABSTAINED):
            raise ValueError("CodeAI:original_selection_case_invalid")
        selected_count = 0
        selected_checked = False
        for card in cards:
            ident = card.get("candidate_id")
            if type(ident) is not str or ident not in plan_by_id:
                raise ValueError("CodeAI:scorecard_not_source_candidate")
            original_class = card.get("source_classification")
            if original_class not in SOURCE_CLASS_MAP:
                raise ValueError("CodeAI:source_classification_not_mapped")
            if original_class != plan_by_id[ident]["source_classification"]:
                raise ValueError("CodeAI:original_classification_not_bound")
            maximum = _strict_nat(card.get("maximum_evidence_score"),
                                  "CodeAI.maximum_evidence_score")
            score = _strict_nat(card.get("evidence_score"), "CodeAI.evidence_score")
            obligations = _strict_nat(card.get("obligation_count"),
                                      "CodeAI.obligation_count")
            passed = _strict_nat(card.get("passed_count"), "CodeAI.passed_count")
            failed = _strict_nat(card.get("failed_count"), "CodeAI.failed_count")
            inconclusive = _strict_nat(card.get("inconclusive_count"),
                                       "CodeAI.inconclusive_count")
            skipped = _strict_nat(card.get("skipped_count"), "CodeAI.skipped_count")
            if passed + failed + inconclusive + skipped != obligations:
                raise ValueError("CodeAI:obligation_outcomes_not_exhaustive")
            if score > maximum:
                raise ValueError("CodeAI:evidence_score_over_maximum")
            evidence_status = (
                "allPassed" if passed == obligations and
                failed == inconclusive == skipped == 0 else
                "hasFailure" if failed > 0 else "incomplete"
            )
            admissible = SOURCE_CLASS_MAP[original_class] == "admissible"
            should_be_eligible = admissible and evidence_status == "allPassed"
            if type(card.get("eligible")) is not bool or card["eligible"] != should_be_eligible:
                raise ValueError("CodeAI:score_does_not_override_eligibility")
            is_selected = card.get("candidate_selected")
            if type(is_selected) is not bool:
                raise ValueError("CodeAI:source_selection_bool_required")
            if is_selected:
                selected_count += 1
                if value != DECISION_SELECTED or ident != selected_id:
                    raise ValueError("CodeAI:selected_scorecard_source_mismatch")
                verdict = audit_lean_condition_data({
                    "candidateId": ident,
                    "sourceClassification": SOURCE_CLASS_MAP[original_class],
                    "evidenceStatus": evidence_status,
                    "evidenceScore": score,
                    "maximumEvidenceScore": maximum,
                    "decision": "selected",
                    "scoreTreatedAsProbability": decision["score_treated_as_probability"],
                    "scoreTreatedAsCorrectnessProof": decision["score_treated_as_correctness_proof"],
                    "selectionTreatedAsCorrectnessProof": decision["selection_treated_as_correctness_proof"],
                    "abstentionTreatedAsRejection": decision["abstention_treated_as_rejection"],
                })
                if verdict.status != "LOCAL_CONDITIONS_CHECKED":
                    raise ValueError("CodeAI:Lean_selected_candidate_data_conditions_failed")
                selected_checked = True
        if value == DECISION_SELECTED and (selected_count != 1 or not selected_checked):
            raise ValueError("CodeAI:selected_candidate_not_uniquely_evidenced")
        if value == DECISION_ABSTAINED and (selected_count != 0 or selected_id != ""):
            raise ValueError("CodeAI:abstention_not_preserved")
        if _fingerprint([sources, decision, receipt]) != source_fingerprint:
            raise ValueError("CodeAI:source_mutated")
        return CodeAINativeSelectionAudit(
            status=PASS, source_digest=source_fingerprint,
            selection_case=value, source_scorecards_checked=len(cards),
            selected_lean_condition_checked=selected_checked,
            original_selection_replayed=True,
            original_output_digest_checked=True,
        )
    except KeyError as exc:
        return _hold(NO_DATA, "CodeAI:required_source_missing:" + str(exc))
    except (TypeError, ValueError, OverflowError, UnicodeError,
            RecursionError, AttributeError) as exc:
        return _hold(BLOCKED, "CodeAI:source_binding_exception:" +
                     type(exc).__name__ + ":" + str(exc)[:300])


__all__ = (
    "VERSION", "SOURCE_MAIN", "PASS", "NO_DATA", "BLOCKED",
    "CodeAINativeSelectionAudit", "audit_native_codeai_selection",
)
