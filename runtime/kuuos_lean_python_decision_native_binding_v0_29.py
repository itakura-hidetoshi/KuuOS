"""DecisionOS: bind original admitted candidate to Lean ConstraintGate.

Requires the original committed DecisionOS state, its actual source
Belief-gerbe receipt, and the *supplied original* commit event (read
from its source ledger in the native fixture). The commit event and
recorded event-history digest must match. A matching local packet is
NOT proof of its external issuer or a general Lean/Python refinement.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

from typing import Any
from runtime.kuuos_lean_python_decision_mediator_source_v0_29 import (
    BLOCKED, NO_DATA, UnavailableSource, copied_state, field, truth,
    plain_list, string, natural, require_match, fail, record,
)
from runtime.kuuos_lean_python_os_path_composition_v0_6 import _finite_json
from runtime.kuuos_belief_os_gerbe_store_v0_3 import validate_gerbe_state
from runtime.kuuos_belief_os_gerbe_types_v0_3 import (
    RECEIPT_VERSION, receipt_digest,
)
from runtime.kuuos_decision_os_phase_v0_1 import (
    _constraint_reasons, _option_digest,
)
from runtime.kuuos_decision_os_types_v0_1 import event_digest
from runtime import kuuos_lean_python_decision_obligations_v0_27 as proof

OS_NAME = "DecisionOS"


def audit_native_decision_from_belief(
    belief_state: Any, belief_receipt: Any,
    decision_state: Any, commit_event: Any,
):
    """Source-typed local data obligations; commit receipt is supplied, not issued."""
    try:
        if belief_state is None or belief_receipt is None or commit_event is None:
            raise UnavailableSource("DecisionOS:original_source_packets_missing")
        for label, item in (("belief_state", belief_state),
                            ("belief_receipt", belief_receipt),
                            ("commit_event", commit_event)):
            if type(item) is not dict:
                raise UnavailableSource(label + ":exact_object_required", BLOCKED)
        belief = _finite_json(belief_state)
        receipt = _finite_json(belief_receipt)
        event = _finite_json(commit_event)
        problems = validate_gerbe_state(belief)
        if problems:
            raise UnavailableSource("DecisionOS:original_belief_gerbe_invalid", BLOCKED)
        if string(receipt, "version", "BeliefReceipt") != RECEIPT_VERSION:
            raise UnavailableSource("DecisionOS:unexpected_belief_receipt_version", BLOCKED)
        receipt_id = string(receipt, "belief_gerbe_receipt_digest", "BeliefReceipt")
        require_match(receipt_id, receipt_digest(receipt),
                      "DecisionOS:belief_receipt_digest")
        require_match(string(receipt, "route", "BeliefReceipt"),
                      "CANDIDATE", "DecisionOS:source_belief_candidate")
        require_match(string(belief, "latest_receipt_digest", "BeliefState"),
                      receipt_id, "DecisionOS:latest_belief_receipt_binding")
        decision = copied_state(OS_NAME, decision_state)
        require_match(string(decision, "source_belief_receipt_digest", OS_NAME),
                      receipt_id, "DecisionOS:source_belief_receipt_identity")
        require_match(string(decision, "lineage_id", OS_NAME),
                      string(belief, "lineage_id", "BeliefState"),
                      "DecisionOS:belief_lineage_identity")
        require_match(string(receipt, "lineage_id", "BeliefReceipt"),
                      string(belief, "lineage_id", "BeliefState"),
                      "DecisionOS:belief_receipt_lineage")
        if string(event, "target_phase", "DecisionOS.commit_event") != "commit":
            raise UnavailableSource("DecisionOS:original_commit_event_required", BLOCKED)
        event_id = string(event, "decision_event_digest", "DecisionOS.commit_event")
        require_match(event_id, event_digest(event),
                      "DecisionOS:commit_event_digest")
        require_match(string(event, "decision_id", "DecisionOS.commit_event"),
                      string(decision, "decision_id", OS_NAME),
                      "DecisionOS:commit_event_decision_identity")
        history = plain_list(decision, "event_history", OS_NAME)
        if not history:
            raise UnavailableSource("DecisionOS:committed_event_history_missing")
        last = field(history[-1], "decision_event_digest", "DecisionOS.event_history")
        require_match(last, event_id, "DecisionOS:recorded_commit_event")
        require_match(natural(event, "event_index", "DecisionOS.commit_event"),
                      natural(decision, "event_index", "DecisionOS"),
                      "DecisionOS:commit_event_index")
        require_match(natural(event, "created_at_ms", "DecisionOS.commit_event"),
                      natural(history[-1], "created_at_ms", "DecisionOS.event_history"),
                      "DecisionOS:commit_event_time")
        payload = field(event, "payload", "DecisionOS.commit_event")
        if type(payload) is not dict:
            raise UnavailableSource("DecisionOS:commit_payload_object_required", BLOCKED)
        require_match(string(payload, "activation_boundary", "DecisionOS.commit"),
                      "mission_replan_only", "DecisionOS:commit_activation_boundary")
        require_match(truth(payload, "future_only", "DecisionOS.commit"),
                      True, "DecisionOS:commit_future_only")
        require_match(truth(payload, "memory_overwrite", "DecisionOS.commit"),
                      False, "DecisionOS:commit_no_memory_overwrite")
        require_match(truth(payload, "decision_not_execution", "DecisionOS.commit"),
                      True, "DecisionOS:commit_not_execution")
        selected = string(decision, "selected_option_id", "DecisionOS",
                          empty_allowed=True)
        if (string(decision, "route", "DecisionOS") != "SELECT_CANDIDATE"
                or not selected):
            raise UnavailableSource("DecisionOS:no_selected_admissible_candidate")
        admitted = plain_list(decision, "admissible_option_ids", "DecisionOS")
        if selected not in admitted:
            raise UnavailableSource("DecisionOS:selected_candidate_not_admitted", BLOCKED)
        options = plain_list(decision, "options", "DecisionOS")
        matches = [x for x in options
                   if type(x) is dict and x.get("option_id") == selected]
        if len(matches) != 1:
            raise UnavailableSource("DecisionOS:selected_source_option_not_unique", BLOCKED)
        option = matches[0]
        require_match(string(option, "option_digest", "DecisionOS.option"),
                      _option_digest(option), "DecisionOS:option_digest")
        if _constraint_reasons(decision, option):
            raise UnavailableSource("DecisionOS:original_option_not_admissible",
                                    BLOCKED)
        threshold = field(decision, "thresholds", OS_NAME)
        required = plain_list(option, "required_evidence_digests", "DecisionOS.option")
        available = plain_list(option, "available_evidence_digests", "DecisionOS.option")
        witness = {
            "missionAllowed": truth(option, "mission_allowed", "DecisionOS.option"),
            "prohibited": truth(option, "prohibited", "DecisionOS.option"),
            "authorityClaimed": truth(option, "authority_claimed", "DecisionOS.option"),
            "withinBudget": option["estimated_cost"] <= decision["decision_budget"],
            "withinRisk": option["estimated_risk"] <= threshold["maximum_risk"],
            "recoverable": option["recoverability"] >= threshold["minimum_recoverability"],
            "reversible": option["reversibility"] >= threshold["minimum_reversibility"],
            # Existence of required, separately present source evidence is
            # distinct from vacuous satisfaction of an empty requirements set.
            "evidencePresent": bool(required) and set(required).issubset(set(available)),
            "futureOnly": truth(payload, "future_only", "DecisionOS.commit"),
            "memoryOverwrite": truth(payload, "memory_overwrite", "DecisionOS.commit"),
            "decisionNotExecution": truth(payload, "decision_not_execution",
                                          "DecisionOS.commit"),
        }
        result = proof.audit_witness(witness)
        if result.status == BLOCKED:
            raise UnavailableSource("DecisionOS:source_bound_constraint_gate_failed",
                                    BLOCKED)
        if result.status != "LOCAL_CONDITIONS_CHECKED":
            raise UnavailableSource("DecisionOS:source_bound_evidence_unavailable")
        paths = [
            "BeliefOSState.latest_receipt_digest",
            "BeliefOSReceipt.belief_gerbe_receipt_digest",
            "DecisionOS.source_belief_receipt_digest",
            "DecisionOS.lineage_id",
            "DecisionOS.options[option_id=" + selected + "]",
            "DecisionOS.admissible_option_ids",
            "DecisionOS.thresholds",
            "DecisionOS.event_history[-1].decision_event_digest",
            "DecisionOS.commit_event.payload",
        ]
        return record(OS_NAME, decision, paths, 1, edge=False,
                      issues=("BeliefGerbeV03_to_BeliefOSV01_formal_refinement_unproved",))
    except UnavailableSource as exc:
        return fail(OS_NAME, exc.reason, status=exc.status)
    except (KeyError, TypeError, ValueError, UnicodeError, OverflowError,
            RecursionError, AttributeError) as exc:
        return fail(OS_NAME, "DecisionOS:original_source_exception:" +
                    type(exc).__name__, status=BLOCKED)


__all__ = ("OS_NAME", "audit_native_decision_from_belief")
