from __future__ import annotations

import hashlib
import json
import math
from copy import deepcopy
from typing import Any, Mapping, Sequence

VERSION = "kuuos_autonomous_mission_cycle_kernel_v0_21"
STATE_VERSION = "kuuos_autonomous_mission_cycle_state_v0_21"
EVENT_VERSION = "kuuos_autonomous_mission_cycle_event_v0_21"
APPLY_RESULT_VERSION = "kuuos_autonomous_mission_cycle_apply_result_v0_21"
STORE_COMMIT_VERSION = "kuuos_autonomous_mission_cycle_store_commit_v0_21"

PHASES = ("mission", "plan", "act", "observe", "verify", "learn", "replan")
NEXT_PHASE = {
    "mission": "plan",
    "plan": "act",
    "act": "observe",
    "observe": "verify",
    "verify": "learn",
    "learn": "replan",
    "replan": "plan",
}
ARTIFACT_KIND = {
    "mission": "mission_contract",
    "plan": "plan",
    "act": "action_receipt",
    "observe": "observation",
    "verify": "verification",
    "learn": "learning",
    "replan": "replan",
}
VERIFICATION_VERDICTS = frozenset({"passed", "failed", "indeterminate"})

NON_AUTHORITY_FLAGS = {
    "grants_execution_authority": False,
    "grants_tool_authority": False,
    "grants_network_authority": False,
    "grants_shell_authority": False,
    "grants_truth_authority": False,
    "grants_final_commitment_authority": False,
    "grants_memory_overwrite_authority": False,
    "grants_clinical_authority": False,
    "grants_theorem_authority": False,
    "grants_self_modification_authority": False,
}

REQUIRED_BOUNDARY = {
    "mission_contract_is_source_authority": True,
    "phase_order_is_strict": True,
    "act_requires_lower_authority_receipts": True,
    "observe_does_not_rewrite_action": True,
    "verify_does_not_grant_truth_authority": True,
    "learning_is_future_only": True,
    "replan_is_append_only": True,
    "replay_is_idempotent": True,
    "snapshot_is_derived_from_append_only_ledger": True,
    "lower_execution_authority_preserved": True,
    "foreground_user_control_preserved": True,
    "graph_semantics_forbidden": True,
}


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def digest_without(value: Mapping[str, Any], field: str) -> str:
    result = dict(value)
    result.pop(field, None)
    return sha(result)


def state_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "mission_cycle_state_digest")


def event_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "mission_cycle_event_digest")


def apply_result_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "mission_cycle_apply_result_digest")


def store_commit_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "mission_cycle_store_commit_digest")


def require_nonempty_string(value: Any, name: str) -> str:
    text = str(value).strip()
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


def require_finite_number(value: Any, name: str, *, minimum: float | None = None) -> float:
    try:
        result = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{name}_invalid") from exc
    if not math.isfinite(result):
        raise ValueError(f"{name}_not_finite")
    if minimum is not None and result < minimum:
        raise ValueError(f"{name}_below_minimum")
    return result


def require_unique_strings(
    values: Sequence[Any], name: str, *, allow_empty: bool = True
) -> list[str]:
    normalized = [require_nonempty_string(item, name) for item in values]
    if not allow_empty and not normalized:
        raise ValueError(f"{name}_missing")
    if len(normalized) != len(set(normalized)):
        raise ValueError(f"{name}_duplicate")
    return normalized


def empty_artifact_digests(*, mission_contract_digest: str) -> dict[str, str]:
    result = {phase: "" for phase in PHASES}
    result["mission"] = require_nonempty_string(
        mission_contract_digest, "mission_contract_digest"
    )
    return result


def copy_non_authority() -> dict[str, bool]:
    return deepcopy(NON_AUTHORITY_FLAGS)
