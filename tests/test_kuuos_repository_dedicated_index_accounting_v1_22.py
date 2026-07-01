from dataclasses import replace
import unittest

from runtime.kuuos_repository_dedicated_index_types_v1_22 import (
    INDEX_ERROR,
    repository_dedicated_index_result_digest,
)
from runtime.v122_dedicated_index_result import (
    repository_dedicated_index_result_issues,
)
from tests import test_kuuos_repository_dedicated_index_v1_22 as v122


class RepositoryDedicatedIndexAccountingV122Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.fixture = v122.RepositoryDedicatedIndexV122Tests(
            methodName="test_exact_tree_is_loaded_into_dedicated_index_only"
        )
        self.fixture.setUp()

    def tearDown(self) -> None:
        self.fixture.tearDown()

    def test_error_preserves_completed_dedicated_index_write(self) -> None:
        materialized = self.fixture.execute()
        simulated = replace(
            materialized,
            status=INDEX_ERROR,
            reason="SIMULATED_POSTCONDITION_ERROR",
            index_entries_exact=False,
            result_digest="",
        )
        simulated = replace(
            simulated,
            result_digest=repository_dedicated_index_result_digest(simulated),
        )
        self.assertEqual(repository_dedicated_index_result_issues(simulated), ())
        self.assertTrue(simulated.dedicated_index_write_performed)
        self.assertTrue(simulated.live_repository_mutated)
        self.assertFalse(simulated.canonical_index_write_performed)
        self.assertFalse(simulated.current_object_database_write_performed)
        self.assertFalse(simulated.current_reference_write_performed)


if __name__ == "__main__":
    unittest.main()
