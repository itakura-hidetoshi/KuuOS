from __future__ import annotations

from copy import deepcopy
import unittest

from runtime.kuuos_codeai_candidate_patch_envelope_v0_1 import (
    CANDIDATE_DIGEST_FIELD,
    RECEIPT_DIGEST_FIELD as CANDIDATE_RECEIPT_DIGEST_FIELD,
    canonical_digest,
    patch_artifact_digest,
    seal,
)
from runtime.kuuos_codeai_autonomous_candidate_portfolio_selection_v0_1 import (
    DISPOSITION_SELECTED,
    MODE_SELECTION_ONLY,
    PROFILE_VERSION as SELECTION_PROFILE_VERSION,
    RECEIPT_DIGEST_FIELD as SELECTION_RECEIPT_DIGEST_FIELD,
    SelectedVerificationCandidate,
)
from runtime.kuuos_codeai_autonomous_isolated_candidate_application_v0_1 import (
    APPLICATION_PURPOSE,
    POLICY_DIGEST_FIELD,
    REQUEST_DIGEST_FIELD,
    STATUS_BLOCKED,
    STATUS_READY,
    build_codeai_autonomous_isolated_candidate_application,
)


class IsolatedCandidateApplicationTests(unittest.TestCase):
    def fixture(self):
        repository = {"src/a.py": 'print("old")\n', "src/d.py": "bye\n"}
        artifact = (
            "diff --git a/src/a.py b/src/a.py\n"
            "--- a/src/a.py\n+++ b/src/a.py\n@@ -1 +1 @@\n"
            '-print("old")\n+print("new")\n'
            "diff --git a/src/b.py b/src/b.py\nnew file mode 100644\n"
            "--- /dev/null\n+++ b/src/b.py\n@@ -0,0 +1 @@\n+hello\n"
            "diff --git a/src/d.py b/src/d.py\ndeleted file mode 100644\n"
            "--- a/src/d.py\n+++ /dev/null\n@@ -1 +0,0 @@\n-bye\n"
        )
        candidate = seal(
            {
                "candidate_id": "candidate-1",
                "patch_artifact_digest": patch_artifact_digest(artifact),
                "patch_size_bytes": len(artifact.encode("utf-8")),
                "patch_format": "unified_diff",
                "repository_full_name": "example/repo",
                "source_commit_sha": "a" * 40,
                "declared_change_count": 3,
                "changed_paths": ["src/a.py", "src/b.py", "src/d.py"],
                "added_paths": ["src/b.py"],
                "modified_paths": ["src/a.py"],
                "deleted_paths": ["src/d.py"],
            },
            CANDIDATE_DIGEST_FIELD,
        )
        candidate_receipt = seal(
            {"candidate_patch_ready": True, "codeai_disposition": "candidate_patch_supported"},
            CANDIDATE_RECEIPT_DIGEST_FIELD,
        )
        selected = SelectedVerificationCandidate("candidate-1", 1, candidate, artifact, candidate_receipt)
        selection = seal(
            {
                "schema_version": "v0.1",
                "profile_version": SELECTION_PROFILE_VERSION,
                "codeai_disposition": DISPOSITION_SELECTED,
                "operating_mode": MODE_SELECTION_ONLY,
                "route_receipt_recorded": True,
                "candidate_selected": True,
                "selected_for_independent_verification": True,
                "selection_performed_by_kernel": True,
                "selection_authority_consumed_by_kernel": True,
                "verification_lease_issued": False,
                "execution_lease_issued": False,
                "patch_applied": False,
                "repository_mutation_performed": False,
                "git_ref_changed": False,
                "branch_created": False,
                "commit_created": False,
                "push_performed": False,
                "pull_request_created": False,
                "merge_performed": False,
                "deployment_performed": False,
                "secret_access_performed": False,
                "selected_candidate_id": candidate["candidate_id"],
                "selected_candidate_digest": candidate[CANDIDATE_DIGEST_FIELD],
                "selected_patch_artifact_digest": candidate["patch_artifact_digest"],
                "selected_upstream_rank": 1,
            },
            SELECTION_RECEIPT_DIGEST_FIELD,
        )
        request = seal(
            {
                "application_request_id": "application-1",
                "application_request_revision": "r1",
                "source_selection_receipt_digest": selection[SELECTION_RECEIPT_DIGEST_FIELD],
                "selected_candidate_digest": candidate[CANDIDATE_DIGEST_FIELD],
                "source_repository_snapshot_digest": canonical_digest(repository),
                "application_purpose": APPLICATION_PURPOSE,
                "requested_by_actor_id": "actor-1",
                "request_created_epoch": 100,
            },
            REQUEST_DIGEST_FIELD,
        )
        policy = seal(
            {
                "expected_source_selection_receipt_digest": selection[SELECTION_RECEIPT_DIGEST_FIELD],
                "expected_selected_candidate_digest": candidate[CANDIDATE_DIGEST_FIELD],
                "expected_patch_artifact_digest": candidate["patch_artifact_digest"],
                "expected_repository_full_name": "example/repo",
                "expected_source_commit_sha": "a" * 40,
                "expected_source_repository_snapshot_digest": canonical_digest(repository),
                "maximum_source_path_count": 10,
                "maximum_source_snapshot_bytes": 10000,
                "maximum_result_path_count": 10,
                "maximum_result_snapshot_bytes": 10000,
                "maximum_patch_bytes": 10000,
                "maximum_changed_paths": 10,
                "allowed_path_prefixes": ["src"],
                "forbidden_path_prefixes": ["secrets"],
                "allow_additions": True,
                "allow_modifications": True,
                "allow_deletions": True,
                "require_exact_changed_path_accounting": True,
                "evaluation_epoch": 100,
                "maximum_request_age": 10,
            },
            POLICY_DIGEST_FIELD,
        )
        return repository, selected, selection, request, policy

    def build(self, values):
        repository, selected, selection, request, policy = values
        return build_codeai_autonomous_isolated_candidate_application(
            source_selection_receipt=selection,
            selected_candidate=selected,
            repository_files=repository,
            application_request=request,
            application_policy=policy,
        )

    def rebind(self, repository, selected, selection, request, policy):
        candidate = selected.patch_candidate
        selection["selected_candidate_digest"] = candidate[CANDIDATE_DIGEST_FIELD]
        selection["selected_patch_artifact_digest"] = candidate["patch_artifact_digest"]
        selection = seal(selection, SELECTION_RECEIPT_DIGEST_FIELD)
        request["source_selection_receipt_digest"] = selection[SELECTION_RECEIPT_DIGEST_FIELD]
        request["selected_candidate_digest"] = candidate[CANDIDATE_DIGEST_FIELD]
        request = seal(request, REQUEST_DIGEST_FIELD)
        policy["expected_source_selection_receipt_digest"] = selection[SELECTION_RECEIPT_DIGEST_FIELD]
        policy["expected_selected_candidate_digest"] = candidate[CANDIDATE_DIGEST_FIELD]
        policy["expected_patch_artifact_digest"] = candidate["patch_artifact_digest"]
        policy = seal(policy, POLICY_DIGEST_FIELD)
        return repository, selected, selection, request, policy

    def test_valid_modify_add_delete_materializes_snapshot(self):
        result = self.build(self.fixture())
        self.assertEqual(result.status, STATUS_READY)
        self.assertEqual(result.resulting_repository_files, {"src/a.py": 'print("new")\n', "src/b.py": "hello\n"})
        self.assertTrue(result.receipt["verification_workspace_ready"])

    def test_input_snapshot_is_not_mutated(self):
        values = self.fixture()
        before = deepcopy(values[0])
        result = self.build(values)
        self.assertEqual(result.status, STATUS_READY)
        self.assertEqual(values[0], before)
        self.assertFalse(result.receipt["input_repository_snapshot_mutated"])

    def test_selection_receipt_tamper_blocks(self):
        values = list(self.fixture())
        values[2]["selected_candidate_id"] = "tampered"
        result = self.build(tuple(values))
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn("source_selection_receipt_digest_mismatch", result.issues)

    def test_candidate_digest_tamper_blocks(self):
        values = self.fixture()
        values[1].patch_candidate["declared_change_count"] = 4
        result = self.build(values)
        self.assertIn("selected_candidate_digest_mismatch", result.issues)

    def test_artifact_digest_mismatch_blocks(self):
        repository, selected, selection, request, policy = self.fixture()
        selected = SelectedVerificationCandidate(
            selected.candidate_id, selected.upstream_rank, selected.patch_candidate,
            selected.patch_artifact + "\n", selected.candidate_receipt
        )
        result = self.build((repository, selected, selection, request, policy))
        self.assertIn("selected_patch_artifact_digest_mismatch", result.issues)

    def test_snapshot_digest_mismatch_blocks(self):
        values = self.fixture()
        values[0]["src/extra.py"] = "extra\n"
        result = self.build(values)
        self.assertIn("application_request_snapshot_mismatch", result.issues)

    def test_hunk_context_mismatch_blocks(self):
        repository, selected, selection, request, policy = self.fixture()
        artifact = selected.patch_artifact.replace('-print("old")', '-print("other")')
        candidate = dict(selected.patch_candidate)
        candidate["patch_artifact_digest"] = patch_artifact_digest(artifact)
        candidate["patch_size_bytes"] = len(artifact.encode("utf-8"))
        candidate = seal(candidate, CANDIDATE_DIGEST_FIELD)
        selected = SelectedVerificationCandidate(selected.candidate_id, 1, candidate, artifact, selected.candidate_receipt)
        values = self.rebind(repository, selected, selection, request, policy)
        result = self.build(values)
        self.assertTrue(any("deletion_mismatch" in issue for issue in result.issues))

    def test_changed_path_accounting_mismatch_blocks(self):
        repository, selected, selection, request, policy = self.fixture()
        candidate = dict(selected.patch_candidate)
        candidate["changed_paths"] = ["src/a.py", "src/b.py", "src/x.py"]
        candidate["deleted_paths"] = ["src/x.py"]
        candidate = seal(candidate, CANDIDATE_DIGEST_FIELD)
        selected = SelectedVerificationCandidate(selected.candidate_id, 1, candidate, selected.patch_artifact, selected.candidate_receipt)
        result = self.build(self.rebind(repository, selected, selection, request, policy))
        self.assertIn("changed_path_accounting_mismatch", result.issues)

    def test_forbidden_path_blocks(self):
        values = list(self.fixture())
        values[4]["forbidden_path_prefixes"] = ["src/b.py"]
        values[4] = seal(values[4], POLICY_DIGEST_FIELD)
        result = self.build(tuple(values))
        self.assertIn("changed_path_forbidden:src/b.py", result.issues)

    def test_stale_request_blocks(self):
        values = list(self.fixture())
        values[4]["evaluation_epoch"] = 1000
        values[4] = seal(values[4], POLICY_DIGEST_FIELD)
        result = self.build(tuple(values))
        self.assertIn("application_request_window_invalid", result.issues)

    def test_operation_policy_blocks_deletion(self):
        values = list(self.fixture())
        values[4]["allow_deletions"] = False
        values[4] = seal(values[4], POLICY_DIGEST_FIELD)
        result = self.build(tuple(values))
        self.assertIn("deletions_not_allowed", result.issues)

    def test_receipt_grants_no_live_or_git_effect(self):
        result = self.build(self.fixture())
        self.assertEqual(result.status, STATUS_READY)
        for field in (
            "live_repository_patch_applied", "live_repository_files_changed_by_kernel",
            "repository_mutation_performed", "git_ref_changed", "branch_created",
            "commit_created", "push_performed", "pull_request_created", "merge_performed",
            "deployment_performed", "secret_access_performed", "verification_executed",
            "verification_lease_issued", "execution_lease_issued",
            "verification_authority_granted", "execution_authority_granted",
        ):
            self.assertFalse(result.receipt[field], field)


if __name__ == "__main__":
    unittest.main()
