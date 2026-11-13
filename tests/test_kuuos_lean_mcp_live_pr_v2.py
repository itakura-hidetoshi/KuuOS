#!/usr/bin/env python3
"""Offline contracts for current HEAD, exact coverage, semantic CI-log provenance."""
import unittest

from scripts import check_kuuos_lean_mcp_live_pr_v2 as live

H1, H2, BASE = "a" * 40, "b" * 40, "c" * 40


def pr(head=H1, changed_files=2):
    return {
        "number": 3522, "state": "open", "changed_files": changed_files,
        "head": {"sha": head, "repo": {"full_name": live.REPO}},
        "base": {"sha": BASE},
    }


def files():
    return [
        {"filename": "formal/KUOS/Demo.lean", "sha": "d"*40, "status": "modified"},
        {"filename": "tests/test_example.py", "sha": "e"*40, "status": "added"},
    ]


class SnapshotTests(unittest.TestCase):
    def get(self, endpoint):
        if endpoint == "/pulls/3522":
            return pr()
        if endpoint.startswith("/pulls/3522/files?"):
            return files() if endpoint.endswith("page=1") else []
        raise AssertionError("unexpected endpoint " + endpoint)

    def test_full_changed_source_manifest_and_explicit_authority(self):
        p, meta = live.live_plan(3522, self.get)
        self.assertEqual(p["source_head"], H1)
        self.assertEqual(p["scope"], "all-changed")
        self.assertEqual(p["changed_lean_files"], ["formal/KUOS/Demo.lean"])
        self.assertEqual(p["targets"], [{"path": "formal/KUOS/Demo.lean",
                                           "git_blob_sha": "d" * 40}])
        self.assertEqual(meta["pr_files_total"], 2)
        self.assertFalse(meta["blob_content_verified_locally"])
        self.assertFalse(meta["proof_certified"])
        self.assertFalse(meta["github_write_performed"])

    def test_drift_is_obstruction_not_a_successful_snapshot(self):
        calls = 0
        def get(endpoint):
            nonlocal calls
            if endpoint == "/pulls/3522":
                calls += 1
                return pr(H1 if calls == 1 else H2)
            return files()
        with self.assertRaisesRegex(live.SnapshotObstruction, "moved"):
            live.live_plan(3522, get)

    def test_changed_count_gap_fails_closed(self):
        def get(endpoint):
            return pr(changed_files=3) if endpoint == "/pulls/3522" else files()
        with self.assertRaisesRegex(live.SnapshotObstruction, "count differs"):
            live.live_plan(3522, get)

    def test_deleted_lean_file_fails_closed(self):
        def get(endpoint):
            if endpoint == "/pulls/3522":
                return pr()
            return [{**files()[0], "status": "removed"}, files()[1]]
        with self.assertRaisesRegex(live.SnapshotObstruction, "unsupported"):
            live.live_plan(3522, get)

    def test_source_repo_ambiguity_fails_closed(self):
        q = pr()
        q["head"]["repo"]["full_name"] = "untrusted/fork"
        def get(endpoint):
            return q if endpoint == "/pulls/3522" else files()
        with self.assertRaisesRegex(live.SnapshotObstruction, "repo mismatch"):
            live.live_plan(3522, get)

    def test_duplicate_paths_fails_closed(self):
        def get(endpoint):
            return pr() if endpoint == "/pulls/3522" else [files()[0], files()[0]]
        with self.assertRaisesRegex(live.SnapshotObstruction, "duplicate"):
            live.live_plan(3522, get)


class CIHeadBindingTests(unittest.TestCase):
    def meta(self):
        return {"source_head": H1, "ci_run": None, "ci_log_status": "NO_DATA"}

    def test_exact_completed_head_job_log_bound_without_proof_certification(self):
        def fetch(path):
            if path.startswith("/actions/runs?"):
                return {"workflow_runs": [{
                    "name": "KuuOS PR Governance Gate", "head_sha": H1,
                    "id": 26, "created_at": "2026-11-14T00:00:00Z",
                    "status": "completed", "run_attempt": 1,
                    "conclusion": "failure",
                }]}
            if path.startswith("/actions/runs/26/jobs"):
                return {"jobs": [{
                    "id": 50, "name": "Strict Lean formal validation",
                    "status": "completed", "conclusion": "failure",
                }]}
            raise AssertionError(path)
        meta = self.meta()
        log = live.attach_ci_log(meta, fetch, lambda id: "error: formal/KUOS/Demo.lean:2:4: unknown identifier")
        self.assertTrue(log.startswith("error: formal"))
        self.assertEqual(meta["ci_run"]["source_head"], H1)
        self.assertEqual(meta["ci_run"]["strict_job_conclusion"], "failure")
        self.assertFalse(meta.get("proof_certified", False))
        self.assertIn("NOT_PROOF_CERTIFIED", meta["ci_log_status"])

    def test_ongoing_latest_run_cannot_reuse_stale_success(self):
        def fetch(path):
            return {"workflow_runs": [
                {"name": "KuuOS PR Governance Gate", "head_sha": H1,
                 "id": 27, "status": "in_progress", "created_at": "2026-11-14T01:00:00Z"},
                {"name": "KuuOS PR Governance Gate", "head_sha": H1,
                 "id": 26, "status": "completed", "created_at": "2026-11-13T23:00:00Z"},
            ]}
        meta = self.meta()
        self.assertIsNone(live.attach_ci_log(meta, fetch, lambda _: self.fail("old job must not download")))
        self.assertEqual(meta["ci_log_status"], "NO_DATA_LATEST_EXACT_HEAD_RUN_NOT_COMPLETED")

    def test_other_head_run_ignored(self):
        meta = self.meta()
        log = live.attach_ci_log(
            meta, lambda _: {"workflow_runs": [{
                "name": "KuuOS PR Governance Gate", "head_sha": H2,
                "status": "completed", "id": 30,
            }]}, lambda _: self.fail("wrong head"))
        self.assertIsNone(log)
        self.assertEqual(meta["ci_log_status"], "NO_DATA_NO_EXACT_HEAD_GOVERNANCE_RUN")

    def test_log_over_size_does_not_certify(self):
        meta = self.meta()
        def fetch(path):
            return ({"workflow_runs": [{"name": "KuuOS PR Governance Gate",
                                        "head_sha": H1, "status": "completed",
                                        "id": 26, "created_at": "2026-11-14T00:00:00Z"}]}
                    if "runs?" in path else
                    {"jobs": [{"id": 55, "name": "Strict Lean formal validation",
                               "status": "completed"}]})
        with self.assertRaisesRegex(live.SnapshotObstruction, "byte budget"):
            live.attach_ci_log(meta, fetch, lambda _: "x" * (live.MAX_LOG_BYTES + 1))


if __name__ == "__main__":
    unittest.main(verbosity=2)
