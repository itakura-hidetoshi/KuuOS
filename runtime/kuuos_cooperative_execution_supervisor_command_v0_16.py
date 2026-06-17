from __future__ import annotations

from typing import Any, Mapping


def build_supervisor_command(*, job_id: str, command_id: str, action: str, payload: Mapping[str, Any], source_job_state_digest: str) -> dict[str, Any]:
    return {}
