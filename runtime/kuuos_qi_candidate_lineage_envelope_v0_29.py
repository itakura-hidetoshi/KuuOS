from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from runtime.kuuos_belief_os_types_v0_1 import sha


def make_envelope(record: Mapping[str, Any]) -> dict[str, Any]:
    body = deepcopy(dict(record))
    body.pop("qi_candidate_lineage_bound_report_digest", None)
    return {
        "body": body,
        "body_digest": sha(body),
    }


__all__ = ["make_envelope"]
