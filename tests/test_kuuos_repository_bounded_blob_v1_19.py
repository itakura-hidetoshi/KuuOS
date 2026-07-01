import hashlib
from pathlib import Path
import unittest

from runtime.kuuos_repository_live_object_materialization_types_v1_19 import (
    OBJECT_MATERIALIZED,
    OBJECT_REJECTED,
    OBJECT_REUSED,
    SANDBOX_MARKER_FILENAME,
)
from runtime.kuuos_repository_live_object_materialization_v1_19 import (
    execute_repository_live_object_materialization,
)
from runtime.v119_live_object_materialization_policy import (
    build_repository_live_object_materialization_policy,
    build_repository_live_object_materialization_request,
)
from runtime.v119_probe_status import (
    TARGET_PROBE_OPERATION,
    normalize_probe_status,
)
from tests import test_kuuos_repository_checkpoint_live_ref_cas_v1_18 as v118


class RepositoryBoundedBlobV119Tests(unittest.TestCase):
    payload = b"KuuOS bounded blob validation v1.19\n"
    executor_id = "executor-v119"
    marker_token = "c" * 64

    def setUp(self) -> None:
        self.helper = v118.RepositoryCheckpointLiveRefCasV118Tests(
            methodName="test_atomic_live_reference_cas_commits_only_checkpoint_ref"
        )
        self.helper.setUp()
        self.root = self.helper.root
        self.prior = self.helper.execute()
        marker = self.root / ".git" / SANDBOX_MARKER_FILENAME
        marker.write_text(self.marker_token + "\n", encoding="utf-8")
        self.policy = build_repository_live_object_materialization_policy(
            "bounded-blob-v119-tests",
            authorized_executor_ids=(self.executor_id,),
            allowed_repository_path_digests=(self.prior.repository_path_digest,),
        )
        self.request = build_repository_live_object_materialization_request(
            "bounded-blob-v119",
            str(self.root),
            self.prior,
            self.payload,
            executor_id=self.executor_id,
            sandbox_marker_token=self.marker_token,
            requested_at_epoch_seconds=1_800_000_100,
        )

    def tearDown(self) -> None:
        self.helper.tearDown()

    @staticmethod
    def digest_tree(root: Path) -> tuple[tuple[str, str], ...]:
        if not root.exists():
            return ()
        return tuple(
            (
                str(path.relative_to(root)),
                hashlib.sha256(path.read_bytes()).hexdigest(),
            )
            for path in sorted(item for item in root.rglob("*") if item.is_file())
        )

    def non_object_snapshot(self):
        git_dir = self.root / ".git"
        index = git_dir / "index"
        return (
            self.digest_tree(git_dir / "refs"),
            self.digest_tree(git_dir / "logs"),
            hashlib.sha256(index.read_bytes()).hexdigest(),
            hashlib.sha256((self.root / "tracked.txt").read_bytes()).hexdigest(),
        )

    def test_new_blob_is_materialized_without_other_writes(self) -> None:
        git_dir = self.root / ".git"
        before_objects = {path for path, _ in self.digest_tree(git_dir / "objects")}
        before_other = self.non_object_snapshot()
        result = execute_repository_live_object_materialization(
            self.request, self.prior, self.payload, self.policy
        )
        after_objects = {path for path, _ in self.digest_tree(git_dir / "objects")}
        expected_path = (
            f"{self.request.expected_blob_oid[:2]}/"
            f"{self.request.expected_blob_oid[2:]}"
        )
        self.assertEqual(result.status, OBJECT_MATERIALIZED)
        self.assertEqual(after_objects - before_objects, {expected_path})
        self.assertEqual(before_other, self.non_object_snapshot())
        self.assertTrue(result.object_database_write_performed)
        self.assertTrue(result.object_present_after)
        self.assertTrue(result.object_type_blob)
        self.assertTrue(result.object_size_exact)
        self.assertTrue(result.object_content_exact)
        self.assertFalse(result.reference_write_performed)
        self.assertFalse(result.index_write_performed)
        self.assertFalse(result.working_tree_write_performed)
        self.assertFalse(result.reflog_write_performed)
        self.assertFalse(result.push_performed)
        self.assertTrue(result.result_digest)

    def test_exact_reuse_and_payload_mismatch(self) -> None:
        first = execute_repository_live_object_materialization(
            self.request, self.prior, self.payload, self.policy
        )
        object_snapshot = self.digest_tree(self.root / ".git" / "objects")
        second = execute_repository_live_object_materialization(
            self.request, self.prior, self.payload, self.policy
        )
        self.assertEqual(first.status, OBJECT_MATERIALIZED)
        self.assertEqual(second.status, OBJECT_REUSED)
        self.assertFalse(second.write_command_attempted)
        self.assertFalse(second.object_database_write_performed)
        self.assertFalse(second.live_repository_mutated)
        self.assertEqual(
            object_snapshot,
            self.digest_tree(self.root / ".git" / "objects"),
        )
        rejected = execute_repository_live_object_materialization(
            self.request,
            self.prior,
            self.payload + b"tampered",
            self.policy,
        )
        self.assertEqual(rejected.status, OBJECT_REJECTED)
        self.assertFalse(rejected.payload_binding_exact)
        self.assertFalse(rejected.live_git_command_invoked)
        self.assertFalse(rejected.object_database_write_performed)

    def test_probe_normalization_is_fail_closed(self) -> None:
        missing = b"fatal: Not a valid object name 0000000000000000000000000000000000000000"
        denied = b"fatal: cannot access object database"
        self.assertEqual(
            normalize_probe_status(TARGET_PROBE_OPERATION, 128, False, missing),
            1,
        )
        self.assertEqual(
            normalize_probe_status(TARGET_PROBE_OPERATION, 128, False, denied),
            128,
        )


if __name__ == "__main__":
    unittest.main()
