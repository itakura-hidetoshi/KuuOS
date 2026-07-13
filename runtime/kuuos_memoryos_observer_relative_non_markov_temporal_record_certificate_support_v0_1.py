from __future__ import annotations

NON_AUTHORITY_FIELDS = (
    "absolute_observer_claimed",
    "event_record_identity_claimed",
    "history_erasure_performed",
    "memory_overwrite_performed",
    "plan_selection_performed",
    "decision_replayed_as_new_decision",
    "activation_performed",
    "execution_permission",
    "world_mutated",
    "verification_result_claimed",
    "source_planos_mutated",
    "source_decisionos_mutated",
    "source_memoryos_v039_mutated",
)

REQUIRED_TRUE_FIELDS = (
    "observer_relative_recording",
    "append_only_record_lineage",
    "translation_residue_visible",
    "non_markov_history_dependence_preserved",
    "planos_future_bound",
    "decisionos_present_bound",
    "memoryos_past_bound",
    "observe_channel_bound",
)


def expected_governance_claims() -> dict[str, bool]:
    return {
        **{field: True for field in REQUIRED_TRUE_FIELDS},
        **{field: False for field in NON_AUTHORITY_FIELDS},
    }
