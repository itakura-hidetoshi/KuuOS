from __future__ import annotations

import unittest

from runtime import kuuos_ci_continuation_v0_45 as continuation
from runtime import kuuos_current_check as current_check


class CIContinuationV045Test(unittest.TestCase):
    def test_metadata_and_boundaries_are_valid(self) -> None:
        self.assertEqual(continuation.VERSION, "kuuos_ci_continuation_v0_45")
        self.assertEqual(continuation.DEPENDS_ON, "kuuos_overview_index_v0_44")
        self.assertEqual(continuation.POLICY, "run_all_then_decide")
        self.assertIn(
            "ci_success_does_not_grant_merge_authority",
            continuation.NON_AUTHORITY_BOUNDARIES,
        )
        self.assertIn(
            "continuation_does_not_execute_git_or_github_mutation",
            continuation.NON_AUTHORITY_BOUNDARIES,
        )

    def test_continuation_runs_all_steps_before_deciding_failure(self) -> None:
        steps = (
            continuation.ContinuationStep("first", "fake", "a", True),
            continuation.ContinuationStep("middle", "fake", "b", True),
            continuation.ContinuationStep("last", "fake", "c", True),
        )
        observed: list[str] = []

        def fake_executor(step: continuation.StepLike) -> tuple[int, str]:
            observed.append(step.step_id)
            if step.step_id == "middle":
                return 1, "synthetic_failure"
            return 0, "synthetic_success"

        report = continuation.run_ci_continuation(steps, executor=fake_executor)
        self.assertEqual(observed, ["first", "middle", "last"])
        self.assertTrue(report.all_steps_observed)
        self.assertFalse(report.passed)
        self.assertEqual(report.failed_steps(), ("middle",))
        self.assertEqual(report.required_failure_count, 1)
        self.assertEqual(report.decision, continuation.FAILURE_DECISION)

    def test_success_decision_is_separate_next_stage_review(self) -> None:
        steps = (
            continuation.ContinuationStep("first", "fake", "a", True),
            continuation.ContinuationStep("second", "fake", "b", True),
        )
        report = continuation.run_ci_continuation(
            steps,
            executor=lambda step: (0, "synthetic_success"),
        )
        self.assertTrue(report.passed)
        self.assertEqual(report.required_failure_count, 0)
        self.assertEqual(report.decision, continuation.SUCCESS_DECISION)
        self.assertIn("Decision", report.as_markdown())

    def test_unknown_runner_fails_closed(self) -> None:
        step = continuation.ContinuationStep("bad", "unknown", "target", True)
        report = continuation.run_ci_continuation((step,))
        self.assertFalse(report.passed)
        self.assertEqual(report.failed_steps(), ("bad",))
        self.assertIn("unknown_runner", report.results[0].detail)

    def test_current_root_registers_self_test(self) -> None:
        self.assertEqual(continuation.continuation_issues(), ())
        self.assertTrue(continuation.verify_ci_continuation())

    def test_current_check_routes_through_continuation(self) -> None:
        self.assertEqual(
            current_check.CURRENT_ROOT_SEQUENCE_FRONTIER,
            "kuuos_ci_continuation_v0_45",
        )
        self.assertEqual(current_check.run_current(), continuation.run_current_continuation())


if __name__ == "__main__":
    unittest.main()
