#!/usr/bin/env python3
from __future__ import annotations
from typing import Any, Mapping
from runtime.kuuos_observeos_sequential_epistemic_observability_common_v0_1 import *
from runtime.kuuos_observeos_sequential_epistemic_observability_evaluation_v0_1 import evaluate
from runtime.kuuos_observeos_sequential_epistemic_observability_receipt_v0_1 import build_receipt

def build_observeos_sequential_epistemic_observability_envelope(
    *, source_observation_receipt: Mapping[str, Any],
    expected_source_observation_receipt_digest: str,
    observability_packet: Mapping[str, Any], observability_policy: Mapping[str, Any],
) -> ObserveOSSequentialEpistemicObservabilityResult:
    blockers, ctx = evaluate(source_observation_receipt, expected_source_observation_receipt_digest,
        observability_packet, observability_policy)
    if blockers:
        return ObserveOSSequentialEpistemicObservabilityResult(STATUS_BLOCKED, blockers, None)
    return ObserveOSSequentialEpistemicObservabilityResult(
        STATUS_READY, [], build_receipt(expected_source_observation_receipt_digest, ctx))
