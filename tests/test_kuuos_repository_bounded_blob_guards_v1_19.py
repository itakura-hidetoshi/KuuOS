import unittest

from runtime.kuuos_repository_live_object_materialization_types_v1_19 import (
    OBJECT_REJECTED,
)
from runtime.kuuos_repository_live_object_materialization_v1_19 import (
    execute_repository_live_object_materialization,
)
from runtime.v119_live_object_materialization_policy import (
    build_repository_live_object_materialization_request,
)
from tests.test_kuuos_repository_bounded_blob_v1_19 import (
    RepositoryBoundedBlobV119Tests,
)


class RepositoryBoundedBlobGuardsV119Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.fixture = RepositoryBoundedBlobV119Tests(
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


if __name__ == "__main__":
    unittest.main()
