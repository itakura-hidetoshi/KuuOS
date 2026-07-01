from dataclasses import replace
import unittest

from runtime.kuuos_repository_live_object_materialization_types_v1_19 import (
    OBJECT_ERROR,
    repository_live_object_materialization_result_digest,
)
from runtime.kuuos_repository_live_object_materialization_v1_19 import (
    execute_repository_live_object_materialization,
)
from runtime.v119_live_object_materialization_result import (
    repository_live_object_materialization_result_issues,
)
from tests import test_kuuos_repository_bounded_blob_v1_19 as v119_tests


class RepositoryBoundedBlobAccountingV119Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.fixture = v119_tests.RepositoryBoundedBlobV119Tests(
            methodName="test_probe_normalization_is_fail_closed"
        )
        self.fixture.setUp()

    def tearDown(self) -> None:
        self.fixture.tearDown()

    def test_error_preserves_completed_object_write(self) -> None:
        materialized = execute_repository_live_object_materialization(
            self.fixture.request,
            self.fixture.prior,
            self.fixture.payload,
            self.fixture.policy,
        )
        simulated = replace(
            materialized,
            status=OBJECT_ERROR,
            reason="SIMULATED_POSTCONDITION_ERROR",
            object_present_after=False,
            object_type_blob=False,
            object_size_exact=False,
            object_content_exact=False,
            result_digest="",
        )
        simulated = replace(
            simulated,
            result_digest=repository_live_object_materialization_result_digest(
                simulated
            ),
        )
        self.assertEqual(
            repository_live_object_materialization_result_issues(simulated),
            (),
        )
        self.assertTrue(simulated.write_command_succeeded)
        self.assertTrue(simulated.object_database_write_performed)
        self.assertTrue(simulated.live_repository_mutated)


if __name__ == "__main__":
    unittest.main()
