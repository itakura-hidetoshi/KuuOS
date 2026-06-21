from __future__ import annotations

import unittest
from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory

from runtime.kuuos_belief_os_types_v0_1 import sha
from runtime.kuuos_event_wakeup_control_resource_kernel_v0_25 import (
    build_control_command,
    build_resource_envelope,
    build_trigger_event,
    validate_control_command,
    validate_resource_envelope,
    validate_trigger_event,
)
from runtime.kuuos_event_wakeup_control_resource_scenarios_v0_25 import (
    run_event_wakeup_control_resource_scenarios,
)


def resources(value: int) -> dict[str, int]:
    return {
        "tokens": value,
        "api_calls": value,
        "cost_microunits": value,
        "storage_bytes": value,
        "worker_millis": value,
    }


class EventWakeupControlResourceV025Tests(unittest.TestCase):
    def test_full_scenarios(self) -> None:
        result = run_event_wakeup_control_resource_scenarios()
        self.assertEqual(
            "KUUOS_EVENT_WAKEUP_CONTROL_RESOURCE_V0_25_OK",
            result["status"],
        )
        self.assertEqual("WAKEUP_PROPOSED", result["admitted_route"])
        self.assertEqual("WAKEUP_DEGRADED", result["degraded_route"])
        self.assertEqual("standard", result["degraded_model_tier"])
        self.assertEqual("WAKEUP_PROPOSED", result["pause_resume_route"])
        self.assertEqual("WAKEUP_PROPOSED", result["renewal_resume_route"])
        self.assertEqual("WAKEUP_BLOCKED_CANCELLED", result["cancelled_route"])
        self.assertEqual("REJECTED", result["stale_status"])
        self.assertTrue(result["foreground_control_available"])
        self.assertFalse(result["hidden_daemon_started"])
        self.assertFalse(result["queue_is_running"])
        self.assertFalse(result["execution_authority_granted"])

    def test_trigger_never_grants_authority(self) -> None:
        trigger = build_trigger_event(
            trigger_id="test-trigger",
            trigger_class="monitoring_condition",
            source_id="monitor",
            source_event_digest=sha("source"),
            mission_id="mission",
            condition_digest=sha("condition"),
            condition_satisfied=True,
            requested_resources=resources(1),
            requested_model_tier="small",
            cycle_duration_ms=1,
            due_at_ms=1,
            observed_at_ms=1,
        )
        self.assertEqual([], validate_trigger_event(trigger))
        self.assertTrue(trigger["external_trigger_surface"])
        self.assertFalse(trigger["hidden_daemon_invocation"])
        self.assertFalse(trigger["trigger_grants_execution_authority"])

    def test_read_only_control_command(self) -> None:
        command = build_control_command(
            command_id="inspect-command",
            command="inspect",
            mission_id="mission",
            principal_id="user",
            principal_authority_digest=sha("authority"),
            expected_state_digest=sha("state"),
            reason_digest=sha("reason"),
            payload={},
            mission_control_authority=False,
            permission_authority=False,
            budget_authority=False,
            issued_at_ms=1,
        )
        self.assertEqual([], validate_control_command(command))
        self.assertTrue(command["read_only"])
        self.assertFalse(command["direct_execution"])
        self.assertFalse(command["direct_plan_activation"])
        self.assertFalse(command["direct_world_rewrite"])

    def test_resource_envelope_is_finite(self) -> None:
        envelope = build_resource_envelope(
            envelope_id="envelope",
            mission_id="mission",
            authorized_by_digest=sha("authority"),
            allowed_model_tiers=["small", "standard"],
            preferred_model_tier="standard",
            governance_caps=resources(100),
            hard_limits=resources(80),
            reserve_floors=resources(10),
            remaining=resources(60),
            max_cycles=5,
            remaining_cycles=3,
            renewable=True,
            expires_at_ms=100,
        )
        self.assertEqual([], validate_resource_envelope(envelope))
        self.assertTrue(envelope["finite_envelope"])
        self.assertFalse(envelope["self_increase_allowed"])
        self.assertFalse(envelope["model_self_escalation_allowed"])

        tampered = deepcopy(envelope)
        tampered["self_increase_allowed"] = True
        self.assertIn(
            "resource_self_increase_forbidden",
            validate_resource_envelope(tampered),
        )

    def test_budget_cannot_exceed_governance_cap(self) -> None:
        with self.assertRaisesRegex(
            ValueError, "resource_tokens_limit_above_governance_cap"
        ):
            build_resource_envelope(
                envelope_id="invalid-envelope",
                mission_id="mission",
                authorized_by_digest=sha("authority"),
                allowed_model_tiers=["small"],
                preferred_model_tier="small",
                governance_caps=resources(10),
                hard_limits={**resources(10), "tokens": 11},
                reserve_floors=resources(1),
                remaining=resources(10),
                max_cycles=1,
                remaining_cycles=1,
                renewable=False,
                expires_at_ms=1,
            )


if __name__ == "__main__":
    unittest.main()
