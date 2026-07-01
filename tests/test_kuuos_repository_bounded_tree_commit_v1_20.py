from dataclasses import replace
import hashlib
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from runtime.kuuos_repository_atomic_application_types_v0_92 import (
    repository_atomic_application_receipt_digest,
)
from runtime.kuuos_repository_bounded_tree_commit_types_v1_20 import (
    SANDBOX_MARKER_FILENAME,
    TREE_COMMIT_MATERIALIZED,
    TREE_COMMIT_REJECTED,
    TREE_COMMIT_REUSED,
)
from runtime.kuuos_repository_bounded_tree_commit_v1_20 import (
    build_repository_bounded_tree_commit_policy,
    build_repository_bounded_tree_commit_request,
    execute_repository_bounded_tree_commit,
    repository_bounded_tree_commit_result_issues,
)
from runtime.kuuos_repository_commit_candidate_strict_v0_93 import (
    certify_repository_commit_candidate,
)
from runtime.kuuos_repository_commit_candidate_types_v0_93 import (
    REGULAR_FILE_MODE,
    RepositoryParentTreeEntry,
)
from runtime.kuuos_repository_commit_candidate_v0_93 import (
    build_repository_parent_tree_inventory,
)
from runtime.kuuos_repository_live_object_materialization_types_v1_19 import (
    SANDBOX_MARKER_FILENAME as V119_MARKER_FILENAME,
)
from runtime.kuuos_repository_live_object_materialization_v1_19 import (
    execute_repository_live_object_materialization,
)
from runtime.v119_live_object_materialization_policy import (
    build_repository_live_object_materialization_policy,
    build_repository_live_object_materialization_request,
)
from tests import test_kuuos_repository_checkpoint_live_ref_cas_v1_18 as v118_tests
from tests import test_kuuos_repository_commit_candidate_v0_93 as v093_tests


class RepositoryBoundedTreeCommitV120Tests(unittest.TestCase):
    executor_id = "executor-v120"
    marker_token = "d" * 64
    v119_executor_id = "executor-v119-for-v120"
    v119_marker_token = "c" * 64

    def setUp(self) -> None:
        self.live = v118_tests.RepositoryCheckpointLiveRefCasV118Tests(
            methodName="test_atomic_live_reference_cas_commits_only_checkpoint_ref"
        )
        self.live.setUp()
        self.root = self.live.root
        self.v118_result = self.live.execute()

        self.model = v093_tests.RepositoryCommitCandidateV093Tests(
            methodName="test_candidate_is_deterministic_and_exactly_bound"
        )
        self.model.setUp()
        self.snapshot = self.model.snapshot
        self.application_receipt = replace(
            self.model.application_receipt,
            source_commit_sha=self.live.helper.second_oid,
            receipt_digest="",
        )
        self.application_receipt = replace(
            self.application_receipt,
            receipt_digest=repository_atomic_application_receipt_digest(
                self.application_receipt
            ),
        )
        parent_entries = []
        for path in self.snapshot.all_paths:
            payload = f"parent:{path}\n".encode("utf-8")
            oid = self._write_object("blob", payload)
            parent_entries.append(
                RepositoryParentTreeEntry(
                    path=path,
                    mode=REGULAR_FILE_MODE,
                    git_object_oid=oid,
                )
            )
        self.parent_inventory = build_repository_parent_tree_inventory(
            self.application_receipt.source_commit_sha,
            tuple(parent_entries),
        )
        self.candidate = certify_repository_commit_candidate(
            "bounded-tree-commit-candidate-v120",
            self.application_receipt,
            self.snapshot,
            self.parent_inventory,
            self.model.policy,
            author=self.model.author,
            committer=self.model.committer,
            message="Materialize bounded tree and commit objects v1.20",
        )

        v119_marker = self.root / ".git" / V119_MARKER_FILENAME
        v119_marker.write_text(self.v119_marker_token + "\n", encoding="utf-8")
        self.v119_policy = build_repository_live_object_materialization_policy(
            "bounded-tree-commit-v119-policy",
            authorized_executor_ids=(self.v119_executor_id,),
            allowed_repository_path_digests=(self.v118_result.repository_path_digest,),
        )
        payload_by_oid = {}
        for blob in self.candidate.blob_candidates:
            payload_by_oid[blob.git_blob_oid] = self.snapshot.texts[blob.path].encode(
                "utf-8"
            )
        results = []
        for index, (oid, payload) in enumerate(sorted(payload_by_oid.items())):
            request = build_repository_live_object_materialization_request(
                f"bounded-tree-commit-v119-{index}",
                str(self.root),
                self.v118_result,
                payload,
                executor_id=self.v119_executor_id,
                sandbox_marker_token=self.v119_marker_token,
                requested_at_epoch_seconds=1_800_000_200 + index,
            )
            self.assertEqual(request.expected_blob_oid, oid)
            results.append(
                execute_repository_live_object_materialization(
                    request,
                    self.v118_result,
                    payload,
                    self.v119_policy,
                )
            )
        self.v119_results = tuple(results)

        self.marker_path = self.root / ".git" / SANDBOX_MARKER_FILENAME
        self.marker_path.write_text(self.marker_token + "\n", encoding="utf-8")
        self.policy = build_repository_bounded_tree_commit_policy(
            "bounded-tree-commit-policy-v120-tests",
            authorized_executor_ids=(self.executor_id,),
            allowed_repository_path_digests=(self.v118_result.repository_path_digest,),
        )
        self.request = self._request()

    def tearDown(self) -> None:
        self.model.tearDown()
        self.live.tearDown()

    def _write_object(self, kind: str, payload: bytes) -> str:
        completed = subprocess.run(
            ["git", "-C", str(self.root), "hash-object", "-t", kind, "-w", "--stdin"],
            input=payload,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        )
        return completed.stdout.decode("ascii").strip()

    def _request(self, *, executor_id=None, marker_token=None, results=None):
        return build_repository_bounded_tree_commit_request(
            "bounded-tree-commit-v120",
            str(self.root),
            self.candidate,
            self.v119_results if results is None else results,
            executor_id=self.executor_id if executor_id is None else executor_id,
            sandbox_marker_token=(
                self.marker_token if marker_token is None else marker_token
            ),
            requested_at_epoch_seconds=1_800_000_300,
        )

    def execute(self, request=None, results=None, **kwargs):
        supplied_results = self.v119_results if results is None else results
        return execute_repository_bounded_tree_commit(
            self.request if request is None else request,
            self.candidate,
            self.application_receipt,
            self.snapshot,
            self.parent_inventory,
            self.model.policy,
            supplied_results,
            self.policy,
            **kwargs,
        )

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

    def test_tree_and_commit_objects_materialize_without_other_writes(self) -> None:
        git_dir = self.root / ".git"
        before_objects = {path for path, _ in self.digest_tree(git_dir / "objects")}
        before_other = self.non_object_snapshot()
        result = self.execute()
        after_objects = {path for path, _ in self.digest_tree(git_dir / "objects")}
        expected = {
            f"{oid[:2]}/{oid[2:]}"
            for oid in (*result.expected_tree_oids, result.expected_commit_oid)
        }
        self.assertEqual(result.status, TREE_COMMIT_MATERIALIZED)
        self.assertEqual(after_objects - before_objects, expected)
        self.assertEqual(before_other, self.non_object_snapshot())
        self.assertEqual(result.tree_write_count, len(result.expected_tree_oids))
        self.assertEqual(result.commit_write_count, 1)
        self.assertTrue(result.object_database_write_performed)
        self.assertFalse(result.reference_write_performed)
        self.assertFalse(result.index_write_performed)
        self.assertFalse(result.working_tree_write_performed)
        self.assertFalse(result.reflog_write_performed)
        self.assertFalse(result.push_performed)
        self.assertFalse(result.signing_performed)
        self.assertEqual(repository_bounded_tree_commit_result_issues(result), ())

    def test_exact_tree_and_commit_objects_are_reused(self) -> None:
        first = self.execute()
        objects_after_first = self.digest_tree(self.root / ".git" / "objects")
        second = self.execute()
        self.assertEqual(first.status, TREE_COMMIT_MATERIALIZED)
        self.assertEqual(second.status, TREE_COMMIT_REUSED)
        self.assertEqual(second.tree_write_count, 0)
        self.assertEqual(second.commit_write_count, 0)
        self.assertEqual(second.tree_reuse_count, len(second.expected_tree_oids))
        self.assertTrue(second.commit_reused)
        self.assertFalse(second.object_database_write_performed)
        self.assertEqual(objects_after_first, self.digest_tree(self.root / ".git" / "objects"))

    def test_unauthorized_executor_rejects_before_git(self) -> None:
        request = self._request(executor_id="unauthorized-v120")
        result = self.execute(request=request)
        self.assertEqual(result.status, TREE_COMMIT_REJECTED)
        self.assertFalse(result.executor_authorized)
        self.assertFalse(result.live_git_command_invoked)
        self.assertFalse(result.object_database_write_performed)

    def test_missing_v119_coverage_rejects_before_git(self) -> None:
        reduced = self.v119_results[:-1]
        if not reduced:
            self.skipTest("candidate has one unique changed blob")
        request = self._request(results=reduced)
        result = self.execute(request=request, results=reduced)
        self.assertEqual(result.status, TREE_COMMIT_REJECTED)
        self.assertFalse(result.blob_result_coverage_exact)
        self.assertFalse(result.live_git_command_invoked)

    def test_nonliteral_git_never_launches_subprocess(self) -> None:
        with patch("runtime.v120_bounded_tree_commit_git_adapter.subprocess.run") as run:
            with self.assertRaisesRegex(
                ValueError,
                "v120_git_executable_not_allowed",
            ):
                self.execute(git_executable="/bin/echo")
            run.assert_not_called()

    def test_git_object_directory_override_is_ignored(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            with patch.dict(os.environ, {"GIT_OBJECT_DIRECTORY": directory}, clear=False):
                result = self.execute()
            self.assertEqual(result.status, TREE_COMMIT_MATERIALIZED)
            self.assertEqual(os.listdir(directory), [])


if __name__ == "__main__":
    unittest.main()
