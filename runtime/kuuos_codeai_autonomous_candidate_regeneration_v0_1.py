#!/usr/bin/env python3
from __future__ import annotations
from typing import Any
from runtime.kuuos_codeai_autonomous_candidate_regeneration_common_v0_1 import *
from runtime.kuuos_codeai_autonomous_candidate_regeneration_preflight_v0_1 import prepare
from runtime.kuuos_codeai_autonomous_candidate_regeneration_loop_v0_1 import run_prepared

def build_codeai_autonomous_candidate_regeneration(
    *, source_generation_receipt: Any, source_observation_receipt: Any,
    repository_files: Any, seed_candidates: Any, regeneration_request: Any,
    provider_adapters: Any, regeneration_policy: Any, candidate_policy: Any,
):
    prepared, failure = prepare(
        source_generation_receipt=source_generation_receipt,
        source_observation_receipt=source_observation_receipt,
        repository_files=repository_files, seed_candidates=seed_candidates,
        regeneration_request=regeneration_request,
        provider_adapters=provider_adapters,
        regeneration_policy=regeneration_policy,
        candidate_policy=candidate_policy)
    if failure is not None:
        return failure
    assert prepared is not None
    return run_prepared(prepared)

__all__ = [name for name in globals() if name.isupper()] + [
    "CandidateRegenerationAttemptReceipt",
    "CodeAIAutonomousCandidateRegenerationResult",
    "ProviderAdapter",
    "build_codeai_autonomous_candidate_regeneration",
]
