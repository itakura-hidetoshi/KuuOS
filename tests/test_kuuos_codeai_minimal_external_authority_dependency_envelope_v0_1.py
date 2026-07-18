from copy import deepcopy
import unittest

import runtime.kuuos_codeai_minimal_external_authority_dependency_envelope_v0_1 as m
from scripts.check_codeai_minimal_external_authority_dependency_envelope_v0_1 import (
    bind_effect,
    load_example,
    main as run_route_checker,
    reseal_request,
    reseal_policy,
    reseal_state,
    with_capability,
    with_external_success,
    with_failure,
    with_packet,
    without_internal_substitute,
)


class CodeAIMinimalExternalAuthorityDependencyEnvelopeV01Test(unittest.TestCase):
    def setUp(self):
        self.example = load_example()

    def build(self, **overrides):
        values = {
            "source_git_lifecycle_receipt": self.example[
                "source_git_lifecycle_receipt"
            ],
            "dependency_request": self.example["dependency_request"],
            "dependency_state": self.example["dependency_state"],
            "dependency_policy": self.example["dependency_policy"],
        }
        values.update(overrides)
        return m.build_codeai_minimal_external_authority_dependency_envelope(
            **values
        )

    def test_internal_substitute_is_preferred_over_external_dependency(self):
        receipt = self.build().receipt
        assert receipt is not None
        self.assertEqual(
            m.DISPOSITION_INTERNAL_SUBSTITUTE, receipt["codeai_disposition"]
        )
        self.assertTrue(receipt["internal_substitute_authority_granted"])
        self.assertFalse(receipt["external_effect_lease_issued"])
        self.assertFalse(receipt["critical_path_blocked"])

    def test_unaffected_internal_work_continues_before_request_packet(self):
        request = without_internal_substitute(
            self.example["dependency_request"], critical=False
        )
        receipt = self.build(dependency_request=request).receipt
        assert receipt is not None
        self.assertEqual(
            m.DISPOSITION_INTERNAL_CONTINUATION, receipt["codeai_disposition"]
        )
        self.assertTrue(receipt["internal_continuation_authority_granted"])
        self.assertTrue(receipt["unaffected_work_may_continue"])

    def test_deploy_requires_matching_short_lived_one_shot_capability(self):
        request = without_internal_substitute(self.example["dependency_request"])
        state = with_capability(
            self.example["dependency_state"], request, kind=m.KIND_DEPLOY
        )
        receipt = self.build(
            dependency_request=request, dependency_state=state
        ).receipt
        assert receipt is not None
        self.assertEqual(
            m.DISPOSITION_DEPLOY_AUTHORIZED, receipt["codeai_disposition"]
        )
        self.assertTrue(receipt["deployment_authority_granted"])
        self.assertTrue(receipt["external_effect_lease_issued"])
        self.assertFalse(receipt["capability_handle_exposed"])

    def test_secret_mutation_uses_opaque_broker_without_secret_access(self):
        request, state = bind_effect(
            self.example["dependency_request"],
            self.example["dependency_state"],
            kind=m.KIND_SECRET_MUTATION,
            target="ci-signing-key",
            action="rotate_version",
        )
        request = without_internal_substitute(request)
        state = with_capability(
            state, request, kind=m.KIND_SECRET_MUTATION
        )
        receipt = self.build(
            dependency_request=request, dependency_state=state
        ).receipt
        assert receipt is not None
        self.assertEqual(
            m.DISPOSITION_SECRET_MUTATION_AUTHORIZED,
            receipt["codeai_disposition"],
        )
        self.assertTrue(receipt["secret_mutation_authority_granted"])
        self.assertFalse(receipt["secret_access_authority_granted"])
        self.assertFalse(receipt["plaintext_secret_observed"])

    def test_expired_capability_falls_back_to_minimal_packet(self):
        request = without_internal_substitute(self.example["dependency_request"])
        state = with_capability(
            self.example["dependency_state"],
            request,
            kind=m.KIND_DEPLOY,
            expires_epoch=7000,
        )
        receipt = self.build(
            dependency_request=request, dependency_state=state
        ).receipt
        assert receipt is not None
        self.assertEqual(
            m.DISPOSITION_PACKET_AUTHORIZED, receipt["codeai_disposition"]
        )
        self.assertFalse(receipt["deployment_authority_granted"])
        self.assertTrue(receipt["external_request_packet_authority_granted"])

    def test_human_handover_is_last_resort_packet_then_nonblocking_hold(self):
        request, state = bind_effect(
            self.example["dependency_request"],
            self.example["dependency_state"],
            kind=m.KIND_HUMAN_HANDOVER,
            target="human-authority",
            action="approve_nondelegable_decision",
        )
        request = without_internal_substitute(request)
        packet = self.build(
            dependency_request=request, dependency_state=state
        ).receipt
        assert packet is not None
        self.assertEqual(
            m.DISPOSITION_PACKET_AUTHORIZED, packet["codeai_disposition"]
        )
        self.assertTrue(packet["human_handover_deferred"])
        self.assertFalse(packet["human_handover_authority_granted"])
        hold = self.build(
            dependency_request=request, dependency_state=with_packet(state)
        ).receipt
        assert hold is not None
        self.assertEqual(m.DISPOSITION_PENDING_HOLD, hold["codeai_disposition"])
        self.assertFalse(hold["execution_lease_issued"])
        self.assertTrue(hold["critical_path_blocked"])

    def test_plaintext_secret_request_is_rejected(self):
        request = deepcopy(self.example["dependency_request"])
        request["plaintext_secret_requested"] = True
        request = reseal_request(request)
        receipt = self.build(dependency_request=request).receipt
        assert receipt is not None
        self.assertEqual(
            m.DISPOSITION_PLAINTEXT_SECRET_REJECTED,
            receipt["codeai_disposition"],
        )
        self.assertFalse(receipt["execution_lease_issued"])

    def test_unauthorized_executor_cannot_receive_any_lease(self):
        request = deepcopy(self.example["dependency_request"])
        state = deepcopy(self.example["dependency_state"])
        request["executor_id"] = "unowned-executor"
        state["executor_id"] = "unowned-executor"
        receipt = self.build(
            dependency_request=reseal_request(request),
            dependency_state=reseal_state(state),
        ).receipt
        assert receipt is not None
        self.assertEqual(
            m.DISPOSITION_PROVENANCE_REPAIR, receipt["codeai_disposition"]
        )
        self.assertFalse(receipt["execution_lease_issued"])

    def test_policy_cannot_enable_blocking_handover(self):
        policy = deepcopy(self.example["dependency_policy"])
        policy["allow_blocking_handover"] = True
        receipt = self.build(dependency_policy=reseal_policy(policy)).receipt
        assert receipt is not None
        self.assertEqual(
            m.DISPOSITION_SCOPE_ABSTAINED, receipt["codeai_disposition"]
        )
        self.assertFalse(receipt["execution_lease_issued"])

    def test_failure_degrades_without_new_external_effect_authority(self):
        request = without_internal_substitute(self.example["dependency_request"])
        receipt = self.build(
            dependency_request=request,
            dependency_state=with_failure(self.example["dependency_state"]),
        ).receipt
        assert receipt is not None
        self.assertEqual(
            m.DISPOSITION_FAILED_DEGRADED, receipt["codeai_disposition"]
        )
        self.assertEqual(m.MODE_DEGRADED, receipt["operating_mode"])
        self.assertFalse(receipt["external_effect_lease_issued"])

    def test_observed_external_result_completes_without_new_lease(self):
        request = without_internal_substitute(self.example["dependency_request"])
        state = with_external_success(
            self.example["dependency_state"], deploy=True
        )
        receipt = self.build(
            dependency_request=request, dependency_state=state
        ).receipt
        assert receipt is not None
        self.assertEqual(m.DISPOSITION_COMPLETED, receipt["codeai_disposition"])
        self.assertFalse(receipt["execution_lease_issued"])
        self.assertFalse(receipt["active_now"])
        self.assertFalse(receipt["external_result_treated_as_truth"])

    def test_tampered_state_fails_closed(self):
        state = deepcopy(self.example["dependency_state"])
        state["observed_at_epoch"] += 1
        result = self.build(dependency_state=state)
        self.assertEqual(m.STATUS_BLOCKED, result.status)
        self.assertIsNone(result.receipt)
        self.assertIn("external_dependency_state_digest_mismatch", result.issues)

    def test_all_disposition_routes(self):
        run_route_checker()


if __name__ == "__main__":
    unittest.main()
