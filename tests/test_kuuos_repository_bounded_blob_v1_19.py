import unittest

from runtime.kuuos_repository_live_object_materialization_types_v1_19 import (
    SANDBOX_MARKER_FILENAME,
)
from runtime.kuuos_repository_live_object_materialization_v1_19 import (
    execute_repository_live_object_materialization,
)
from runtime.v119_live_object_materialization_policy import (
    build_repository_live_object_materialization_policy,
    build_repository_live_object_materialization_request,
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

    def test_entrypoint_returns_a_result(self) -> None:
        result = execute_repository_live_object_materialization(
            self.request, self.prior, self.payload, self.policy
        )
        self.assertTrue(result.result_digest)
