from pathlib import Path
import unittest

from runtime.kuuos_repository_checkpoint_reflog_types_v1_24 import (
    AUTHORITY_MARKER_FILENAME,
    REFLOG_RECORDED,
    REFLOG_REUSED,
)
from runtime.kuuos_repository_checkpoint_reflog_v1_24 import (
    build_repository_checkpoint_reflog_policy,
    build_repository_checkpoint_reflog_request,
    execute_repository_checkpoint_reflog,
)
from runtime.v124_checkpoint_reflog_surfaces import (
    protected_checkpoint_reflog_snapshot,
)
from runtime.v124_checkpoint_reflog_validation import (
    expected_reflog_entry,
    target_reflog_path,
)
from tests import test_kuuos_repository_sandbox_worktree_v1_23 as v123


class RepositoryCheckpointReflogV124Tests(unittest.TestCase):
    marker_token = "a" * 64

    def setUp(self) -> None:
        self.helper = v123.RepositorySandboxWorktreeV123Tests(
            methodName="test_exact_index_is_reflected_in_sandbox_only"
        )
        self.helper.setUp()
        self.root = self.helper.root
        self.v123_result = self.helper.execute()
        self.v122 = self.helper.helper
        self.v121 = self.v122.helper
        self.v121_result = self.v122.v121_result
        marker = self.root / ".git" / AUTHORITY_MARKER_FILENAME
        marker.write_text(self.marker_token + "\n", encoding="ascii")
        self.policy = build_repository_checkpoint_reflog_policy(
            "checkpoint-reflog-v124-tests",
            authorized_executor_ids=(self.helper.request.executor_id,),
            allowed_repository_path_digests=(
                self.v123_result.repository_path_digest,
            ),
        )
        self.request = build_repository_checkpoint_reflog_request(
            "checkpoint-reflog-v124",
            str(self.root),
            self.v121.request,
            self.v121_result,
            self.helper.request,
            self.v123_result,
            executor_id=self.helper.request.executor_id,
            authority_marker_token=self.marker_token,
            committer_name="KuuOS Checkpoint Recorder",
            committer_email="checkpoint-reflog@example.invalid",
            recorded_at_epoch_seconds=1_800_000_040,
            message="KuuOS checkpoint publication v1.24",
        )

    def tearDown(self) -> None:
        self.helper.tearDown()

    def execute(self, request=None, policy=None, **kwargs):
        return execute_repository_checkpoint_reflog(
            self.request if request is None else request,
            self.v121.request,
            self.v121_result,
            self.helper.request,
            self.v123_result,
            self.policy if policy is None else policy,
            **kwargs,
        )

    def target_path(self) -> Path:
        return target_reflog_path(
            self.root / ".git",
            self.request.checkpoint_reference,
        )

    def protected_snapshot(self):
        return protected_checkpoint_reflog_snapshot(
            self.root,
            self.helper.request.dedicated_index_filename,
            self.target_path(),
        )

    def test_exact_checkpoint_transition_is_recorded_without_ref_change(self) -> None:
        before = self.protected_snapshot()
        result = self.execute()
        after = self.protected_snapshot()
        self.assertEqual(result.status, REFLOG_RECORDED)
        self.assertEqual(
            self.target_path().read_bytes(),
            expected_reflog_entry(self.request),
        )
        self.assertTrue(result.current_ref_exact_before)
        self.assertTrue(result.current_ref_exact_after)
        self.assertTrue(result.target_reflog_entry_exact)
        self.assertTrue(result.target_reflog_single_entry)
        self.assertTrue(result.checkpoint_reflog_write_performed)
        self.assertTrue(result.live_repository_mutated)
        self.assertFalse(result.other_reflog_write_performed)
        self.assertFalse(result.current_object_database_write_performed)
        self.assertFalse(result.current_reference_write_performed)
        self.assertFalse(result.index_write_performed)
        self.assertFalse(result.working_tree_write_performed)
        self.assertTrue(result.prior_object_database_write_performed)
        self.assertTrue(result.prior_checkpoint_reference_write_performed)
        self.assertTrue(result.prior_dedicated_index_write_performed)
        self.assertTrue(result.prior_sandbox_working_tree_write_performed)
        for key in (
            "objects",
            "references",
            "standard_index",
            "dedicated_index",
            "working_tree",
            "other_logs",
        ):
            self.assertEqual(before[key], after[key])

    def test_exact_existing_checkpoint_reflog_is_reused(self) -> None:
        first = self.execute()
        payload = self.target_path().read_bytes()
        second = self.execute()
        self.assertEqual(first.status, REFLOG_RECORDED)
        self.assertEqual(second.status, REFLOG_REUSED)
        self.assertTrue(second.exact_existing_reflog_reused)
        self.assertFalse(second.reflog_write_command_attempted)
        self.assertFalse(second.checkpoint_reflog_write_performed)
        self.assertFalse(second.live_repository_mutated)
        self.assertEqual(payload, self.target_path().read_bytes())


if __name__ == "__main__":
    unittest.main()
