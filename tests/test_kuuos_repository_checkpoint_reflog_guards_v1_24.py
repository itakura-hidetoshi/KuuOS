from dataclasses import replace
import os
import tempfile
import unittest
from unittest.mock import patch

from runtime.kuuos_repository_checkpoint_reflog_types_v1_24 import (
    AUTHORITY_MARKER_FILENAME,
    REFLOG_RECORDED,
    REFLOG_REJECTED,
    repository_checkpoint_reflog_request_digest,
)
from runtime.kuuos_repository_checkpoint_reflog_v1_24 import (
    build_repository_checkpoint_reflog_policy,
)
from tests import test_kuuos_repository_checkpoint_reflog_v1_24 as v124


class RepositoryCheckpointReflogGuardsV124Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.fixture = v124.RepositoryCheckpointReflogV124Tests(
            methodName=(
                "test_exact_checkpoint_transition_is_recorded_without_ref_change"
            )
        )
        self.fixture.setUp()

    def tearDown(self) -> None:
        self.fixture.tearDown()

    def test_missing_authority_marker_rejects_before_git(self) -> None:
        marker = (
            self.fixture.root
            / ".git"
            / AUTHORITY_MARKER_FILENAME
        )
        marker.unlink()
        result = self.fixture.execute()
        self.assertEqual(result.status, REFLOG_REJECTED)
        self.assertFalse(result.authority_marker_exact)
        self.assertFalse(result.live_git_command_invoked)
        self.assertFalse(result.checkpoint_reflog_write_performed)

    def test_unauthorized_executor_rejects_before_git(self) -> None:
        policy = build_repository_checkpoint_reflog_policy(
            "checkpoint-reflog-v124-unauthorized",
            authorized_executor_ids=("another-executor",),
            allowed_repository_path_digests=(
                self.fixture.request.repository_path_digest,
            ),
        )
        result = self.fixture.execute(policy=policy)
        self.assertEqual(result.status, REFLOG_REJECTED)
        self.assertFalse(result.executor_authorized)
        self.assertFalse(result.live_git_command_invoked)

    def test_mismatched_publication_binding_rejects_before_git(self) -> None:
        altered = replace(
            self.fixture.request,
            transition_old_oid="f" * 40,
            request_digest="",
        )
        altered = replace(
            altered,
            request_digest=repository_checkpoint_reflog_request_digest(altered),
        )
        result = self.fixture.execute(request=altered)
        self.assertEqual(result.status, REFLOG_REJECTED)
        self.assertFalse(result.cross_stage_binding_exact)
        self.assertFalse(result.live_git_command_invoked)

    def test_existing_mismatched_reflog_is_not_overwritten(self) -> None:
        target = self.fixture.target_path()
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("mismatched checkpoint log\n", encoding="utf-8")
        before = target.read_bytes()
        result = self.fixture.execute()
        self.assertEqual(result.status, REFLOG_REJECTED)
        self.assertFalse(result.target_reflog_entry_exact)
        self.assertFalse(result.reflog_write_command_attempted)
        self.assertFalse(result.checkpoint_reflog_write_performed)
        self.assertEqual(before, target.read_bytes())

    def test_symlink_target_reflog_is_rejected_before_git(self) -> None:
        target = self.fixture.target_path()
        target.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory() as directory:
            outside = os.path.join(directory, "outside-log")
            with open(outside, "wb") as stream:
                stream.write(b"outside\n")
            target.symlink_to(outside)
            result = self.fixture.execute()
            self.assertEqual(result.status, REFLOG_REJECTED)
            self.assertFalse(result.target_reflog_path_exact)
            self.assertFalse(result.live_git_command_invoked)
            with open(outside, "rb") as stream:
                self.assertEqual(stream.read(), b"outside\n")

    def test_nonliteral_git_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "v124_git_executable_not_allowed"):
            self.fixture.execute(git_executable="not-git")

    def test_inherited_git_environment_is_ignored(self) -> None:
        with tempfile.TemporaryDirectory() as fake_git:
            with tempfile.TemporaryDirectory() as fake_worktree:
                with tempfile.TemporaryDirectory() as fake_objects:
                    with patch.dict(
                        os.environ,
                        {
                            "GIT_DIR": fake_git,
                            "GIT_WORK_TREE": fake_worktree,
                            "GIT_OBJECT_DIRECTORY": fake_objects,
                            "GIT_COMMITTER_NAME": "Uncontrolled Identity",
                            "GIT_COMMITTER_EMAIL": "uncontrolled@example.invalid",
                        },
                        clear=False,
                    ):
                        result = self.fixture.execute()
                    self.assertEqual(os.listdir(fake_git), [])
                    self.assertEqual(os.listdir(fake_worktree), [])
                    self.assertEqual(os.listdir(fake_objects), [])
        self.assertEqual(result.status, REFLOG_RECORDED)
        self.assertTrue(result.target_reflog_entry_exact)
        self.assertFalse(result.current_reference_write_performed)


if __name__ == "__main__":
    unittest.main()
