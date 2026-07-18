from copy import deepcopy
import unittest

import runtime.kuuos_codeai_autonomous_unified_diff_candidates_v0_1 as m
from scripts.check_codeai_autonomous_unified_diff_candidates_v0_1 import (
    load_inputs,
    main as run_route_checker,
)


class CodeAIAutonomousUnifiedDiffCandidatesV01Test(unittest.TestCase):
    def setUp(self):
        self.inputs = load_inputs()

    def build(self, **overrides):
        values = deepcopy(self.inputs)
        values.update(overrides)
        return m.build_codeai_autonomous_unified_diff_candidates(**values)

    def test_generates_and_ranks_multiple_supported_candidates(self):
        result = self.build()
        self.assertEqual(m.STATUS_READY, result.status)
        self.assertEqual(2, len(result.candidates))
        self.assertEqual(1, result.candidates[0].rank)
        self.assertTrue(result.candidates[0].proposal_id.endswith("001"))
        self.assertLessEqual(
            len(result.candidates[0].patch_artifact.encode("utf-8")),
            len(result.candidates[1].patch_artifact.encode("utf-8")),
        )

    def test_generated_artifact_is_git_style_unified_diff(self):
        candidate = self.build().candidates[0]
        artifact = candidate.patch_artifact
        self.assertTrue(artifact.startswith("diff --git a/"))
        self.assertIn("new file mode 100644", artifact)
        self.assertIn("--- /dev/null", artifact)
        self.assertIn("+++ b/docs/CodeAI/", artifact)
        self.assertIn("@@ -0,0 +", artifact)
        self.assertTrue(artifact.endswith("\n"))
        self.assertTrue(candidate.candidate_receipt["candidate_patch_ready"])

    def test_add_modify_delete_rendering_is_deterministic(self):
        repository = {
            "docs/CodeAI/A.md": "old\n",
            "docs/CodeAI/D.md": "delete me\n",
        }
        edits = [
            {"path": "docs/CodeAI/N.md", "operation": "add", "new_content": "new\n"},
            {"path": "docs/CodeAI/A.md", "operation": "modify", "new_content": "changed\n"},
            {"path": "docs/CodeAI/D.md", "operation": "delete", "new_content": None},
        ]
        first = m.render_unified_diff(repository, edits)
        second = m.render_unified_diff(repository, list(reversed(edits)))
        self.assertEqual(first, second)
        artifact, shape, issues = first
        self.assertEqual((), issues)
        assert artifact is not None and shape is not None
        self.assertIn("deleted file mode 100644", artifact)
        self.assertEqual(
            ["docs/CodeAI/A.md", "docs/CodeAI/D.md", "docs/CodeAI/N.md"],
            shape["changed_paths"],
        )

    def test_repository_snapshot_is_not_mutated(self):
        repository = deepcopy(self.inputs["repository_files"])
        before = deepcopy(repository)
        result = self.build(repository_files=repository)
        self.assertEqual(before, repository)
        receipt = result.receipt
        assert receipt is not None
        self.assertTrue(receipt["repository_snapshot_read_only"])
        self.assertFalse(receipt["patch_applied"])
        self.assertFalse(receipt["repository_mutation_performed"])
        self.assertFalse(receipt["git_ref_changed"])

    def test_ranking_does_not_select_or_grant_authority(self):
        receipt = self.build().receipt
        assert receipt is not None
        for field in (
            "candidate_selected",
            "verification_lease_issued",
            "execution_lease_issued",
            "selection_authority_granted",
            "verification_authority_granted",
            "execution_authority_granted",
            "merge_authority_granted",
            "deployment_authority_granted",
            "secret_access_authority_granted",
        ):
            self.assertFalse(receipt[field], field)

    def test_invalid_repository_path_fails_closed(self):
        proposals = deepcopy(self.inputs["proposals"][:1])
        proposals[0]["edits"][0]["path"] = "../escape.md"
        result = self.build(proposals=proposals)
        self.assertEqual(m.STATUS_BLOCKED, result.status)
        self.assertIsNone(result.receipt)
        self.assertIn("proposal[0].edit[0]:path_invalid", result.issues)

    def test_scope_violation_is_rejected_by_candidate_envelope(self):
        proposals = deepcopy(self.inputs["proposals"][:1])
        proposals[0]["edits"][0]["path"] = "runtime/forbidden.py"
        result = self.build(proposals=proposals)
        self.assertEqual(m.STATUS_BLOCKED, result.status)
        self.assertIsNotNone(result.receipt)
        self.assertTrue(
            any("candidate_scope_violation_rejected" in issue for issue in result.issues)
        )

    def test_route_checker(self):
        run_route_checker()


if __name__ == "__main__":
    unittest.main()
