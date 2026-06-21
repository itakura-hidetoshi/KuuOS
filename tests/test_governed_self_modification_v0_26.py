from __future__ import annotations

import unittest
from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory

from runtime.kuuos_belief_os_types_v0_1 import sha
from runtime.kuuos_event_wakeup_control_resource_scenarios_v0_25 import (
    _admitted_and_replay,
)
from runtime.kuuos_governed_self_modification_kernel_v0_26 import (
    build_initial_state,
    build_self_modification_proposal,
    build_stage_evidence,
    validate_proposal,
    validate_state,
)
from runtime.kuuos_governed_self_modification_scenarios_v0_26 import (
    run_governed_self_modification_scenarios,
)


class GovernedSelfModificationV026Tests(unittest.TestCase):
    def test_full_scenarios(self) -> None:
        result = run_governed_self_modification_scenarios()
        self.assertEqual(
            "KUUOS_GOVERNED_SELF_MODIFICATION_V0_26_OK",
            result["status"],
        )
        self.assertEqual("DEPLOYMENT_CLOSED_SUCCESS", result["success_route"])
        self.assertEqual("ROLLED_BACK", result["rollback_route"])
        self.assertEqual(
            "REJECTED_PERMANENT_FORBIDDEN_ACTION", result["forbidden_route"]
        )
        self.assertEqual(
            "REJECTED_VALIDATION_FAILURE", result["regression_route"]
        )
        self.assertEqual(
            "EXTERNAL_APPROVAL_REQUIRED", result["approval_missing_route"]
        )
        self.assertEqual("REPLAYED", result["replay_status"])
        self.assertEqual("REJECTED", result["stale_status"])
        self.assertFalse(result["gate_modified_running_system"])
        self.assertFalse(result["authority_widened"])
        self.assertFalse(result["automatic_rollback"])
        self.assertFalse(result["execution_authority_granted"])

    def test_proposal_is_non_executing_and_append_only(self) -> None:
        with TemporaryDirectory() as directory:
            source = _admitted_and_replay(Path(directory) / "source")
            proposal = build_self_modification_proposal(
                proposal_id="proposal-boundary",
                source_v025_state=source,
                base_artifact_digest=sha("base"),
                candidate_artifact_digest=sha("candidate"),
                rollback_artifact_digest=sha("rollback"),
                changed_paths=["runtime/example.py"],
                intended_improvement_digest=sha("improvement"),
                success_criteria_digest=sha("criteria"),
                requested_actions=[],
                external_approval_required=True,
                max_canary_percent=5,
                max_deployment_cycles=2,
                rollback_window_ms=1_000,
                proposed_at_ms=1,
            )
            self.assertEqual([], validate_proposal(proposal))
            self.assertTrue(proposal["proposal_only"])
            self.assertFalse(proposal["running_system_modified"])
            self.assertFalse(proposal["direct_deployment_performed"])
            self.assertFalse(proposal["self_authorized"])
            state = build_initial_state(
                proposal=proposal, source_v025_state=source, now_ms=1
            )
            self.assertEqual([], validate_state(state))
            self.assertTrue(state["append_only"])
            self.assertFalse(state["memory_overwrite"])

    def test_static_analysis_cannot_pass_forbidden_action(self) -> None:
        with TemporaryDirectory() as directory:
            source = _admitted_and_replay(Path(directory) / "source")
            proposal = build_self_modification_proposal(
                proposal_id="forbidden-pass-attempt",
                source_v025_state=source,
                base_artifact_digest=sha("base"),
                candidate_artifact_digest=sha("candidate"),
                rollback_artifact_digest=sha("rollback"),
                changed_paths=["runtime/example.py"],
                intended_improvement_digest=sha("improvement"),
                success_criteria_digest=sha("criteria"),
                requested_actions=["widen_own_authority"],
                external_approval_required=True,
                max_canary_percent=5,
                max_deployment_cycles=2,
                rollback_window_ms=1_000,
                proposed_at_ms=1,
            )
            state = build_initial_state(
                proposal=proposal, source_v025_state=source, now_ms=1
            )
            with self.assertRaisesRegex(
                ValueError, "static_analysis_cannot_pass_forbidden_action"
            ):
                build_stage_evidence(
                    state=state,
                    stage="static_analysis",
                    passed=True,
                    evidence_digests=[sha("evidence")],
                    finding_codes=["widen_own_authority"],
                    isolated_environment_digest=sha("isolated"),
                    evaluator_id="external-evaluator",
                    evaluated_at_ms=2,
                )

    def test_canary_scope_is_bounded(self) -> None:
        with TemporaryDirectory() as directory:
            source = _admitted_and_replay(Path(directory) / "source")
            with self.assertRaisesRegex(
                ValueError, "max_canary_percent_above_governed_limit"
            ):
                build_self_modification_proposal(
                    proposal_id="wide-canary",
                    source_v025_state=source,
                    base_artifact_digest=sha("base"),
                    candidate_artifact_digest=sha("candidate"),
                    rollback_artifact_digest=sha("rollback"),
                    changed_paths=["runtime/example.py"],
                    intended_improvement_digest=sha("improvement"),
                    success_criteria_digest=sha("criteria"),
                    requested_actions=[],
                    external_approval_required=True,
                    max_canary_percent=11,
                    max_deployment_cycles=2,
                    rollback_window_ms=1_000,
                    proposed_at_ms=1,
                )

    def test_tampered_authority_is_rejected(self) -> None:
        with TemporaryDirectory() as directory:
            source = _admitted_and_replay(Path(directory) / "source")
            proposal = build_self_modification_proposal(
                proposal_id="tamper",
                source_v025_state=source,
                base_artifact_digest=sha("base"),
                candidate_artifact_digest=sha("candidate"),
                rollback_artifact_digest=sha("rollback"),
                changed_paths=["runtime/example.py"],
                intended_improvement_digest=sha("improvement"),
                success_criteria_digest=sha("criteria"),
                requested_actions=[],
                external_approval_required=True,
                max_canary_percent=5,
                max_deployment_cycles=2,
                rollback_window_ms=1_000,
                proposed_at_ms=1,
            )
            tampered = deepcopy(proposal)
            tampered["non_authority"]["grants_self_modification_authority"] = True
            self.assertIn("proposal_authority_escalation", validate_proposal(tampered))


if __name__ == "__main__":
    unittest.main()
