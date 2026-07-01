from dataclasses import replace
import os
import tempfile
import unittest
from unittest.mock import patch

from runtime.kuuos_repository_constructed_commit_publication_types_v1_21 import (
    COMMIT_PUBLISHED,
    PUBLICATION_REJECTED,
    repository_constructed_commit_publication_request_digest,
)
from tests import test_kuuos_repository_constructed_commit_publication_v1_21 as v121


class RepositoryConstructedCommitPublicationGuardsV121Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.fixture = v121.RepositoryConstructedCommitPublicationV121Tests(
            methodName="test_constructed_commit_publication"
        )
        self.fixture.setUp()

    def tearDown(self) -> None:
        self.fixture.tearDown()

    def test_commit_binding_mismatch_rejects_before_delegate(self) -> None:
        altered = replace(
            self.fixture.request,
            constructed_commit_oid="f" * 40,
            request_digest="",
        )
        altered = replace(
            altered,
            request_digest=repository_constructed_commit_publication_request_digest(
                altered
            ),
        )
        result = self.fixture.execute(altered)
        self.assertEqual(result.status, PUBLICATION_REJECTED)
        self.assertFalse(result.constructed_commit_binding_exact)
        self.assertFalse(result.delegated_live_ref_cas_invoked)
        self.assertFalse(result.checkpoint_reference_write_performed)

    def test_nonliteral_git_is_rejected_before_delegate(self) -> None:
        with self.assertRaisesRegex(ValueError, "v121_git_executable_not_allowed"):
            self.fixture.execute(git_executable="not-git")

    def test_git_environment_redirect_is_removed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            with patch.dict(os.environ, {"GIT_DIR": directory}, clear=False):
                result = self.fixture.execute()
            self.assertEqual(result.status, COMMIT_PUBLISHED)
            self.assertEqual(os.listdir(directory), [])


if __name__ == "__main__":
    unittest.main()
