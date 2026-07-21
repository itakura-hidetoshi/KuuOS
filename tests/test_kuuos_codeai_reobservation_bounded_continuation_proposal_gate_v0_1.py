from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import unittest

from runtime.kuuos_codeai_reobservation_bounded_continuation_proposal_gate_v0_1 import *
from scripts.build_codeai_reobservation_bounded_continuation_proposal_gate_fixture_v0_1 import (
    PREDECESSOR_GATE_MANIFEST_DIGEST,
    build_reference_fixture,
    deep_reference_fixture,
)
from scripts.project_codeai_reobservation_bounded_continuation_proposal_gate_fixture_v0_1 import project_fixture


class ReobservationBoundedContinuationProposalGateV01Tests(unittest.TestCase):
    def fixture(self) -> dict:
        return deep_reference_fixture()

    def build(self, fixture: dict):
        return build_codeai_reobservation_bounded_continuation_proposal_gate(
            request=fixture["request"],
            policy=fixture["policy"],
            predecessor_gate=fixture["predecessor_gate"],
            continuation_proposal=fixture["continuation_proposal"],
        )

    def reseal(self, fixture: dict, name: str) -> None:
        field = {
            "request": REQUEST_DIGEST_FIELD,
            "policy": POLICY_DIGEST_FIELD,
            "continuation_proposal": PROPOSAL_DIGEST_FIELD,
        }[name]
        fixture[name] = seal(fixture[name], field)

    def update_binding(self, fixture: dict, field: str, value) -> None:
        fixture["request"][field] = value
        fixture["policy"]["expected_" + field] = value
        fixture["continuation_proposal"][field] = value
        self.reseal(fixture, "request")
        self.reseal(fixture, "policy")
        self.reseal(fixture, "continuation_proposal")

    def mutate_predecessor_and_rebind(self, fixture: dict, field: str, value) -> None:
        fixture["predecessor_gate"][field] = value
        digest = canonical_digest(fixture["predecessor_gate"])
        self.update_binding(fixture, "predecessor_gate_manifest_digest", digest)

    def test_reference_is_admitted(self) -> None:
        fixture = self.fixture()
        result = self.build(fixture)
        self.assertEqual(result.status, STATUS_READY)
        self.assertEqual(result.issues, ())
        self.assertIsNotNone(result.gate_pack)
        assert result.gate_pack is not None
        self.assertEqual(result.gate_pack["gate_decision"], DECISION_ADMIT)
        self.assertEqual(result.gate_pack["hold_reasons"], [])

    def test_reference_exact_lineage(self) -> None:
        fixture = self.fixture()
        self.assertEqual(
            fixture["request"]["source_commit_sha"],
            "2944084ee7d415993f35c2bb8551c4fe83ee443d",
        )
        self.assertEqual(
            fixture["request"]["predecessor_gate_manifest_digest"],
            PREDECESSOR_GATE_MANIFEST_DIGEST,
        )
        self.assertEqual(
            PREDECESSOR_GATE_MANIFEST_DIGEST,
            "c24224d427dca0529e9a4aaee1e69da44c95800fc99f763e15500f53f7f0104d",
        )

    def test_reference_residual_budget_is_derived(self) -> None:
        pack = self.fixture()["gate_pack"]
        self.assertEqual(pack["residual_steps_before"], 2)
        self.assertEqual(pack["residual_tool_calls_before"], 3)
        self.assertEqual(pack["residual_model_calls_before"], 2)
        self.assertEqual(pack["residual_token_units_before"], 14000)
        self.assertEqual(pack["residual_wall_clock_ms_before"], 420000)
        self.assertEqual(pack["residual_failed_actions_before"], 0)
        self.assertEqual(pack["residual_token_units_if_executed"], 7000)

    def test_projection_matches_committed_artifacts(self) -> None:
        projection = project_fixture(self.fixture())
        root = Path(__file__).resolve().parents[1]
        example = json.loads((root / "examples/codeai_reobservation_bounded_continuation_proposal_gate_v0_1.json").read_text())
        manifest = json.loads((root / "manifests/kuuos_codeai_reobservation_bounded_continuation_proposal_gate_v0_1.json").read_text())
        self.assertEqual(projection, example)
        self.assertEqual(projection, manifest)

    def test_digests_are_deterministic(self) -> None:
        first = build_reference_fixture()
        second = build_reference_fixture()
        self.assertEqual(first["request"][REQUEST_DIGEST_FIELD], second["request"][REQUEST_DIGEST_FIELD])
        self.assertEqual(first["policy"][POLICY_DIGEST_FIELD], second["policy"][POLICY_DIGEST_FIELD])
        self.assertEqual(
            first["continuation_proposal"][PROPOSAL_DIGEST_FIELD],
            second["continuation_proposal"][PROPOSAL_DIGEST_FIELD],
        )
        self.assertEqual(first["gate_pack"][PACK_DIGEST_FIELD], second["gate_pack"][PACK_DIGEST_FIELD])
        self.assertEqual(first["receipt"][RECEIPT_DIGEST_FIELD], second["receipt"][RECEIPT_DIGEST_FIELD])

    def test_non_mapping_blocks(self) -> None:
        fixture = self.fixture()
        result = build_codeai_reobservation_bounded_continuation_proposal_gate(
            request=None,
            policy=fixture["policy"],
            predecessor_gate=fixture["predecessor_gate"],
            continuation_proposal=fixture["continuation_proposal"],
        )
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn("input_not_mapping", result.issues)

    def test_request_tamper_blocks(self) -> None:
        fixture = self.fixture()
        fixture["request"]["requested_continuation_round"] = 2
        result = self.build(fixture)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn("request_digest_mismatch", result.issues)

    def test_request_extra_field_blocks(self) -> None:
        fixture = self.fixture()
        fixture["request"]["extra"] = True
        result = self.build(fixture)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertTrue(any(item.startswith("request_extra_fields:") for item in result.issues))

    def test_binding_mismatch_blocks(self) -> None:
        fixture = self.fixture()
        fixture["continuation_proposal"]["source_commit_sha"] = "0" * 40
        self.reseal(fixture, "continuation_proposal")
        result = self.build(fixture)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn("proposal_binding_mismatch:source_commit_sha", result.issues)

    def test_stale_request_blocks(self) -> None:
        fixture = self.fixture()
        fixture["request"]["request_created_epoch"] = 1
        self.reseal(fixture, "request")
        result = self.build(fixture)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn("request_window_invalid", result.issues)

    def test_stale_proposal_blocks(self) -> None:
        fixture = self.fixture()
        fixture["continuation_proposal"]["proposal_created_epoch"] = 1
        self.reseal(fixture, "continuation_proposal")
        result = self.build(fixture)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn("proposal_window_invalid", result.issues)

    def test_predecessor_manifest_tamper_blocks(self) -> None:
        fixture = self.fixture()
        fixture["predecessor_gate"]["token_units"] += 1
        result = self.build(fixture)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn("predecessor_manifest_digest_mismatch", result.issues)

    def test_predecessor_pack_mismatch_blocks(self) -> None:
        fixture = self.fixture()
        self.update_binding(fixture, "predecessor_gate_pack_digest", "0" * 64)
        result = self.build(fixture)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn("predecessor_pack_digest_mismatch", result.issues)

    def test_predecessor_held_produces_hold(self) -> None:
        fixture = self.fixture()
        self.mutate_predecessor_and_rebind(fixture, "gate_decision", "progress_efficiency_held")
        fixture["predecessor_gate"]["hold_reasons"] = ["livelock_cycle_detected"]
        self.update_binding(
            fixture,
            "predecessor_gate_manifest_digest",
            canonical_digest(fixture["predecessor_gate"]),
        )
        result = self.build(fixture)
        self.assertEqual(result.status, STATUS_READY)
        assert result.gate_pack is not None
        self.assertEqual(result.gate_pack["gate_decision"], DECISION_HOLD)
        self.assertIn("predecessor_progress_efficiency_not_admitted", result.gate_pack["hold_reasons"])

    def test_predecessor_hint_boundary_missing_holds(self) -> None:
        fixture = self.fixture()
        self.mutate_predecessor_and_rebind(fixture, "continuation_hint_only", False)
        result = self.build(fixture)
        self.assertEqual(result.status, STATUS_READY)
        assert result.gate_pack is not None
        self.assertIn("predecessor_hint_boundary_missing", result.gate_pack["hold_reasons"])

    def test_multiple_actions_hold(self) -> None:
        fixture = self.fixture()
        fixture["continuation_proposal"]["action_count"] = 2
        self.reseal(fixture, "continuation_proposal")
        result = self.build(fixture)
        self.assertEqual(result.status, STATUS_READY)
        assert result.gate_pack is not None
        self.assertIn("proposal_not_exactly_one_action", result.gate_pack["hold_reasons"])

    def test_mutating_action_holds(self) -> None:
        fixture = self.fixture()
        fixture["continuation_proposal"]["read_only_action"] = False
        self.reseal(fixture, "continuation_proposal")
        result = self.build(fixture)
        assert result.gate_pack is not None
        self.assertIn("proposal_action_not_read_only", result.gate_pack["hold_reasons"])

    def test_missing_observable_return_holds(self) -> None:
        fixture = self.fixture()
        fixture["continuation_proposal"]["observable_return_required"] = False
        self.reseal(fixture, "continuation_proposal")
        result = self.build(fixture)
        assert result.gate_pack is not None
        self.assertIn("proposal_observable_return_missing", result.gate_pack["hold_reasons"])

    def test_missing_checkpoint_holds(self) -> None:
        fixture = self.fixture()
        fixture["continuation_proposal"]["new_checkpoint_required"] = False
        self.reseal(fixture, "continuation_proposal")
        result = self.build(fixture)
        assert result.gate_pack is not None
        self.assertIn("proposal_new_checkpoint_missing", result.gate_pack["hold_reasons"])

    def test_missing_gate_reentry_holds(self) -> None:
        fixture = self.fixture()
        fixture["continuation_proposal"]["predecessor_gate_reentry_required"] = False
        self.reseal(fixture, "continuation_proposal")
        result = self.build(fixture)
        assert result.gate_pack is not None
        self.assertIn("proposal_predecessor_gate_reentry_missing", result.gate_pack["hold_reasons"])

    def test_self_report_only_holds(self) -> None:
        fixture = self.fixture()
        fixture["continuation_proposal"]["self_report_only"] = True
        self.reseal(fixture, "continuation_proposal")
        result = self.build(fixture)
        assert result.gate_pack is not None
        self.assertIn("proposal_self_report_only", result.gate_pack["hold_reasons"])

    def test_disallowed_action_kind_holds(self) -> None:
        fixture = self.fixture()
        fixture["policy"]["allowed_action_kinds"] = ["observe_repository"]
        self.reseal(fixture, "policy")
        result = self.build(fixture)
        assert result.gate_pack is not None
        self.assertIn("proposal_action_kind_not_allowed", result.gate_pack["hold_reasons"])

    def test_token_residual_excess_holds(self) -> None:
        fixture = self.fixture()
        fixture["continuation_proposal"]["requested_token_units"] = 15000
        self.reseal(fixture, "continuation_proposal")
        result = self.build(fixture)
        assert result.gate_pack is not None
        self.assertIn("residual_budget_insufficient:token_units", result.gate_pack["hold_reasons"])

    def test_total_budget_already_exhausted_holds(self) -> None:
        fixture = self.fixture()
        fixture["policy"]["maximum_total_steps"] = 5
        self.reseal(fixture, "policy")
        result = self.build(fixture)
        assert result.gate_pack is not None
        self.assertIn("residual_budget_already_exhausted:steps", result.gate_pack["hold_reasons"])

    def test_request_authority_claim_blocks(self) -> None:
        fixture = self.fixture()
        fixture["request"]["claims_execution_authority"] = True
        self.reseal(fixture, "request")
        result = self.build(fixture)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn("request_claims_authority_or_correctness", result.issues)

    def test_proposal_authority_claim_holds(self) -> None:
        fixture = self.fixture()
        fixture["continuation_proposal"]["claims_execution_authority"] = True
        self.reseal(fixture, "continuation_proposal")
        result = self.build(fixture)
        assert result.gate_pack is not None
        self.assertIn(
            "proposal_forbidden_claim:claims_execution_authority",
            result.gate_pack["hold_reasons"],
        )

    def test_receipt_preserves_non_authority(self) -> None:
        receipt = self.fixture()["receipt"]
        self.assertTrue(receipt["proposal_hint_only"])
        self.assertFalse(receipt["budget_reserved"])
        self.assertFalse(receipt["budget_consumed"])
        self.assertFalse(receipt["continuation_authority_granted"])
        self.assertFalse(receipt["execution_authority_granted"])
        self.assertFalse(receipt["repository_mutation_performed"])
        self.assertFalse(receipt["git_authority_granted"])
        self.assertFalse(receipt["correctness_claimed"])

    def test_pack_does_not_execute_or_select(self) -> None:
        pack = self.fixture()["gate_pack"]
        self.assertFalse(pack["action_executed"])
        self.assertFalse(pack["specialist_dispatched"])
        self.assertFalse(pack["candidate_selected"])
        self.assertFalse(pack["budget_reserved"])
        self.assertFalse(pack["budget_consumed"])


if __name__ == "__main__":
    unittest.main()
