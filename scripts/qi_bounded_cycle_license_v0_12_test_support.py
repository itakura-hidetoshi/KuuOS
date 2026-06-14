#!/usr/bin/env python3
from __future__ import annotations

from typing import Any

from scripts.qi_action_v0_9_test_support import execution_license
from scripts.qi_child_feedback_cycle_v0_10_test_support import bridge_license
from scripts.qi_parent_cycle_reentry_v0_11_test_support import loop_license
from scripts.qi_recovery_action_v0_8_test_support import action_license


def _without_bound(value: dict[str, Any], field: str) -> dict[str, Any]:
    result = dict(value)
    result.pop(field, None)
    return result


def cycle_license(
    plan: dict[str, Any],
    source: dict[str, Any],
    **overrides: Any,
) -> dict[str, Any]:
    v08 = _without_bound(
        action_license({"action_plan_digest": "TEMPLATE"}),
        "bound_action_plan_digest",
    )
    v09 = _without_bound(
        execution_license(
            {
                "execution_plan_digest": "TEMPLATE",
                "selected_action_kind": plan["selected_action_kind"],
            },
            source["causal"],
        ),
        "bound_execution_plan_digest",
    )
    v10 = _without_bound(
        bridge_license({"bridge_plan_digest": "TEMPLATE"}),
        "bound_bridge_plan_digest",
    )
    v11 = _without_bound(
        loop_license({"loop_plan_digest": "TEMPLATE"}),
        "bound_loop_plan_digest",
    )
    value = {
        "license_status": "INDRA_QI_BOUNDED_GENERATIONAL_CYCLE_V0_12_LICENSE_READY",
        "bound_cycle_plan_digest": plan["cycle_plan_digest"],
        "source_v0_11_read_allowed": True,
        "runner_state_read_allowed": True,
        "transaction_snapshot_allowed": True,
        "transaction_restore_allowed": True,
        "v0_8_invoke_allowed": True,
        "v0_9_invoke_allowed": True,
        "v0_10_invoke_allowed": True,
        "v0_11_invoke_allowed": True,
        "state_write_allowed": True,
        "handoff_write_allowed": True,
        "record_write_allowed": True,
        "ledger_append_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
        "v0_8_license_template": v08,
        "v0_9_license_template": v09,
        "v0_10_license_template": v10,
        "v0_11_license_template": v11,
    }
    value.update(overrides)
    return value
