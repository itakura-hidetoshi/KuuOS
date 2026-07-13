#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_memoryos_observer_relative_finite_window_qi_influence_planos_handoff_algebra_support_v0_1 import (
    exact_discarded_tail_residue,
    influence_handoff_observables,
)
from runtime.kuuos_memoryos_observer_relative_finite_window_qi_influence_planos_handoff_certificate_kernel_v0_1 import (
    issue_observer_relative_finite_window_qi_influence_planos_handoff_certificate,
)
from runtime.kuuos_memoryos_observer_relative_finite_window_qi_influence_planos_handoff_certificate_support_v0_1 import (
    expected_governance_claims,
)
from runtime.kuuos_memoryos_observer_relative_finite_window_qi_influence_planos_handoff_schema_support_v0_1 import (
    COMPONENTS,
    SCHEMA_VERSION,
    SOURCE_MEMORYOS_V040_SCHEMA_VERSION,
    SOURCE_PLANOS_V123_SCHEMA_VERSION,
    compute_input_digest,
    digest_object,
    normalize_candidate_couplings,
    normalize_component_map,
    normalize_history_projection_records,
    normalize_lag_weights,
    normalize_source_memoryos_v040_receipt,
    normalize_source_planos_v123_receipt,
)

RECORD_IDS = ["record-tail", "record-window-a", "record-window-b"]
RECORD_DIGESTS = ["record-tail-digest", "record-window-a-digest", "record-window-b-digest"]
OBSERVER_IDS = ["observer-alpha", "observer-beta"]
TRANSLATION_IDS = ["translation-alpha-beta"]
HISTORY_IDS = ["plan-history-a", "plan-history-b"]


def _effects(**overrides: int) -> dict[str, int]:
    values = {component: 0 for component in COMPONENTS}
    values.update(overrides)
    return values


def source_memory_receipt() -> dict:
    ledger_digest = digest_object(
        {
            "record_digests": RECORD_DIGESTS,
            "observer_ids": OBSERVER_IDS,
            "translation_ids": TRANSLATION_IDS,
        }
    )
    return {
        "accepted": True,
        "schema_version": SOURCE_MEMORYOS_V040_SCHEMA_VERSION,
        "certificate_digest": "memoryos-v0.40-certificate-digest",
        "record_ledger_digest": ledger_digest,
        "temporal_cycle_digest": "memoryos-v0.40-temporal-cycle-digest",
        "retained_record_ids": RECORD_IDS,
        "retained_record_digests": RECORD_DIGESTS,
        "retained_observer_ids": OBSERVER_IDS,
        "retained_translation_ids": TRANSLATION_IDS,
        "finite_non_markov_witness": True,
    }


def source_planos_receipt() -> dict:
    return {
        "accepted": True,
        "schema_version": SOURCE_PLANOS_V123_SCHEMA_VERSION,
        "input_digest": "planos-v1.23-partial-dephasing-input-digest",
        "retained_history_ids": HISTORY_IDS,
        "all_histories_retained": True,
        "history_pruning_performed": False,
        "history_ranking_performed": False,
        "representative_history_selected": False,
    }


def projection_records() -> list[dict]:
    return [
        {
            "record_id": RECORD_IDS[0],
            "record_digest": RECORD_DIGESTS[0],
            "observer_id": "observer-alpha",
            "event_digest": "event-tail",
            "sequence_index": 0,
            "component_effects": _effects(holonomy=1, rollback=1, residue=2),
            "translation_residue_visible": True,
            "observation_backaction_visible": True,
        },
        {
            "record_id": RECORD_IDS[1],
            "record_digest": RECORD_DIGESTS[1],
            "observer_id": "observer-alpha",
            "event_digest": "event-window-a",
            "sequence_index": 1,
            "component_effects": _effects(body=1, observation=2, residue=1),
            "translation_residue_visible": False,
            "observation_backaction_visible": True,
        },
        {
            "record_id": RECORD_IDS[2],
            "record_digest": RECORD_DIGESTS[2],
            "observer_id": "observer-beta",
            "event_digest": "event-window-b",
            "sequence_index": 2,
            "component_effects": _effects(boundary=1, leak=-1, holonomy=1, residue=2),
            "translation_residue_visible": True,
            "observation_backaction_visible": True,
        },
    ]


def candidate_couplings() -> list[dict]:
    return [
        {
            "history_id": "plan-history-a",
            "base_action_numerator": 11,
            "component_couplings": {
                "body": 1,
                "boundary": 2,
                "leak": 1,
                "observation": 1,
                "holonomy": 1,
                "recovery": -1,
                "rollback": 2,
                "lockin": 1,
                "residue": 3,
            },
        },
        {
            "history_id": "plan-history-b",
            "base_action_numerator": 20,
            "component_couplings": {
                "body": 0,
                "boundary": 1,
                "leak": 2,
                "observation": 0,
                "holonomy": 1,
                "recovery": 1,
                "rollback": -1,
                "lockin": 2,
                "residue": 1,
            },
        },
    ]


def reference_input_without_claims() -> dict:
    records = projection_records()
    return {
        "schema_version": SCHEMA_VERSION,
        "source_memoryos_v040_receipt": source_memory_receipt(),
        "source_planos_v123_receipt": source_planos_receipt(),
        "history_projection_records": records,
        "window_length": 2,
        "lag_weights": [3, 2],
        "discarded_tail_residue": dict(records[0]["component_effects"]),
        "discarded_tail_residue_visible": True,
        "candidate_couplings": candidate_couplings(),
        "action_denominator": 4,
    }


def build_reference_payload() -> dict:
    payload = reference_input_without_claims()
    source_memory = normalize_source_memoryos_v040_receipt(
        payload["source_memoryos_v040_receipt"]
    )
    source_planos = normalize_source_planos_v123_receipt(
        payload["source_planos_v123_receipt"]
    )
    records = normalize_history_projection_records(
        payload["history_projection_records"],
        source_record_ids=source_memory["retained_record_ids"],
        source_record_digests=source_memory["retained_record_digests"],
        source_observer_ids=source_memory["retained_observer_ids"],
        source_translation_ids=source_memory["retained_translation_ids"],
    )
    lag_weights = normalize_lag_weights(
        payload["lag_weights"], window_length=payload["window_length"]
    )
    tail = exact_discarded_tail_residue(records[:-payload["window_length"]])
    assert tail == normalize_component_map(
        payload["discarded_tail_residue"], "discarded_tail_residue"
    )
    couplings = normalize_candidate_couplings(
        payload["candidate_couplings"],
        source_history_ids=source_planos["retained_history_ids"],
    )
    normalized_input = {
        "source_memoryos_v040_receipt": source_memory,
        "source_planos_v123_receipt": source_planos,
        "history_projection_records": records,
        "window_length": payload["window_length"],
        "lag_weights": lag_weights,
        "discarded_tail_residue": tail,
        "discarded_tail_residue_visible": True,
        "candidate_couplings": couplings,
        "action_denominator": payload["action_denominator"],
    }
    input_digest = compute_input_digest(**normalized_input)
    observables = influence_handoff_observables(
        source_memoryos_v040_receipt=source_memory,
        source_planos_v123_receipt=source_planos,
        projection_records=records,
        window_length=payload["window_length"],
        lag_weights=lag_weights,
        discarded_tail_residue=tail,
        candidate_couplings=couplings,
        action_denominator=payload["action_denominator"],
        input_digest=input_digest,
    )
    payload["claims"] = {**observables, **expected_governance_claims()}
    return payload


def assert_rejects(payload: dict, blocker: str) -> None:
    result = issue_observer_relative_finite_window_qi_influence_planos_handoff_certificate(
        payload
    )
    assert not result["accepted"], result
    assert blocker in result["blockers"], result["blockers"]


def main() -> int:
    payload = build_reference_payload()
    certificate = issue_observer_relative_finite_window_qi_influence_planos_handoff_certificate(
        payload
    )
    assert certificate["accepted"], certificate["blockers"]
    obs = certificate["observables"]
    assert obs["window_record_ids"] == ["record-window-a", "record-window-b"]
    assert obs["discarded_tail_record_ids"] == ["record-tail"]
    assert obs["weighted_window_components"] == {
        "body": 3,
        "boundary": 2,
        "leak": -2,
        "observation": 6,
        "holonomy": 2,
        "recovery": 0,
        "rollback": 0,
        "lockin": 0,
        "residue": 7,
    }
    assert obs["discarded_tail_residue"] == _effects(
        holonomy=1, rollback=1, residue=2
    )
    profile_a, profile_b = obs["candidate_influence_profile"]
    assert profile_a["window_influence_numerator"] == 34
    assert profile_a["tail_influence_numerator"] == 9
    assert profile_a["total_history_influence_numerator"] == 43
    assert profile_a["window_only_action_numerator"] == 45
    assert profile_a["conditioned_action_numerator"] == 54
    assert profile_b["window_influence_numerator"] == 7
    assert profile_b["tail_influence_numerator"] == 2
    assert profile_b["conditioned_action_numerator"] == 29
    assert obs["tail_sensitive_candidate_count"] == 2
    assert obs["tail_residue_changes_at_least_one_candidate"]
    assert obs["all_planos_histories_retained"]
    assert not obs["full_history_replaced"]
    assert obs["translation_residue_visible_record_count"] == 2
    assert certificate["certificate_digest"]

    tampered = copy.deepcopy(payload)
    tampered["source_memoryos_v040_receipt"]["record_ledger_digest"] = "substituted"
    assert_rejects(tampered, "source_memoryos_v040_record_ledger_digest_invalid")

    tampered = copy.deepcopy(payload)
    tampered["history_projection_records"][1]["record_digest"] = "substituted"
    assert_rejects(
        tampered,
        "history_projection_record_digest_binding_mismatch_record-window-a",
    )

    tampered = copy.deepcopy(payload)
    tampered["history_projection_records"][2]["sequence_index"] = 1
    assert_rejects(
        tampered,
        "history_projection_sequence_not_contiguous_record-window-b",
    )

    tampered = copy.deepcopy(payload)
    tampered["history_projection_records"][0]["observer_id"] = "observer-missing"
    assert_rejects(
        tampered,
        "history_projection_observer_not_source_bound_observer-missing",
    )

    tampered = copy.deepcopy(payload)
    tampered["history_projection_records"][0]["translation_residue_visible"] = False
    tampered["history_projection_records"][2]["translation_residue_visible"] = False
    assert_rejects(tampered, "source_translation_residue_not_projected")

    tampered = copy.deepcopy(payload)
    tampered["discarded_tail_residue"]["residue"] = 0
    assert_rejects(tampered, "discarded_tail_residue_not_exact")

    tampered = copy.deepcopy(payload)
    tampered["discarded_tail_residue_visible"] = False
    assert_rejects(tampered, "discarded_tail_residue_visibility_required")

    tampered = copy.deepcopy(payload)
    tampered["lag_weights"] = [3, -2]
    assert_rejects(tampered, "lag_weight_invalid")

    tampered = copy.deepcopy(payload)
    tampered["window_length"] = 4
    assert_rejects(tampered, "window_length_exceeds_record_count")

    tampered = copy.deepcopy(payload)
    tampered["candidate_couplings"].pop()
    assert_rejects(tampered, "candidate_couplings_source_history_support_mismatch")

    for field in (
        "history_pruning_performed",
        "history_ranking_performed",
        "representative_history_selected",
        "plan_selection_performed",
        "activation_performed",
        "execution_permission",
        "source_memoryos_v040_mutated",
        "source_planos_v123_mutated",
        "persistent_world_state_mutated",
        "truth_authority_granted",
    ):
        tampered = copy.deepcopy(payload)
        tampered["claims"][field] = True
        assert_rejects(tampered, "claim_mismatch_" + field)

    tampered = copy.deepcopy(payload)
    tampered["claims"]["candidate_influence_profile"][0][
        "conditioned_action_numerator"
    ] = 999
    assert_rejects(tampered, "claim_mismatch_candidate_influence_profile")

    print(
        json.dumps(
            {
                "status": "PASS",
                "schema_version": SCHEMA_VERSION,
                "record_window": {
                    "full": obs["full_record_ids"],
                    "window": obs["window_record_ids"],
                    "discarded_tail": obs["discarded_tail_record_ids"],
                    "tail_residue": obs["discarded_tail_residue"],
                },
                "candidate_influence_profile": obs["candidate_influence_profile"],
                "all_planos_histories_retained": obs[
                    "all_planos_histories_retained"
                ],
                "full_history_replaced": obs["full_history_replaced"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
