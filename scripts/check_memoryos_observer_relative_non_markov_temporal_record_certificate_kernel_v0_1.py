#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_memoryos_observer_relative_non_markov_temporal_record_algebra_support_v0_1 import (
    temporal_record_observables,
)
from runtime.kuuos_memoryos_observer_relative_non_markov_temporal_record_certificate_kernel_v0_1 import (
    issue_observer_relative_non_markov_temporal_record_certificate,
)
from runtime.kuuos_memoryos_observer_relative_non_markov_temporal_record_certificate_support_v0_1 import (
    expected_governance_claims,
)
from runtime.kuuos_memoryos_observer_relative_non_markov_temporal_record_schema_support_v0_1 import (
    SCHEMA_VERSION,
    ZERO_DIGEST,
    build_record_chain,
    compute_input_digest,
    normalize_observers,
    normalize_translations,
)

SOURCE_PLANOS = "planos-v1.23-coherence-certificate-digest"
SOURCE_DECISIONOS = "decisionos-v0.6-present-cut-digest"
SOURCE_MEMORYOS = "memoryos-v0.39-observe-intake-capsule-digest"
SOURCE_WORLD = "kuuos-v14-world-model-digest"


def _observer(observer_id: str) -> dict:
    return {
        "observer_id": observer_id,
        "observer_frame_digest": observer_id + "-frame-digest",
        "instrument_family_digest": observer_id + "-instrument-family-digest",
        "observation_chart_digest": observer_id + "-chart-digest",
        "absolute_observer": False,
    }


def _record(
    record_id: str,
    observer_id: str,
    event_digest: str,
    observation_value: int,
    history_effect: int,
    observer_state_index: int,
    world_state_index: int,
) -> dict:
    return {
        "record_id": record_id,
        "observer_id": observer_id,
        "event_digest": event_digest,
        "plan_future_ensemble_digest": SOURCE_PLANOS,
        "decision_present_cut_digest": SOURCE_DECISIONOS,
        "observation_operator_digest": record_id + "-operator-digest",
        "instrument_trace_digest": record_id + "-instrument-trace-digest",
        "pre_observer_state_digest": f"{observer_id}-state-{observer_state_index}",
        "post_observer_state_digest": f"{observer_id}-state-{observer_state_index + 1}",
        "pre_world_state_digest": f"world-state-{world_state_index}",
        "post_world_state_digest": f"world-state-{world_state_index + 1}",
        "backaction_digest": record_id + "-backaction-digest",
        "residue_digest": record_id + "-residue-digest",
        "source_memoryos_v039_capsule_digest": SOURCE_MEMORYOS,
        "observation_value": observation_value,
        "history_effect": history_effect,
        "uncertainty_numerator": abs(history_effect) + 1,
        "uncertainty_denominator": 8,
        "record_not_event_identity": True,
    }


def reference_input_without_claims() -> dict:
    return {
        "schema_version": SCHEMA_VERSION,
        "source_planos_v123_certificate_digest": SOURCE_PLANOS,
        "source_decisionos_v06_certificate_digest": SOURCE_DECISIONOS,
        "source_memoryos_v039_capsule_digest": SOURCE_MEMORYOS,
        "source_world_model_digest": SOURCE_WORLD,
        "observers": [_observer("observer-alpha"), _observer("observer-beta")],
        "records": [
            _record("record-alpha-shared", "observer-alpha", "event-shared", 7, 2, 0, 0),
            _record("record-beta-shared", "observer-beta", "event-shared", 10, -1, 0, 1),
            _record("record-alpha-later", "observer-alpha", "event-later", 4, 3, 1, 2),
        ],
        "translations": [
            {
                "translation_id": "translation-alpha-beta-shared",
                "source_observer_id": "observer-alpha",
                "target_observer_id": "observer-beta",
                "event_digest": "event-shared",
                "translation_map_digest": "translation-alpha-beta-map-digest",
                "offset_integer": 2,
                "source_value": 7,
                "target_value": 10,
                "translated_value": 9,
                "translation_residue": 1,
                "residue_visible": True,
            }
        ],
        "memory_kernel_weights": [3, 2, 1],
        "counterfactual_history_effects": [2, -1, 0],
        "present_signal": 5,
    }


def build_reference_payload() -> dict:
    payload = reference_input_without_claims()
    observers = normalize_observers(payload["observers"])
    records = build_record_chain(payload["records"])
    translations = normalize_translations(payload["translations"])
    input_digest = compute_input_digest(
        source_planos_v123_certificate_digest=SOURCE_PLANOS,
        source_decisionos_v06_certificate_digest=SOURCE_DECISIONOS,
        source_memoryos_v039_capsule_digest=SOURCE_MEMORYOS,
        source_world_model_digest=SOURCE_WORLD,
        observers=observers,
        records=records,
        translations=translations,
        memory_kernel_weights=payload["memory_kernel_weights"],
        counterfactual_history_effects=payload["counterfactual_history_effects"],
        present_signal=payload["present_signal"],
    )
    observables = temporal_record_observables(
        source_planos_v123_certificate_digest=SOURCE_PLANOS,
        source_decisionos_v06_certificate_digest=SOURCE_DECISIONOS,
        source_memoryos_v039_capsule_digest=SOURCE_MEMORYOS,
        source_world_model_digest=SOURCE_WORLD,
        observers=observers,
        records=records,
        translations=translations,
        memory_kernel_weights=payload["memory_kernel_weights"],
        counterfactual_history_effects=payload["counterfactual_history_effects"],
        present_signal=payload["present_signal"],
        input_digest=input_digest,
    )
    payload["records"] = records
    payload["claims"] = {**observables, **expected_governance_claims()}
    return payload


def rechain(payload: dict) -> None:
    raw = []
    for record in payload["records"]:
        row = dict(record)
        row.pop("sequence_index", None)
        row.pop("previous_record_digest", None)
        row.pop("record_digest", None)
        raw.append(row)
    payload["records"] = build_record_chain(raw)


def assert_rejects(payload: dict, blocker: str) -> None:
    certificate = issue_observer_relative_non_markov_temporal_record_certificate(payload)
    assert not certificate["accepted"], certificate
    assert blocker in certificate["blockers"], certificate["blockers"]


def main() -> int:
    payload = build_reference_payload()
    certificate = issue_observer_relative_non_markov_temporal_record_certificate(payload)
    assert certificate["accepted"], certificate["blockers"]
    obs = certificate["observables"]
    assert obs["retained_history_effects"] == [2, -1, 3]
    assert obs["history_memory_contribution"] == 7
    assert obs["counterfactual_memory_contribution"] == 4
    assert obs["next_context_from_retained_history"] == 12
    assert obs["next_context_from_counterfactual_history"] == 9
    assert obs["finite_non_markov_witness"]
    assert obs["visible_translation_residue_count"] == 1
    assert obs["translation_residue_profile"][0]["translation_residue"] == 1
    assert obs["multiple_observer_event_count"] == 1
    assert obs["observer_state_change_count"] == 3
    assert obs["world_or_backaction_visible_count"] == 3
    assert obs["record_count"] == 3
    assert obs["observer_count"] == 2
    assert obs["all_records_not_event_identity"]

    tampered = copy.deepcopy(payload)
    tampered["observers"][1]["observer_id"] = "observer-alpha"
    assert_rejects(tampered, "observer_id_duplicate_observer-alpha")

    tampered = copy.deepcopy(payload)
    tampered["observers"][0]["absolute_observer"] = True
    assert_rejects(tampered, "absolute_observer_forbidden")

    tampered = copy.deepcopy(payload)
    tampered["records"][1]["previous_record_digest"] = ZERO_DIGEST
    assert_rejects(tampered, "record_previous_digest_invalid_record-beta-shared")

    tampered = copy.deepcopy(payload)
    tampered["records"][0]["observer_id"] = "observer-missing"
    rechain(tampered)
    assert_rejects(tampered, "record_observer_missing_record-alpha-shared")

    tampered = copy.deepcopy(payload)
    tampered["records"][0]["record_not_event_identity"] = False
    rechain(tampered)
    assert_rejects(tampered, "record_event_identity_forbidden_record-alpha-shared")

    tampered = copy.deepcopy(payload)
    tampered["translations"][0]["translation_residue"] = 0
    assert_rejects(tampered, "translation_residue_invalid_translation-alpha-beta-shared")

    tampered = copy.deepcopy(payload)
    tampered["memory_kernel_weights"] = [3, -2, 1]
    assert_rejects(tampered, "memory_kernel_weight_negative")

    for field in (
        "absolute_observer_claimed",
        "history_erasure_performed",
        "memory_overwrite_performed",
        "plan_selection_performed",
        "activation_performed",
        "execution_permission",
        "world_mutated",
    ):
        tampered = copy.deepcopy(payload)
        tampered["claims"][field] = True
        assert_rejects(tampered, "claim_mismatch_" + field)

    tampered = copy.deepcopy(payload)
    tampered["claims"]["next_context_from_retained_history"] = 999
    assert_rejects(tampered, "claim_mismatch_next_context_from_retained_history")

    print(json.dumps({
        "status": "PASS",
        "schema_version": SCHEMA_VERSION,
        "observer_count": obs["observer_count"],
        "record_count": obs["record_count"],
        "temporal_roles": obs["temporal_roles"],
        "non_markov_witness": {
            "present_signal": obs["present_signal"],
            "retained_history": obs["retained_history_effects"],
            "counterfactual_history": obs["counterfactual_history_effects"],
            "next_context_retained": obs["next_context_from_retained_history"],
            "next_context_counterfactual": obs["next_context_from_counterfactual_history"],
        },
        "translation_residue_profile": obs["translation_residue_profile"],
        "all_records_retained": True,
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
