#!/usr/bin/env python3
from __future__ import annotations

from typing import Any, Mapping

from runtime.kuuos_runtime_daemon_physical_quantum_qi_v12_5_to_v12_6_transition_executor_bridge_v13_9 import (
    build_physical_quantum_qi_v12_5_to_v12_6_transition_executor_bridge,
)


def build_physical_quantum_qi_v13_22_receipt_link(
    *,
    runtime_context: Mapping[str, Any],
    receipt_link_license: Mapping[str, Any],
):
    return build_physical_quantum_qi_v12_5_to_v12_6_transition_executor_bridge(
        runtime_context=runtime_context,
        v12_5_to_v12_6_transition_executor_bridge_license=receipt_link_license,
    )
