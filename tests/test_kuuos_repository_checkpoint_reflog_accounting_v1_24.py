from dataclasses import replace
import unittest

from runtime.kuuos_repository_checkpoint_reflog_types_v1_24 import (
    REFLOG_ERROR,
    repository_checkpoint_reflog_result_digest,
)
from runtime.v124_checkpoint_reflog_result import (
    repository_checkpoint_reflog_result_issues,
)
from tests import test_kuuos_repository_checkpoint_reflog_v1_24 as v124


class RepositoryCheckpointReflogAccountingV124Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.fixture = v124.RepositoryCheckpointReflogV124Tests(
            methodName=(
                "test_exact_checkpoint_transition_is_recorded_without_ref_change"
            )
        )
        self.fixture.setUp()

    def tearDown(self) -> None:
        self.fixture.tearDown()

    def test_error_preserves_completed_checkpoint_reflog_write(self) -> None:
        recorded = self.fixture.execute()
        simulated = replace(
            recorded,
            status=REFLOG_ERROR,
            reason="SIMULATED_CHECKPOINT_REFLOG_POSTCONDITION_ERROR",
            target_reflog_entry_exact=False,
            result_digest="",
        )
        simulated = replace(
            simulated,
            result_digest=repository_checkpoint_reflog_result_digest(simulated),
        )
        self.assertEqual(repository_checkpoint_reflog_result_issues(simulated), ())
        self.assertTrue(simulated.checkpoint_reflog_write_performed)
        self.assertTrue(simulated.live_repository_mutated)
        self.assertFalse(simulated.current_reference_write_performed)
        self.assertFalse(simulated.current_object_database_write_performed)
        self.assertFalse(simulated.index_write_performed)
        self.assertFalse(simulated.working_tree_write_performed)

    def test_error_can_report_unexpected_protected_effect(self) -> None:
        recorded = self.fixture.execute()
        simulated = replace(
            recorded,
            status=REFLOG_ERROR,
            reason="SIMULATED_UNEXPECTED_REFERENCE_EFFECT",
            current_reference_write_performed=True,
            result_digest="",
        )
        simulated = replace(
            simulated,
            result_digest=repository_checkpoint_reflog_result_digest(simulated),
        )
        self.assertEqual(repository_checkpoint_reflog_result_issues(simulated), ())
        self.assertTrue(simulated.current_reference_write_performed)
        self.assertTrue(simulated.live_repository_mutated)


if __name__ == "__main__":
    unittest.main()
