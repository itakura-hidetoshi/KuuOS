from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

from runtime.kuuos_belief_os_types_v0_1 import sha
from runtime.kuuos_act_os_fixture_v0_1 import (
    host_inputs,
    prepared_project_state,
    source_plan,
)
from runtime.v01_act_os_authority_bound_invocation import _finish as finish_act
from runtime.kuuos_observe_os_kernel_v0_1 import (
    build_initial_observe_state,
    build_observe_event,
)
from runtime.kuuos_observe_os_store_v0_1 import ObserveStore


def source_act_state(root: Path) -> dict[str, Any]:
    plan_state, activation = source_plan(root)
    policy, bundle, license_packet, projection = host_inputs(job_id="observe-source-job")
    store, act_state = prepared_project_state(
        root=root / "act-source",
        act_id="observe-source-act",
        plan_state=plan_state,
        plan_activation=activation,
        job_id="observe-source-job",
        host_license=license_packet,
        projection=projection,
    )
    ready, _ = finish_act(
        store=store,
        state=act_state,
        bundle=bundle,
        policy=policy,
        invoke_ms=90_004,
    )
    if ready.get("route") != "EFFECT_RECORDED":
        raise AssertionError(ready)
    return ready


def event(
    state: Mapping[str, Any], phase: str, payload: Mapping[str, Any], tick: int
) -> dict[str, Any]:
    return build_observe_event(
        state=state,
        target_phase=phase,
        artifact_digest=sha({"phase": phase, "payload": dict(payload), "tick": tick}),
        payload=payload,
        now_ms=100_000 + tick,
    )


def apply(
    store: ObserveStore,
    state: Mapping[str, Any],
    phase: str,
    payload: Mapping[str, Any],
    tick: int,
) -> dict[str, Any]:
    result = store.apply(event(state, phase, payload, tick))
    if result.get("status") != "APPLIED":
        raise AssertionError(result)
    return result["state"]


def evidence_items(*, conflict: bool = False) -> list[dict[str, Any]]:
    return [
        {
            "evidence_id": "evidence-1",
            "channel_id": "system-output",
            "source_kind": "system",
            "collector_id": "collector-system",
            "independent_source_id": "source-system",
            "collected_at_ms": 99_100,
            "raw_artifact_digest": sha("raw-system"),
            "value_digest": sha("value-system-divergent" if conflict else "value-system"),
            "uncertainty_digest": sha("uncertainty-system"),
            "calibration_digest": sha("calibration-system"),
            "context_digest": sha("context-system"),
            "tamper_evidence_digest": sha("tamper-system"),
            "provenance_hop_digests": [sha("source"), sha("collector")],
        },
        {
            "evidence_id": "evidence-2",
            "channel_id": "independent-check",
            "source_kind": "human",
            "collector_id": "collector-human",
            "independent_source_id": "source-human",
            "collected_at_ms": 99_200,
            "raw_artifact_digest": sha("raw-human"),
            "value_digest": sha("value-human"),
            "uncertainty_digest": sha("uncertainty-human"),
            "calibration_digest": sha("calibration-human"),
            "context_digest": sha("context-human"),
            "tamper_evidence_digest": sha("tamper-human"),
            "provenance_hop_digests": [sha("witness"), sha("review")],
        },
    ]


def prepared_assessed_state(
    *,
    root: Path,
    observe_id: str,
    act_state: Mapping[str, Any],
    quality: Mapping[str, Any] | None = None,
    conflict: bool = False,
) -> tuple[ObserveStore, dict[str, Any]]:
    store = ObserveStore(root)
    state = store.initialize(
        build_initial_observe_state(
            observe_id=observe_id,
            act_state=act_state,
            now_ms=98_000,
        )
    )
    state = apply(
        store,
        state,
        "scope",
        {
            "observation_target_digest": act_state["expected_observation_digest"],
            "observation_protocol_digest": sha("observe-protocol"),
            "window_start_ms": 99_000,
            "window_end_ms": 99_900,
            "channels": ["system-output", "independent-check"],
            "minimum_evidence_items": 2,
            "independence_required": True,
            "observer_context_digest": sha("observer-context"),
            "baseline_digest": sha("baseline"),
        },
        1,
    )
    state = apply(
        store,
        state,
        "collect",
        {"evidence_items": evidence_items(conflict=conflict)},
        2,
    )
    state = apply(
        store,
        state,
        "trace",
        {
            "provenance_receipt_digest": sha("provenance-receipt"),
            "evidence_chain_complete": True,
            "source_identity_preserved": True,
            "raw_artifacts_immutable": True,
            "no_unbound_evidence": True,
        },
        3,
    )
    report = dict(
        quality
        or {
            "coverage": 0.95,
            "freshness": 0.9,
            "provenance": 0.95,
            "calibration": 0.9,
            "completeness": 0.95,
            "conflict": 0.1,
            "assessment_method_digest": sha("quality-method"),
        }
    )
    state = apply(
        store,
        state,
        "assess",
        {"quality_report": report},
        4,
    )
    return store, state
