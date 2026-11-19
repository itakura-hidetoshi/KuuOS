"""DecisionOSWa: original plural-mediated Lean WaEndorsementGate fields.

The original v0.3 ENDORSE result is not a universal truth claim.
Only when the original plural→Wa typed edge, original validators,
source option/profile identities and finite Wa observations agree do
we check the v0.27 Lean-structure data obligations.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations
from typing import Any

from runtime.kuuos_lean_python_decision_mediator_source_v0_29 import (
    BLOCKED, UnavailableSource, copied_edge, mediator_state, field,
    truth, string, plain_list, require_match, rational_float,
    fail, record,
)
from runtime.kuuos_lean_python_wa_finite_extrema_v0_25 import (
    audit_wa_finite_extrema_state,
)
from runtime import kuuos_lean_python_decision_wa_obligations_v0_27 as proof
from runtime.kuuos_decision_os_wa_kernel_v0_3 import _profile_digest

OS_NAME = "DecisionOSWa"


def audit_native_wa_endorsement(plural_state: Any, wa_state: Any):
    """Read original Plural→Wa source and check the selected endorsement."""
    try:
        plural = mediator_state("DecisionOSPlural", plural_state)
        wa = mediator_state(OS_NAME, wa_state)
        copied_edge("DecisionOSPlural", OS_NAME, plural, wa)
        if string(wa, "route", OS_NAME) != "ENDORSE":
            raise UnavailableSource("DecisionOSWa:no_native_endorsement")
        selected = string(plural, "selected_option_id", "DecisionOSPlural")
        require_match(string(wa, "source_selected_option_id", OS_NAME),
                      selected, "DecisionOSWa:plural_selected_identity")
        if selected not in plain_list(wa, "endorsed_option_ids", OS_NAME):
            raise UnavailableSource("DecisionOSWa:selected_not_endorsed", BLOCKED)
        profiles = plain_list(wa, "profiles", OS_NAME)
        records = plain_list(wa, "wa_records", OS_NAME)
        classified = plain_list(wa, "false_harmony_records", OS_NAME)
        def exactly_one(items: list, label: str) -> dict:
            matches = [item for item in items
                       if type(item) is dict and item.get("option_id") == selected]
            if len(matches) != 1:
                raise UnavailableSource("DecisionOSWa:" + label + ":not_unique",
                                        BLOCKED)
            return matches[0]
        profile = exactly_one(profiles, "profile")
        record_item = exactly_one(records, "wa_record")
        false_record = exactly_one(classified, "false_harmony")
        require_match(string(profile, "wa_profile_digest", "DecisionOSWa.profile"),
                      _profile_digest(profile), "DecisionOSWa:profile_digest")
        plurality = field(wa, "plurality", OS_NAME)
        for key in ("all_source_options_profiled",
                    "retained_alternatives_preserved",
                    "selected_identity_preserved",
                    "stakeholder_sections_preserved",
                    "veto_and_appeal_history_preserved"):
            if not truth(plurality, key, "DecisionOSWa.plurality"):
                raise UnavailableSource("DecisionOSWa:plurality_not_preserved:" + key,
                                        BLOCKED)
        if truth(plurality, "silent_substitution_detected",
                 "DecisionOSWa.plurality"):
            raise UnavailableSource("DecisionOSWa:silent_substitution", BLOCKED)
        if truth(false_record, "suspected_false_harmony",
                 "DecisionOSWa.false_harmony"):
            raise UnavailableSource("DecisionOSWa:suspected_requires_reobservation",
                                    BLOCKED)
        # Strengthen to exact rational comparison of recorded finite
        # native floats. We do NOT add tolerance to Lean's inequalities.
        limits = field(wa, "thresholds", OS_NAME)
        score = field(record_item, "wa_interval", "DecisionOSWa.record")
        weakest = field(record_item, "weakest_interval", "DecisionOSWa.record")
        floor_wa = (rational_float(field(score, "lower", "DecisionOSWa.record"),
                                  "wa:lower")
                    >= rational_float(field(limits, "minimum_wa_floor", "Wa.thresholds"),
                                      "wa:threshold"))
        floor_weak = (
            rational_float(field(weakest, "lower", "DecisionOSWa.record"),
                           "weakest:lower")
            >= rational_float(field(limits, "minimum_dimension_floor", "Wa.thresholds"),
                              "weakest:threshold"))
        projection = {
            "confirmedFalseHarmony": truth(
                false_record, "confirmed_false_harmony", "DecisionOSWa.false_harmony"),
            "minorityPreserved": truth(
                profile, "minority_preserved", "DecisionOSWa.profile"),
            "dissentConsidered": truth(
                profile, "dissent_considered", "DecisionOSWa.profile"),
            "minimumWaPassed": floor_wa,
            "weakestDimensionPassed": floor_weak,
            "sourcePluralIdentityPreserved": truth(
                plurality, "selected_identity_preserved", "DecisionOSWa.plurality"),
        }
        v027 = proof.audit_witness(projection)
        if v027.status == BLOCKED:
            raise UnavailableSource("DecisionOSWa:source_bound_lean_gate_failed",
                                    BLOCKED)
        if v027.status != "LOCAL_CONDITIONS_CHECKED":
            raise UnavailableSource("DecisionOSWa:source_bound_lean_gate_incomplete")
        prior = audit_wa_finite_extrema_state(wa)
        if prior.get("all_original_finite_extrema_checked") is not True:
            raise UnavailableSource("DecisionOSWa:original_finite_extrema_unconfirmed")
        return record(OS_NAME, wa, [
            "DecisionOSPlural.plural_state_digest",
            "DecisionOSWa.source_plural_state_digest",
            "DecisionOSWa.source_selected_option_id",
            "DecisionOSWa.endorsed_option_ids",
            "DecisionOSWa.profiles[option_id=" + selected + "].wa_profile_digest",
            "DecisionOSWa.false_harmony_records[option_id=" + selected + "]",
            "DecisionOSWa.wa_records[option_id=" + selected + "].wa_interval.lower",
            "DecisionOSWa.wa_records[option_id=" + selected + "].weakest_interval.lower",
            "DecisionOSWa.thresholds",
            "DecisionOSWa.plurality",
        ], 1, edge=True, issues=(
            "Lean_WaEndorsementGate_proof_fields_not_constructed",
            "original_native_float_comparisons_only_conditional",
        ))
    except UnavailableSource as exc:
        return fail(OS_NAME, exc.reason, status=exc.status)
    except (TypeError, ValueError, KeyError, RecursionError, AttributeError) as exc:
        return fail(OS_NAME, "DecisionOSWa:original_source_exception:" +
                    type(exc).__name__, status=BLOCKED)


__all__ = ("OS_NAME", "audit_native_wa_endorsement")
