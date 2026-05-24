import unittest

from runtime.kuuos_runtime_daemon_qi_reentry_chain_controller_v0_1 import (
    decide_qi_reentry_chain_controller,
)


def health(*, score=0.8, action="invoke_manual_runner", status="RECOVERABLE_BY_MANUAL_RUNNER", unsafe=False, allowed=True):
    return {
        "daemon_health_status": "HEALTHY_REENTRY_READY" if action == "invoke_manual_runner" else "REOBSERVE_REQUIRED",
        "next_operator_action": action,
        "recoverability_status": status,
        "recoverability_score": score,
        "recovery_unsafe": unsafe,
        "local_recovery_allowed": allowed,
    }


class QiReentryChainControllerTests(unittest.TestCase):
    def test_missing_health_projection_disallows_chain(self):
        decision = decide_qi_reentry_chain_controller(health_projection=None, requested_max_cycles=2)
        self.assertEqual(decision.controller_decision, "CHAIN_NOT_ALLOWED")
        self.assertEqual(decision.controller_reason, "health_projection_missing")
        self.assertEqual(decision.allowed_max_cycles, 0)
        self.assertFalse(decision.chain_invocation_allowed)
        self.assertFalse(decision.grants_execution_authority)

    def test_stable_recoverability_allows_at_most_three_cycles(self):
        decision = decide_qi_reentry_chain_controller(
            health_projection=health(score=0.95),
            requested_max_cycles=5,
        )
        self.assertEqual(decision.controller_decision, "CHAIN_ALLOWED_STABLE")
        self.assertEqual(decision.allowed_max_cycles, 3)
        self.assertTrue(decision.chain_invocation_allowed)

    def test_bounded_recoverability_allows_at_most_two_cycles(self):
        decision = decide_qi_reentry_chain_controller(
            health_projection=health(score=0.75),
            requested_max_cycles=5,
        )
        self.assertEqual(decision.controller_decision, "CHAIN_ALLOWED_BOUNDED")
        self.assertEqual(decision.allowed_max_cycles, 2)

    def test_fragile_recoverability_allows_single_step_only(self):
        decision = decide_qi_reentry_chain_controller(
            health_projection=health(score=0.4),
            requested_max_cycles=5,
        )
        self.assertEqual(decision.controller_decision, "CHAIN_ALLOWED_SINGLE_STEP")
        self.assertEqual(decision.allowed_max_cycles, 1)

    def test_requested_cycles_are_clamped_to_five(self):
        decision = decide_qi_reentry_chain_controller(
            health_projection=health(score=0.95),
            requested_max_cycles=100,
        )
        self.assertEqual(decision.requested_max_cycles, 5)
        self.assertEqual(decision.allowed_max_cycles, 3)

    def test_unsafe_recovery_disallows_chain(self):
        decision = decide_qi_reentry_chain_controller(
            health_projection=health(score=0.95, unsafe=True),
            requested_max_cycles=3,
        )
        self.assertEqual(decision.controller_decision, "CHAIN_NOT_ALLOWED")
        self.assertEqual(decision.controller_reason, "recovery_unsafe")
        self.assertEqual(decision.allowed_max_cycles, 0)

    def test_non_manual_action_disallows_chain(self):
        decision = decide_qi_reentry_chain_controller(
            health_projection=health(action="reobserve", status="RECOVERABLE_BY_REOBSERVATION"),
            requested_max_cycles=3,
        )
        self.assertEqual(decision.controller_decision, "CHAIN_NOT_ALLOWED")
        self.assertEqual(decision.controller_reason, "next_operator_action_not_invoke_manual_runner")
        self.assertEqual(decision.allowed_max_cycles, 0)

    def test_local_recovery_not_allowed_disallows_chain(self):
        decision = decide_qi_reentry_chain_controller(
            health_projection=health(allowed=False),
            requested_max_cycles=3,
        )
        self.assertEqual(decision.controller_decision, "CHAIN_NOT_ALLOWED")
        self.assertEqual(decision.controller_reason, "local_recovery_not_allowed")
        self.assertEqual(decision.allowed_max_cycles, 0)


if __name__ == "__main__":
    unittest.main()
