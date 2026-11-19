"""DecisionOSPlural: source-bound native consensus boundary, not a raw veto.

The native fixture's consensus route normally has NO validated veto.
Rather than constructing a fictitious ValidatedProtectiveVeto instance
to satisfy v0.27's different witness, check Lean's actual
BroadAcceptabilityBoundary.eligible premise and consensus consequences
against the original source's selected aggregate and ordered records.

Any near-threshold source float is compared at its exact finite rational
value; the original Python tolerance is NOT promoted to Lean ≤.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations
from typing import Any

from runtime.kuuos_lean_python_decision_mediator_source_v0_29 import (
    BLOCKED, UnavailableSource, copied_state, copied_edge, mediator_state,
    field, truth, string, plain_list, require_match, fail, record,
    rational_float,
)
from runtime.kuuos_decision_os_plural_kernel_v0_2 import _adjudicate

OS_NAME = "DecisionOSPlural"
LEAN_THEOREMS = (
    "consensusCertificate_has_no_validated_veto",
    "consensusCertificate_meets_support_floor",
    "consensusCertificate_meets_opposition_ceiling",
    "consensusCertificate_meets_worst_case_floor",
    "consensusCertificate_is_not_truth",
)


def audit_native_plural_consensus(decision_state: Any, plural_state: Any):
    try:
        decision = copied_state("DecisionOS", decision_state)
        plural = mediator_state(OS_NAME, plural_state)
        copied_edge("DecisionOS", OS_NAME, decision, plural)
        if string(plural, "route", OS_NAME) != "CONSENSUS_CANDIDATE":
            raise UnavailableSource("DecisionOSPlural:no_native_consensus_certificate")
        selected = string(plural, "selected_option_id", OS_NAME)
        ids = plain_list(plural, "source_option_ids", OS_NAME)
        if selected not in ids:
            raise UnavailableSource("DecisionOSPlural:source_option_missing",
                                    BLOCKED)
        records = plain_list(plural, "aggregate_records", OS_NAME)
        matches = [record for record in records
                   if type(record) is dict and record.get("option_id") == selected]
        if len(matches) != 1:
            raise UnavailableSource("DecisionOSPlural:selected_aggregate_missing",
                                    BLOCKED)
        aggregate = matches[0]
        if truth(aggregate, "validated_veto_present", OS_NAME):
            raise UnavailableSource("DecisionOSPlural:validated_veto_blocks_consensus",
                                    BLOCKED)
        excluded = plain_list(plural, "veto_excluded_option_ids", OS_NAME)
        if selected in excluded:
            raise UnavailableSource("DecisionOSPlural:excluded_option_selected",
                                    BLOCKED)
        if not truth(aggregate, "broadly_acceptable", OS_NAME):
            raise UnavailableSource("DecisionOSPlural:source_not_broadly_acceptable",
                                    BLOCKED)
        thresholds = field(plural, "thresholds", OS_NAME)
        # Strict mathematically exact comparisons of the native source
        # floating values. No epsilon loosened Lean hypothesis.
        for source_key, limit_key, op in (
            ("support_weight", "minimum_support_weight", "floor"),
            ("opposition_weight", "maximum_opposition_weight", "ceiling"),
            ("worst_case_lower", "minimum_worst_case_value", "floor"),
        ):
            observed = rational_float(field(aggregate, source_key, "aggregate"),
                                      "aggregate:" + source_key)
            limit = rational_float(field(thresholds, limit_key, "thresholds"),
                                   "thresholds:" + limit_key)
            valid = limit <= observed if op == "floor" else observed <= limit
            if not valid:
                raise UnavailableSource(
                    "DecisionOSPlural:real_order_boundary_not_certified:" + source_key
                )
        ranks = plain_list(plural, "ranked_aggregates", OS_NAME)
        broad = [x for x in ranks if type(x) is dict
                 and x.get("broadly_acceptable") is True]
        if not broad or broad[0].get("option_id") != selected:
            raise UnavailableSource("DecisionOSPlural:selected_not_first_broad",
                                    BLOCKED)
        route, recomputed, _retained = _adjudicate(
            plural, {"handover_required": False})
        require_match(route, "CONSENSUS_CANDIDATE",
                      "DecisionOSPlural:source_rule_consensus")
        require_match(recomputed, selected,
                      "DecisionOSPlural:source_rule_selection")
        if truth(field(plural, "non_authority", OS_NAME),
                 "consensus_truth_authority_granted", OS_NAME):
            raise UnavailableSource("DecisionOSPlural:truth_authority_forbidden",
                                    BLOCKED)
        # An original consensus route is not an independent proof of a
        # unique mathematically ranked candidate across other contexts.
        return record(OS_NAME, plural, [
            "DecisionOS.decision_state_digest",
            "DecisionOSPlural.source_decision_state_digest",
            "DecisionOSPlural.route",
            "DecisionOSPlural.selected_option_id",
            "DecisionOSPlural.source_option_ids",
            "DecisionOSPlural.aggregate_records[option_id=" + selected + "]",
            "DecisionOSPlural.thresholds",
            "DecisionOSPlural.veto_excluded_option_ids",
            "DecisionOSPlural.ranked_aggregates",
            "DecisionOSPlural.non_authority.consensus_truth_authority_granted",
        ], 1, edge=True, issues=(
            "ConsensusCertificate_Lean_proof_fields_not_constructed",
            "native_ranked_choice_not_general_CPythons_semantics_proof",
        ))
    except UnavailableSource as exc:
        return fail(OS_NAME, exc.reason, status=exc.status)
    except (TypeError, ValueError, KeyError, RecursionError, AttributeError) as exc:
        return fail(OS_NAME, "DecisionOSPlural:original_source_exception:" +
                    type(exc).__name__, status=BLOCKED)


__all__ = ("OS_NAME", "LEAN_THEOREMS", "audit_native_plural_consensus")
