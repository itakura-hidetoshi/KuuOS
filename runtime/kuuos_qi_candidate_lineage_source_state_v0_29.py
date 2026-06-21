from __future__ import annotations

from typing import Any, Mapping

from runtime.kuuos_integrated_long_duration_operation_types_v0_27 import (
    STATE_VERSION,
    state_digest,
)
from runtime.kuuos_qi_candidate_lineage_types_v0_29 import (
    require_nonnegative_int,
    require_string,
)


def validate_source_state(state: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    try:
        if state.get("version") != STATE_VERSION:
            errors.append("source_v027_state_version_invalid")
        for field in ("mission_id", "lineage_id", "latest_checkpoint_digest"):
            require_string(state.get(field), f"source_v027_{field}")
        require_nonnegative_int(state.get("cycle_index"), "source_v027_cycle_index")
        require_string(state.get("mode"), "source_v027_mode")
        if state.get("integrated_operation_state_digest") != state_digest(state):
            errors.append("source_v027_state_digest_invalid")
    except (TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors


__all__ = ["validate_source_state"]
