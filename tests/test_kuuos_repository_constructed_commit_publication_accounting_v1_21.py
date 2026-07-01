from dataclasses import replace
import unittest

from runtime.kuuos_repository_constructed_commit_publication_types_v1_21 import (
    PUBLICATION_ERROR,
    repository_constructed_commit_publication_result_digest,
)
from runtime.v121_constructed_commit_publication_result import (
    repository_constructed_commit_publication_result_issues,
)
from tests import test_kuuos_repository_constructed_commit_publication_v1_21 as v121


class RepositoryConstructedCommitPublicationAccountingV121Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.fixture = v121.RepositoryConstructedCommitPublicationV121Tests(
            methodName="test_constructed_commit_publication"
        )
        self.fixture.setUp()

    def tearDown(self) -> None:
        self.fixture.tearDown()

    def test_error_preserves_completed_reference_write(self) -> None:
        published = self.fixture.execute()
        simulated = replace(
            published,
            status=PUBLICATION_ERROR,
            reason="SIMULATED_POSTCONDITION_ERROR",
            reference_cas_committed=False,
            result_digest="",
        )
        simulated = replace(
            simulated,
            result_digest=repository_constructed_commit_publication_result_digest(
                simulated
            ),
        )
        self.assertEqual(
            repository_constructed_commit_publication_result_issues(simulated),
            (),
        )
        self.assertTrue(simulated.checkpoint_reference_write_performed)
        self.assertTrue(simulated.live_repository_mutated)
        self.assertFalse(simulated.current_object_database_write_performed)
        self.assertFalse(simulated.reference_cas_committed)


if __name__ == "__main__":
    unittest.main()
