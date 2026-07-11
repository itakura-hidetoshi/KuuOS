#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
import math
from typing import Any

STATUS_READY = "ready"
STATUS_BLOCKED = "blocked"


def _digest(value: Any) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return sha256(payload.encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class FiniteTemperatureConcentrationResult:
    status: str
    blockers: list[str]
    certificate: dict[str, Any] | None


def build_finite_temperature_concentration_certificate(
    source_zero_temperature_limit: dict[str, Any],
    candidate_actions: dict[str, float],
    temperature: float,
    epsilon: float,
) -> FiniteTemperatureConcentrationResult:
    blockers: list[str] = []
    if not source_zero_temperature_limit:
        blockers.append("missing_source_zero_temperature_limit")
    if not math.isfinite(temperature) or temperature <= 0.0:
        blockers.append("temperature_must_be_positive")
    if not math.isfinite(epsilon) or not 0.0 < epsilon < 1.0:
        blockers.append("epsilon_must_be_between_zero_and_one")
    if not candidate_actions:
        blockers.append("candidate_actions_empty")
    if len(candidate_actions) != len(set(candidate_actions)):
        blockers.append("duplicate_candidate_ids")
    for candidate_id, action in candidate_actions.items():
        if not candidate_id:
            blockers.append("empty_candidate_id")
        if not math.isfinite(action) or action < 0.0:
            blockers.append(f"invalid_action:{candidate_id}")

    if blockers:
        return FiniteTemperatureConcentrationResult(STATUS_BLOCKED, blockers, None)

    minimum_action = min(candidate_actions.values())
    minimizers = sorted(k for k, v in candidate_actions.items() if abs(v - minimum_action) <= 1e-12)
    nonminimal_gaps = {k: v - minimum_action for k, v in candidate_actions.items() if k not in minimizers}
    minimum_positive_gap = min(nonminimal_gaps.values()) if nonminimal_gaps else math.inf

    shifted_weights = {k: math.exp(-(v - minimum_action) / temperature) for k, v in candidate_actions.items()}
    partition = sum(shifted_weights.values())
    if not math.isfinite(partition) or partition <= 0.0:
        return FiniteTemperatureConcentrationResult(STATUS_BLOCKED, ["invalid_partition_function"], None)
    masses = {k: w / partition for k, w in shifted_weights.items()}
    minimizer_mass = sum(masses[k] for k in minimizers)
    nonminimal_mass = 1.0 - minimizer_mass

    if math.isinf(minimum_positive_gap):
        upper_bound = 0.0
    else:
        upper_bound = min(1.0, (len(nonminimal_gaps) / max(1, len(minimizers))) * math.exp(-minimum_positive_gap / temperature))

    certified = nonminimal_mass <= epsilon + 1e-12 and upper_bound <= epsilon + 1e-12
    certificate = {
        "source_zero_temperature_limit_digest": _digest(source_zero_temperature_limit),
        "candidate_action_digest": _digest(candidate_actions),
        "temperature": temperature,
        "epsilon": epsilon,
        "minimum_action": minimum_action,
        "minimal_action_candidate_ids": minimizers,
        "minimum_positive_action_gap": None if math.isinf(minimum_positive_gap) else minimum_positive_gap,
        "normalized_candidate_mass": masses,
        "minimal_support_mass": minimizer_mass,
        "nonminimal_support_mass": nonminimal_mass,
        "nonminimal_mass_upper_bound": upper_bound,
        "epsilon_concentration_certified": certified,
        "authority_invariance_preserved": True,
        "history_read_only": True,
        "future_only": True,
        "active_now": False,
        "execution_permission": False,
    }
    certificate["concentration_certificate_digest"] = _digest(certificate)
    return FiniteTemperatureConcentrationResult(STATUS_READY, [], certificate)
