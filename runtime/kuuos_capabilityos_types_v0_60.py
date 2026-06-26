from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from typing import Any, Mapping, Sequence

VERSION = "kuuos_capabilityos_qi_world_kernel_v0_60"
DEFINITION_VERSION = "kuuos_capability_definition_v0_60"
CANDIDATE_VERSION = "kuuos_capability_candidate_v0_60"
PATH_VERSION = "kuuos_capability_path_candidate_v0_60"
STATUS_OK = "KUUOS_CAPABILITYOS_QI_WORLD_KERNEL_V0_60_OK"

GUARD_ORDER = (
    "present_activation_blocker",
    "execution_authority_blocker",
    "memory_overwrite_blocker",
    "world_identity_blocker",
    "truth_authority_blocker",
    "same_cycle_self_loop_blocker",
    "multi_world_collapse_blocker",
)
IMPEDIMENT_ORDER = (
    "missing_input", "stale_world_state", "representation_mismatch",
    "tool_unavailable", "resource_insufficient", "verifier_unavailable",
    "distribution_shift", "unresolved_contradiction", "unsafe_side_effect",
    "causal_model_insufficient", "capability_saturation",
)
READY = {"READY_FOR_PLANOS", "READY_WITH_WORLD_PLURALITY"}
DISPOSITIONS = READY | {
    "DECOMPOSE_CAPABILITY", "SUBSTITUTE_CAPABILITY", "REOBSERVE_PROCESS",
    "REOBSERVE_WORLD_PRECONDITION", "REVIEW_CONTRADICTION",
    "CONTAIN_YANG_SATURATION", "QUARANTINE_GUARD_EVIDENCE",
    "HOLD_NO_VERIFIER", "UNAVAILABLE_IN_CURRENT_WORLD",
}
NON_AUTHORITY = {
    "grants_plan_activation": False,
    "grants_execution_authority": False,
    "grants_tool_authority": False,
    "grants_truth_authority": False,
    "grants_causal_authority": False,
    "grants_world_commit": False,
    "grants_blocker_discharge": False,
    "grants_memory_overwrite_authority": False,
    "grants_automatic_learning_authority": False,
    "grants_final_commitment_authority": False,
}
BOUNDARY = {
    "capability_is_contextual_not_intrinsic": True,
    "qi_support_is_not_truth": True,
    "yin_guard_is_not_execution_license": True,
    "impediment_is_not_protective_guard": True,
    "world_candidate_is_not_exact_world": True,
    "world_imagination_does_not_mutate_world": True,
    "world_plurality_is_preserved": True,
    "memory_retrieval_is_not_plan_activation": True,
    "capability_disposition_is_not_plan_activation": True,
    "planos_owns_composition": True,
    "decisionos_owns_selection": True,
    "actos_owns_execution": True,
    "verifyos_owns_outcome_verification": True,
    "learning_is_future_only": True,
}


def _sha(value: Any) -> str:
    text = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(text.encode()).hexdigest()


def _digest(value: Mapping[str, Any], field: str) -> str:
    payload = deepcopy(dict(value))
    payload.pop(field, None)
    return _sha(payload)


def _text(value: Any, name: str) -> str:
    result = str(value).strip()
    if not result:
        raise ValueError(f"{name}_missing")
    return result


def _nat(value: Any, name: str, *, positive: bool = False) -> int:
    if isinstance(value, bool):
        raise ValueError(f"{name}_invalid")
    try:
        result = int(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{name}_invalid") from exc
    if result < 0 or (positive and result == 0):
        raise ValueError(f"{name}_out_of_range")
    return result


def _names(values: Sequence[Any], name: str) -> list[str]:
    if isinstance(values, (str, bytes, bytearray)):
        raise ValueError(f"{name}_invalid")
    result = [_text(item, name) for item in values]
    if len(result) != len(set(result)):
        raise ValueError(f"{name}_duplicate")
    return result


def _flags(value: Mapping[str, Any] | None, order: Sequence[str]) -> dict[str, bool]:
    raw = dict(value or {})
    return {name: raw.get(name) is True for name in order}


def build_capability_definition(
    *, capability_id: str, revision: int, provider_id: str, skill_digest: str,
    task_type: str, input_schema_digest: str, output_schema_digest: str,
    verifier_capability: str, max_cost: int, max_steps: int,
    max_duration_ms: int, required_capabilities: Sequence[str] = (),
    produced_capabilities: Sequence[str] = (), world_preconditions: Sequence[str] = (),
    required_tools: Sequence[str] = (), known_failure_modes: Sequence[str] = (),
) -> dict[str, Any]:
    packet = {
        "version": VERSION,
        "definition_version": DEFINITION_VERSION,
        "capability_id": _text(capability_id, "capability_id"),
        "revision": _nat(revision, "revision"),
        "provider_id": _text(provider_id, "provider_id"),
        "skill_digest": _text(skill_digest, "skill_digest"),
        "task_type": _text(task_type, "task_type"),
        "input_schema_digest": _text(input_schema_digest, "input_schema_digest"),
        "output_schema_digest": _text(output_schema_digest, "output_schema_digest"),
        "required_capabilities": _names(required_capabilities, "required_capabilities"),
        "produced_capabilities": _names(produced_capabilities, "produced_capabilities"),
        "world_preconditions": _names(world_preconditions, "world_preconditions"),
        "required_tools": _names(required_tools, "required_tools"),
        "verifier_capability": _text(verifier_capability, "verifier_capability"),
        "known_failure_modes": _names(known_failure_modes, "known_failure_modes"),
        "resource_envelope": {
            "max_cost": _nat(max_cost, "max_cost", positive=True),
            "max_steps": _nat(max_steps, "max_steps", positive=True),
            "max_duration_ms": _nat(max_duration_ms, "max_duration_ms", positive=True),
        },
        "candidate_only": True,
        "non_authority": deepcopy(NON_AUTHORITY),
        "boundary": deepcopy(BOUNDARY),
        "capability_definition_digest": "",
    }
    packet["capability_definition_digest"] = _digest(
        packet, "capability_definition_digest"
    )
    errors = validate_capability_definition(packet)
    if errors:
        raise ValueError(";".join(errors))
    return packet


def validate_capability_definition(packet: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    try:
        if packet.get("version") != VERSION or packet.get("definition_version") != DEFINITION_VERSION:
            errors.append("definition_version_invalid")
        for key in (
            "capability_id", "provider_id", "skill_digest", "task_type",
            "input_schema_digest", "output_schema_digest", "verifier_capability",
        ):
            _text(packet.get(key), key)
        _nat(packet.get("revision"), "revision")
        for key in (
            "required_capabilities", "produced_capabilities", "world_preconditions",
            "required_tools", "known_failure_modes",
        ):
            if not isinstance(packet.get(key), list):
                errors.append(f"{key}_invalid")
            else:
                _names(packet[key], key)
        resource = packet.get("resource_envelope")
        if not isinstance(resource, Mapping):
            errors.append("resource_envelope_invalid")
        else:
            for key in ("max_cost", "max_steps", "max_duration_ms"):
                _nat(resource.get(key), key, positive=True)
        if packet.get("candidate_only") is not True:
            errors.append("candidate_only_required")
        if dict(packet.get("non_authority", {})) != NON_AUTHORITY:
            errors.append("definition_authority_expansion")
        if dict(packet.get("boundary", {})) != BOUNDARY:
            errors.append("definition_boundary_invalid")
        if packet.get("capability_definition_digest") != _digest(
            packet, "capability_definition_digest"
        ):
            errors.append("definition_digest_invalid")
    except (TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors
