import unittest

from runtime.kuuos_repository_checkpoint_live_git_preflight_v1_17 import execute_repository_checkpoint_live_git_preflight
from runtime.kuuos_repository_checkpoint_live_ref_cas_v1_18 import build_repository_checkpoint_live_ref_cas_policy, build_repository_checkpoint_live_ref_cas_request
from runtime.kuuos_repository_constructed_commit_publication_types_v1_21 import COMMIT_PUBLISHED
from runtime.kuuos_repository_constructed_commit_publication_v1_21 import build_repository_constructed_commit_publication_policy, build_repository_constructed_commit_publication_request, execute_repository_constructed_commit_publication
from runtime.kuuos_repository_tree_commit_materialization_v1_20 import execute_repository_tree_commit_materialization
from tests import test_kuuos_repository_tree_commit_v1_20 as v120


class RepositoryConstructedCommitPublicationV121Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.fixture = v120.RepositoryTreeCommitV120Tests(methodName="test_exact_reuse_and_message_mismatch")
        self.fixture.setUp()
        self.v120_result = execute_repository_tree_commit_materialization(self.fixture.request, self.fixture.prior, self.fixture.message, self.fixture.policy)
        self.v118 = self.fixture.helper.helper
        self.v117 = self.v118.helper
        self.transition = self.v117._transition(self.v117.transition, expected_oid=self.v117.second_oid, proposed_oid=self.v120_result.expected_commit_oid)
        self.preflight_policy = self.v117.policy
        self.preflight_request = self.v117._request(self.transition)
        self.preflight_receipt = execute_repository_checkpoint_live_git_preflight(self.preflight_request, self.transition, self.preflight_policy)
        self.executor_id = "executor-v121"
        self.live_policy = build_repository_checkpoint_live_ref_cas_policy("v121-live", authorized_executor_ids=(self.executor_id,), allowed_repository_path_digests=(self.preflight_receipt.repository_path_digest,))
        self.live_request = build_repository_checkpoint_live_ref_cas_request("v121-live", self.preflight_request, self.preflight_receipt, self.transition, executor_id=self.executor_id, sandbox_marker_token=self.v118.marker_token, requested_at_epoch_seconds=1_800_000_005)
        self.policy = build_repository_constructed_commit_publication_policy("v121-publication", authorized_executor_ids=(self.executor_id,), allowed_repository_path_digests=(self.v120_result.repository_path_digest,))
        self.request = build_repository_constructed_commit_publication_request("v121-publication", self.v120_result, self.live_request, requested_at_epoch_seconds=1_800_000_006)

    def tearDown(self) -> None:
        self.fixture.tearDown()

    def execute(self, request=None, **kwargs):
        return execute_repository_constructed_commit_publication(
            self.request if request is None else request,
            self.v120_result,
            self.live_request,
            self.transition,
            self.preflight_policy,
            self.preflight_request,
            self.preflight_receipt,
            self.live_policy,
            self.policy,
            execution_started_at_epoch_seconds=1_800_000_010,
            execution_completed_at_epoch_seconds=1_800_000_012,
            **kwargs,
        )

    def test_constructed_commit_publication(self) -> None:
        before = self.v118._non_ref_snapshot()
        result = self.execute()
        after = self.v118._non_ref_snapshot()
        self.assertEqual(result.status, COMMIT_PUBLISHED)
        self.assertTrue(result.reference_cas_committed)
        self.assertTrue(result.checkpoint_reference_write_performed)
        self.assertFalse(result.current_object_database_write_performed)
        self.assertFalse(result.reflog_write_performed)
        self.assertEqual(before, after)


if __name__ == "__main__":
    unittest.main()
