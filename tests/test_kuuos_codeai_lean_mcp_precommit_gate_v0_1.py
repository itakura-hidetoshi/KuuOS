"""CodeAI -> Lean MCP -> pinned direct Lean must all agree before a proof edit."""
from __future__ import annotations
from copy import deepcopy
import unittest
from runtime.kuuos_codeai_lean_mcp_precommit_gate_v0_1 import (
    STATUS_READY, STATUS_BLOCKED, digest, evaluate, git_blob, sha256,
)

HEAD, TREE, TARGET = "a"*40, "b"*40, "formal/KUOS/Test.lean"
SOURCE = b"import Mathlib\ntheorem sample : True := by\n  skip\n"
CANDIDATE = b"import Mathlib\ntheorem sample : True := by\n  trivial\n"
LOG = "Lean completed without error\n"


def seal(value, field):
    value = dict(value)
    value[field] = digest(value)
    return value


def evidence():
    o = seal({"source_commit_sha": HEAD, "tree_digest": TREE},
             "codeai_intent_repository_observation_receipt_digest")
    p = seal({"source_observation_receipt_digest": o["codeai_intent_repository_observation_receipt_digest"],
              "source_commit_sha": HEAD, "candidate_patch_digest": "c"*64,
              "patch_artifact_digest": "d"*64, "codeai_disposition": "candidate_patch_supported",
              "patch_candidate_only": True}, "codeai_candidate_patch_receipt_digest")
    g = seal({"source_observation_receipt_digest": o["codeai_intent_repository_observation_receipt_digest"],
              "generated_candidate_digests": [p["candidate_patch_digest"]]},
             "codeai_autonomous_unified_diff_candidates_receipt_digest")
    s = seal({"source_portfolio_receipt_digest": g["codeai_autonomous_unified_diff_candidates_receipt_digest"],
              "selected_candidate_digest": p["candidate_patch_digest"],
              "selected_patch_artifact_digest": p["patch_artifact_digest"], "candidate_selected": True},
             "codeai_autonomous_candidate_selection_receipt_digest")
    a = seal({"source_selection_receipt_digest": s["codeai_autonomous_candidate_selection_receipt_digest"],
              "source_candidate_receipt_digest": p["codeai_candidate_patch_receipt_digest"],
              "source_commit_sha": HEAD, "repository_full_name": "itakura-hidetoshi/KuuOS",
              "changed_paths": [TARGET], "modified_paths": [TARGET], "added_paths": [], "deleted_paths": [],
              "isolated_patch_applied": True, "isolated_snapshot_materialized": True,
              "source_snapshot_verified": True, "selection_correspondence_verified": True,
              "repository_mutation_performed": False, "git_ref_changed": False,
              "live_repository_patch_applied": False, "verification_executed": False, "merge_performed": False,
              "source_repository_snapshot_digest": digest({TARGET: SOURCE.decode()}),
              "resulting_repository_snapshot_digest": digest({TARGET: CANDIDATE.decode()}),
              "resulting_changed_path_digests": [{"path": TARGET, "content_digest": digest(CANDIDATE.decode())}]},
             "codeai_autonomous_isolated_candidate_application_receipt_digest")
    c = {"source_repo": "itakura-hidetoshi/KuuOS", "source_head": HEAD,
         "source_git_tree": TREE, "source_blob": git_blob(SOURCE),
         "candidate_blob": git_blob(CANDIDATE), "git_effect": False,
         "source_observation_receipt": o, "candidate_receipt": p,
         "generated_candidate_receipt": g, "selection_receipt": s,
         "isolated_application_receipt": a}
    m = {"source_head": HEAD, "source_git_blob": git_blob(SOURCE),
         "codeai_candidate_git_blob": git_blob(CANDIDATE),
         "codeai_receipt": a["codeai_autonomous_isolated_candidate_application_receipt_digest"],
         "full_source_status": "SOURCE_OBSERVATION_READY",
         "lean_mcp_status": "LOCAL_FULLSOURCE_AND_LEAN_GREEN_CANDIDATE_ONLY",
         "imports_unchanged": True, "source_signature_unchanged": True,
         "source_restored_by_mcp": True, "source_restored_final": True,
         "new_forbidden_constructs": False, "git_write_performed": False,
         "mcp_local_receipt": {
             "status": "LOCAL_LEAN_GREEN_CANDIDATE_ONLY",
             "original_sha256": sha256(SOURCE), "candidate_sha256": sha256(CANDIDATE),
             "source_restored": True, "git_write_performed": False, "independent_ci_success": False,
             "rounds": [
                 {"round": 0, "source_sha256": sha256(SOURCE), "errors": 1,
                  "goal_digest": "e"*64, "preliminary_tactic_details": [{"snippet": "simp", "goals": ["True"]}]},
                 {"round": 1, "source_sha256": sha256(CANDIDATE), "errors": 0,
                  "semantic_success": True, "partial": False,
                  "direct_lean": {"exit_code": 0}, "forbidden_final_count": 0},
             ],
         },
         "strict_lean_status": "SUCCESS", "strict_lean_returncode": 0,
         "strict_candidate_log_sha256": sha256(LOG.encode())}
    return c, m


class PrecommitGateTests(unittest.TestCase):
    def check(self, c, m, source=SOURCE, candidate=CANDIDATE, log=LOG):
        return evaluate(codeai_record=c, mcp_precommit_record=m, source=source,
                        candidate=candidate, target=TARGET, source_head=HEAD,
                        source_git_tree=TREE, direct_lean_log=log)

    def test_positive_still_disclaims_independent_CI(self):
        c, m = evidence()
        r = self.check(c, m)
        self.assertEqual(r.status, STATUS_READY, r.issues)
        self.assertFalse(r.receipt["independent_ci_certified"])
        self.assertFalse(r.receipt["merge_authority_granted"])

    def test_missing_isolated_codeai_receipt(self):
        c, m = evidence()
        c.pop("isolated_application_receipt")
        self.assertEqual(self.check(c, m).status, STATUS_BLOCKED)

    def test_codeai_receipt_tampering(self):
        c, m = evidence()
        c["isolated_application_receipt"]["changed_paths"] = ["formal/Bad.lean"]
        self.assertIn("isolated_application_receipt:receipt_digest_mismatch", self.check(c, m).issues)

    def test_source_or_candidate_sha_drift(self):
        c, m = evidence()
        self.assertEqual(self.check(c, m, source=SOURCE+b"\n").status, STATUS_BLOCKED)
        self.assertEqual(self.check(c, m, candidate=CANDIDATE+b"\n").status, STATUS_BLOCKED)

    def test_mcp_not_green(self):
        c, m = evidence()
        m["lean_mcp_status"] = "BOUNDED_BUDGET_EXHAUSTED"
        self.assertEqual(self.check(c, m).status, STATUS_BLOCKED)

    def test_mcp_partial_diagnostics(self):
        c, m = evidence()
        m["mcp_local_receipt"]["rounds"][-1]["partial"] = True
        self.assertEqual(self.check(c, m).status, STATUS_BLOCKED)

    def test_mcp_goals_or_multi_attempt_missing(self):
        c, m = evidence()
        m["mcp_local_receipt"]["rounds"][0].pop("goal_digest")
        self.assertEqual(self.check(c, m).status, STATUS_BLOCKED)

    def test_direct_strict_lean_failure(self):
        c, m = evidence()
        m["strict_lean_returncode"] = 1
        self.assertEqual(self.check(c, m).status, STATUS_BLOCKED)
        c, m = evidence()
        self.assertEqual(self.check(c, m, log="error: Lean failed").status, STATUS_BLOCKED)

    def test_imports_or_signatures_drift(self):
        c, m = evidence()
        m["imports_unchanged"] = False
        self.assertEqual(self.check(c, m).status, STATUS_BLOCKED)
        c, m = evidence()
        m["source_signature_unchanged"] = None
        self.assertEqual(self.check(c, m).status, STATUS_BLOCKED)

    def test_NO_DATA_Git_effect_or_HEAD_mismatch(self):
        c, m = evidence()
        m["codeai_receipt"] = "NO_DATA"
        self.assertEqual(self.check(c, m).status, STATUS_BLOCKED)
        c, m = evidence()
        m["git_write_performed"] = True
        self.assertEqual(self.check(c, m).status, STATUS_BLOCKED)
        c, m = evidence()
        m["source_head"] = "f"*40
        self.assertEqual(self.check(c, m).status, STATUS_BLOCKED)


if __name__ == "__main__":
    unittest.main()
