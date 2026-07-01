import os
import tempfile
import unittest
from unittest.mock import patch

from runtime.kuuos_repository_live_object_materialization_types_v1_19 import (
    OBJECT_MATERIALIZED,
    OBJECT_REJECTED,
)
from runtime.kuuos_repository_live_object_materialization_v1_19 import (
    execute_repository_live_object_materialization,
)
from runtime.v119_live_object_materialization_policy import (
    build_repository_live_object_materialization_request,
)
from tests import test_kuuos_repository_bounded_blob_v1_19 as v119_tests


class RepositoryBoundedBlobGuardsV119Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.fixture = v119_tests.RepositoryBoundedBlobV119Tests(
            methodName="test_probe_normalization_is_fail_closed"
        )
        self.fixture.setUp()

    def tearDown(self) -> None:
        self.fixture.tearDown()

    def test_missing_marker_rejects_before_git(self) -> None:
        marker = self.fixture.root / ".git" / "kuuos-live-object-materialization-sandbox-v1_19"
        marker.unlink()
        result = execute_repository_live_object_materialization(
            self.fixture.request,
            self.fixture.prior,
            self.fixture.payload,
            self.fixture.policy,
        )
        self.assertEqual(result.status, OBJECT_REJECTED)
        self.assertFalse(result.sandbox_marker_present)
        self.assertFalse(result.live_git_command_invoked)
        self.assertFalse(result.object_database_write_performed)

    def test_unauthorized_executor_rejects_before_git(self) -> None:
        request = build_repository_live_object_materialization_request(
            "bounded-blob-v119-unauthorized",
            str(self.fixture.root),
            self.fixture.prior,
            self.fixture.payload,
            executor_id="unauthorized-v119",
            sandbox_marker_token=self.fixture.marker_token,
            requested_at_epoch_seconds=1_800_000_101,
        )
        result = execute_repository_live_object_materialization(
            request,
            self.fixture.prior,
            self.fixture.payload,
            self.fixture.policy,
        )
        self.assertEqual(result.status, OBJECT_REJECTED)
        self.assertFalse(result.executor_authorized)
        self.assertFalse(result.live_git_command_invoked)
        self.assertFalse(result.object_database_write_performed)

    def test_nonliteral_git_is_rejected_before_process_launch(self) -> None:
        with patch("runtime.v119_live_object_git_adapter.subprocess.run") as run:
            with self.assertRaisesRegex(
                ValueError,
                "v119_git_executable_not_allowed",
            ):
                execute_repository_live_object_materialization(
                    self.fixture.request,
                    self.fixture.prior,
                    self.fixture.payload,
                    self.fixture.policy,
                    git_executable="/bin/echo",
                )
            run.assert_not_called()

    def test_object_directory_override_is_removed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            with patch.dict(
                os.environ,
                {"GIT_OBJECT_DIRECTORY": directory},
                clear=False,
            ):
                result = execute_repository_live_object_materialization(
                    self.fixture.request,
                    self.fixture.prior,
                    self.fixture.payload,
                    self.fixture.policy,
                )
            self.assertEqual(result.status, OBJECT_MATERIALIZED)
            self.assertEqual(os.listdir(directory), [])


if __name__ == "__main__":
    unittest.main()
