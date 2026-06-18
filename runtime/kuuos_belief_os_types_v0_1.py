from __future__ import annotations

import hashlib
import json
import math
from copy import deepcopy
from typing import Any, Mapping, Sequence

VERSION = "kuuos_belief_os_relational_conditional_kernel_v0_1"
STATE_VERSION = "kuuos_belief_os_state_v0_1"
EVENT_VERSION = "kuuos_belief_os_event_v0_1"
APPLY_RESULT_VERSION = "kuuos_belief_os_apply_result_v0_1"
STORE_COMMIT_VERSION = "kuuos_belief_os_store_commit_v0_1"
ACTIVATION_RECEIPT_VERSION = "kuuos_belief_os_replan_activation_receipt_v0_1"

PHASES = (
    "propose",
    "contextualize",
    "trace",
    "weigh",
    "challenge",
    "qi_condition",
    "two_truths_check",
    "middle_way_gate",
    "commit",
)

NEXT_PHASE = {
    "propose": "contextualize",
    "contextualize": "trace",
    "trace": "weigh",
    "weigh": "challenge",
    "challenge": "qi_condition",
    "qi_condition": "two_truths_check",
    "two_truths_check": "middle_way_gate",
    "middle_way_gate": "commit",
    "commit": "propose",
}

ROUTES = frozenset(
    {
        "CANDIDATE",
        "OBSERVE",
        "HOLD",
        "REPAIR",
        "REJECT",
        "QUARANTINE",
        "RETIRED",
    }
)

QI_ALLOWED_ROLES = frozenset(
    {
        "contextual_prior_modifier",
        "likelihood_context_modifier",
        "temporal_transition_constraint",
        "anomaly_signal",
        "recovery_trajectory_signal",
        "context_transport_support",
    }
)

QI_FORBIDDEN_ROLES = frozenset(
    {
        "standalone_truth_evidence",
        "automatic_fact_promotion",
        "direct_execution_license",
        "proof_substitute",
        "standalone_clinical_certainty",
        "unrestricted_causal_explanation",
    }
)

NON_AUTHORITY_FLAGS = {
    "truth_authority_granted": False,
    "execution_authority_granted": False,
    "proof_authority_granted": False,
    "clinical_authority_granted": False,
    "institutional_authority_granted": False,
    "essence_authority_granted": False,
    "memory_overwrite_authority_granted": False,
    "self_modification_authority_granted": False,
}

REQUIRED_BOUNDARY = {
    "belief_is_conditional": True,
    "belief_is_not_truth": True,
    "confidence_is_not_certainty": True,
    "memory_persistence_is_not_belief_sovereignty": True,
    "counterevidence_is_preserved": True,
    "qi_is_samvrti_context_only": True,
    "qi_does_not_grant_authority": True,
    "two_truths_are_separated": True,
    "middle_way_avoids_reification_and_erasure": True,
    "history_is_append_only": True,
    "learning_is_future_only": True,
    "activation_requires_mission_replan": True,
}

DEFAULT_UNCERTAINTY = {
    "epistemic": 1.0,
    "aleatory": 0.0,
    "contextual": 1.0,
    "temporal": 1.0,
    "model": 1.0,
    "observer": 1.0,
    "process_history": 1.0,
}


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def digest_without(value: Mapping[str, Any], field: str) -> str:
    payload = dict(value)
    payload.pop(field, None)
    return sha(payload)


def state_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "belief_state_digest")


def event_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "belief_event_digest")


def apply_result_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "belief_apply_result_digest")


def store_commit_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "belief_store_commit_digest")


def activation_receipt_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "belief_activation_receipt_digest")


def require_nonempty_string(value: Any, name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{name}_invalid")
    text = value.strip()
    if not text:
        raise ValueError(f"{name}_missing")
    return text


def require_nonnegative_int(value: Any, name: str) -> int:
    if isinstance(value, bool):
        raise ValueError(f"{name}_invalid")
    try:
        result = int(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{name}_invalid") from exc
    if result < 0:
        raise ValueError(f"{name}_negative")
    return result


def require_finite_number(
    value: Any,
    name: str,
    *,
    minimum: float | None = None,
    maximum: float | None = None,
) -> float:
    if isinstance(value, bool):
        raise ValueError(f"{name}_invalid")
    try:
        result = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{name}_invalid") from exc
    if not math.isfinite(result):
        raise ValueError(f"{name}_not_finite")
    if minimum is not None and result < minimum:
        raise ValueError(f"{name}_below_minimum")
    if maximum is not None and result > maximum:
        raise ValueError(f"{name}_above_maximum")
    return result


def require_bool(value: Any, name: str) -> bool:
    if not isinstance(value, bool):
        raise ValueError(f"{name}_invalid")
    return value


def require_unique_strings(
    values: Sequence[Any], name: str, *, allow_empty: bool = True
) -> list[str]:
    if isinstance(values, (str, bytes)):
        raise ValueError(f"{name}_invalid")
    normalized = [require_nonempty_string(item, name) for item in values]
    if not allow_empty and not normalized:
        raise ValueError(f"{name}_missing")
    if len(normalized) != len(set(normalized)):
        raise ValueError(f"{name}_duplicate")
    return normalized


def require_mapping(value: Any, name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{name}_invalid")
    return value


def normalize_credal_state(value: Mapping[str, Any]) -> dict[str, float | None]:
    lower = require_finite_number(
        value.get("lower_probability"), "lower_probability", minimum=0.0, maximum=1.0
    )
    upper = require_finite_number(
        value.get("upper_probability"), "upper_probability", minimum=0.0, maximum=1.0
    )
    if lower > upper:
        raise ValueError("credal_interval_inverted")
    central_raw = value.get("central_estimate")
    central: float | None
    if central_raw is None:
        central = None
    else:
        central = require_finite_number(
            central_raw, "central_estimate", minimum=lower, maximum=upper
        )
    conflict = require_finite_number(
        value.get("conflict_index", 0.0), "conflict_index", minimum=0.0, maximum=1.0
    )
    return {
        "lower_probability": lower,
        "upper_probability": upper,
        "central_estimate": central,
        "conflict_index": conflict,
        "ignorance_width": upper - lower,
    }


def normalize_uncertainty(value: Mapping[str, Any]) -> dict[str, float]:
    result: dict[str, float] = {}
    for key in DEFAULT_UNCERTAINTY:
        result[key] = require_finite_number(
            value.get(key), key, minimum=0.0, maximum=1.0
        )
    return result


def copy_non_authority() -> dict[str, bool]:
    return deepcopy(NON_AUTHORITY_FLAGS)


def copy_boundary() -> dict[str, bool]:
    return deepcopy(REQUIRED_BOUNDARY)
