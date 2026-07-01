import hashlib
from pathlib import Path
import unittest

from runtime.kuuos_repository_checkpoint_live_git_preflight_v1_17 import (
    execute_repository_checkpoint_live_git_preflight,
)
from runtime.kuuos_repository_checkpoint_live_ref_cas_types_v1_18 import (
    LIVE_REF_CAS_COMMITTED,
    LIVE_REF_CAS_REJECTED,
    SANDBOX_MARKER_FILENAME,
)
from runtime.kuuos_repository_checkpoint_live_ref_cas_v1_18 import (
    build_repository_checkpoint_live_ref_cas_policy,
    build_repository_checkpoint_live_ref_cas_request,
    execute_repository_checkpoint_live_ref_cas,
)
from tests import test_kuuos_repository_checkpoint_live_git_preflight_v1_17 as v117_tests


class RepositoryCheckpointLiveRefCasV118Tests(unittest.TestCase):
    marker_token = "a" * 64
    executor_id = "executor-v118"

    def setUp(self) -> None:
        self.helper = v117_tests.RepositoryCheckpointLiveGitPreflightV117Tests(
            methodName="test_same_repository_state_is_deterministic"
        )
        self.helper.setUp()
        self.root = self.helper.root
        self.transition = self.helper.transition
        self.preflight_policy = self.helper.policy
        self.preflight_request = self.helper._request()
        self.preflight_receipt = execute_repository_checkpoint_live_git_preflight(
            self.preflight_request,
            self.transition,
            self.preflight_policy,
        )
        self.marker_path = self.root / ".git" / SANDBOX_MARKER_FILENAME
        self.marker_path.write_text(self.marker_token + "\n", encoding="utf-8")
        self.policy = build_repository_checkpoint_live_ref_cas_policy(
            "checkpoint-live-ref-cas-policy-v118-tests",
            authorized_executor_ids=(self.executor_id,),
            allowed_repository_path_digests=(
                self.preflight_receipt.repository_path_digest,
            ),
        )
        self.requested_at = self.preflight_request.requested_at_epoch_seconds + 5
        self.started_at = self.requested_at + 5
        self.completed_at = self.started_at + 2

    def tearDown(self) -> None:
        self.helper.tearDown()

    def request(self, *, executor_id=None, marker_token=None):
        return build_repository_checkpoint_live_ref_cas_request(
            "checkpoint-live-ref-cas-v118",
            self.preflight_request,
            self.preflight_receipt,
            self.transition,
            executor_id=self.executor_id if executor_id is None else executor_id,
            sandbox_marker_token=(
                self.marker_token if marker_token is None else marker_token
            ),
            requested_at_epoch_seconds=self.requested_at,
        )

    def execute(self, request=None):
        return execute_repository_checkpoint_live_ref_cas(
            self.request() if request is None else request,
            self.transition,
            self.preflight_policy,
            self.preflight_request,
            self.preflight_receipt,
            self.policy,
            execution_started_at_epoch_seconds=self.started_at,
            execution_completed_at_epoch_seconds=self.completed_at,
        )

    def _digest_tree(self, root: Path) -> tuple[tuple[str, str], ...]:
        if not root.exists():
            return ()
        return tuple(
            (
                str(path.relative_to(root)),
                hashlib.sha256(path.read_bytes()).hexdigest(),
            )
            for path in sorted(item for item in root.rglob("*") if item.is_file())
        )

    def _non_ref_snapshot(self):
        git_dir = self.root / ".git"
        index = git_dir / "index"
        tracked = self.root / "tracked.txt"
        return {
            "objects": self._digest_tree(git_dir / "objects"),
            "logs": self._digest_tree(git_dir / "logs"),
            "index": (
                hashlib.sha256(index.read_bytes()).hexdigest()
                if index.exists()
                else ""
            ),
            "working_tree": hashlib.sha256(tracked.read_bytes()).hexdigest(),
        }

    def test_atomic_live_reference_cas_commits_only_checkpoint_ref(self) -> None:
        before = self._non_ref_snapshot()
        result = self.execute()
        after = self._non_ref_snapshot()
        observed = self.helper._git(
            "show-ref", "--verify", "--hash", self.helper.checkpoint_reference
        ).strip()

        self.assertEqual(result.status, LIVE_REF_CAS_COMMITTED)
        self.assertTrue(result.update_ref_attempted)
        self.assertTrue(result.update_ref_succeeded)
        self.assertTrue(result.post_update_verified)
        self.assertTrue(result.live_git_command_invoked)
        self.assertTrue(result.live_repository_mutated)
        self.assertTrue(result.checkpoint_reference_write_performed)
        self.assertEqual(result.observed_before_oid, self.helper.first_oid)
        self.assertEqual(result.observed_after_oid, self.helper.second_oid)
        self.assertEqual(observed, self.helper.second_oid)
        self.assertFalse(result.object_database_write_performed)
        self.assertFalse(result.index_write_performed)
        self.assertFalse(result.working_tree_write_performed)
        self.assertFalse(result.reflog_write_performed)
        self.assertFalse(result.force_update_performed)
        self.assertFalse(result.reference_delete_performed)
        self.assertFalse(result.push_performed)
        self.assertEqual(before, after)
        self.assertFalse(
            (self.root / ".git" / "logs" / self.helper.checkpoint_reference).exists()
        )

    def test_missing_or_incorrect_sandbox_marker_rejects_before_mutation(self) -> None:
        cases = ("missing", "incorrect")
        for case in cases:
            with self.subTest(case=case):
                self.helper._git(
                    "update-ref",
                    self.helper.checkpoint_reference,
                    self.helper.first_oid,
                )
                if case == "missing":
                    self.marker_path.unlink(missing_ok=True)
                else:
                    self.marker_path.write_text("b" * 64 + "\n", encoding="utf-8")
                result = self.execute()
                observed = self.helper._git(
                    "show-ref",
                    "--verify",
                    "--hash",
                    self.helper.checkpoint_reference,
                ).strip()
                self.assertEqual(result.status, LIVE_REF_CAS_REJECTED)
                self.assertFalse(result.update_ref_attempted)
                self.assertFalse(result.live_repository_mutated)
                self.assertEqual(observed, self.helper.first_oid)
                self.marker_path.write_text(
                    self.marker_token + "\n", encoding="utf-8"
                )

    def test_unauthorized_executor_rejects_before_mutation(self) -> None:
        result = self.execute(self.request(executor_id="unauthorized-v118"))
        observed = self.helper._git(
            "show-ref", "--verify", "--hash", self.helper.checkpoint_reference
        ).strip()
        self.assertEqual(result.status, LIVE_REF_CAS_REJECTED)
        self.assertFalse(result.executor_authorized)
        self.assertFalse(result.preflight_recomputed)
        self.assertFalse(result.update_ref_attempted)
        self.assertFalse(result.live_repository_mutated)
        self.assertEqual(observed, self.helper.first_oid)

    def test_changed_ref_after_supplied_preflight_is_rejected_by_recomputation(self) -> None:
        self.helper._git(
            "update-ref",
            self.helper.checkpoint_reference,
            self.helper.second_oid,
            self.helper.first_oid,
        )
        result = self.execute()
        observed = self.helper._git(
            "show-ref", "--verify", "--hash", self.helper.checkpoint_reference
        ).strip()
        self.assertEqual(result.status, LIVE_REF_CAS_REJECTED)
        self.assertTrue(result.preflight_recomputed)
        self.assertFalse(result.preflight_receipt_exact)
        self.assertFalse(result.update_ref_attempted)
        self.assertFalse(result.checkpoint_reference_write_performed)
        self.assertEqual(observed, self.helper.second_oid)

    def test_replay_cannot_apply_the_same_old_oid_twice(self) -> None:
        first = self.execute()
        second = self.execute()
        observed = self.helper._git(
            "show-ref", "--verify", "--hash", self.helper.checkpoint_reference
        ).strip()
        self.assertEqual(first.status, LIVE_REF_CAS_COMMITTED)
        self.assertEqual(second.status, LIVE_REF_CAS_REJECTED)
        self.assertFalse(second.preflight_receipt_exact)
        self.assertFalse(second.update_ref_attempted)
        self.assertFalse(second.checkpoint_reference_write_performed)
        self.assertEqual(observed, self.helper.second_oid)


if __name__ == "__main__":
    unittest.main()
