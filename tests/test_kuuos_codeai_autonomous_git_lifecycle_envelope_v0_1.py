from copy import deepcopy
from pathlib import Path
import subprocess
import tempfile
import unittest

import runtime.kuuos_codeai_autonomous_git_lifecycle_envelope_v0_1 as m
from scripts.check_codeai_autonomous_git_lifecycle_envelope_v0_1 import (
    bind_source,
    checks_state,
    committed_state,
    load_example,
    main as run_route_checker,
    merge_ready_state,
    merged_state,
    pull_request_state,
    pushed_state,
    reseal_request,
    reseal_source,
    reseal_state,
)


class CodeAIAutonomousGitLifecycleEnvelopeV01Test(unittest.TestCase):
    def setUp(self):
        self.example = load_example()

    def build(self, **overrides):
        values = {
            "source_trajectory_receipt": self.example[
                "source_trajectory_receipt"
            ],
            "lifecycle_request": self.example["lifecycle_request"],
            "lifecycle_state": self.example["lifecycle_state"],
            "lifecycle_policy": self.example["lifecycle_policy"],
        }
        values.update(overrides)
        return m.build_codeai_autonomous_git_lifecycle_envelope(**values)

    def test_initial_state_authorizes_only_local_commit(self):
        receipt = self.build().receipt
        assert receipt is not None
        self.assertEqual(
            m.DISPOSITION_LOCAL_COMMIT_AUTHORIZED, receipt["codeai_disposition"]
        )
        self.assertEqual(m.PHASE_LOCAL_COMMIT, receipt["next_effect_phase"])
        self.assertTrue(receipt["local_commit_authority_granted"])
        self.assertTrue(receipt["execution_lease_issued"])
        self.assertTrue(receipt["active_now"])
        self.assertFalse(receipt["push_authority_granted"])
        self.assertFalse(receipt["merge_authority_granted"])

    def test_each_effect_requires_prior_observed_receipt_state(self):
        state = self.example["lifecycle_state"]
        policy = self.example["lifecycle_policy"]
        phases = (
            (committed_state(state), m.PHASE_PUSH),
            (pushed_state(state), m.PHASE_CREATE_PR),
            (pull_request_state(state, draft=True), m.PHASE_MARK_PR_READY),
            (pull_request_state(state, draft=False), m.PHASE_AWAIT_CHECKS),
            (merge_ready_state(state, policy), m.PHASE_MERGE),
            (merged_state(state, policy), m.PHASE_COMPLETE),
        )
        for staged_state, phase in phases:
            with self.subTest(phase=phase):
                receipt = self.build(lifecycle_state=staged_state).receipt
                assert receipt is not None
                self.assertEqual(phase, receipt["next_effect_phase"])

    def test_failed_checks_degrade_without_merge_authority(self):
        policy = self.example["lifecycle_policy"]
        required = sorted(policy["required_check_names"])
        state = checks_state(
            self.example["lifecycle_state"],
            policy,
            successful=[required[0]],
            pending=[],
            failed=[required[1]],
        )
        receipt = self.build(lifecycle_state=state).receipt
        assert receipt is not None
        self.assertEqual(m.DISPOSITION_CHECKS_FAILED, receipt["codeai_disposition"])
        self.assertEqual(m.MODE_DEGRADED_AUTONOMY, receipt["operating_mode"])
        self.assertFalse(receipt["merge_authority_granted"])
        self.assertFalse(receipt["execution_lease_issued"])

    def test_merge_requires_pinned_head_checks_and_mergeability(self):
        policy = self.example["lifecycle_policy"]
        state = merge_ready_state(self.example["lifecycle_state"], policy)
        receipt = self.build(lifecycle_state=state).receipt
        assert receipt is not None
        self.assertEqual(m.DISPOSITION_MERGE_AUTHORIZED, receipt["codeai_disposition"])
        self.assertEqual(m.PHASE_MERGE, receipt["next_effect_phase"])
        self.assertTrue(receipt["merge_authority_granted"])
        self.assertFalse(receipt["push_authority_granted"])

    def test_force_push_admin_bypass_and_branch_deletion_are_rejected(self):
        for field in (
            "force_push_requested",
            "admin_merge_requested",
            "remote_branch_delete_requested",
        ):
            with self.subTest(field=field):
                request = deepcopy(self.example["lifecycle_request"])
                request[field] = True
                request = reseal_request(request)
                receipt = self.build(lifecycle_request=request).receipt
                assert receipt is not None
                self.assertEqual(
                    m.DISPOSITION_DESTRUCTIVE_REJECTED,
                    receipt["codeai_disposition"],
                )
                self.assertFalse(receipt["execution_lease_issued"])

    def test_human_handover_remains_deferred(self):
        request = deepcopy(self.example["lifecycle_request"])
        request["human_handover_requested"] = True
        request = reseal_request(request)
        receipt = self.build(lifecycle_request=request).receipt
        assert receipt is not None
        self.assertEqual(m.DISPOSITION_HANDOVER_DEFERRED, receipt["codeai_disposition"])
        self.assertTrue(receipt["human_handover_deferred"])
        self.assertFalse(receipt["human_handover_performed"])
        self.assertFalse(receipt["external_authority_handover_performed"])

    def test_source_trajectory_is_not_treated_as_git_authority(self):
        receipt = self.build().receipt
        assert receipt is not None
        self.assertFalse(receipt["source_receipt_treated_as_git_authority"])
        self.assertFalse(receipt["checks_treated_as_correctness_proof"])
        self.assertFalse(receipt["merge_treated_as_truth"])
        self.assertFalse(receipt["effect_execution_performed_by_kernel"])

    def test_tampered_state_fails_closed(self):
        state = deepcopy(self.example["lifecycle_state"])
        state["observed_at_epoch"] += 1
        result = self.build(lifecycle_state=state)
        self.assertEqual(m.STATUS_BLOCKED, result.status)
        self.assertIsNone(result.receipt)
        self.assertIn("git_lifecycle_state_digest_mismatch", result.issues)

    def test_isolated_git_commit_and_push_follow_phase_leases(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            remote = root / "remote.git"
            work = root / "work"
            self._git(root, "init", "--bare", str(remote))
            work.mkdir()
            self._git(work, "init")
            self._git(work, "config", "user.name", "KuuOS Test")
            self._git(work, "config", "user.email", "kuuos-test@example.invalid")
            (work / "seed.txt").write_text("seed\n", encoding="utf-8")
            self._git(work, "add", "seed.txt")
            self._git(work, "commit", "-m", "seed")
            self._git(work, "branch", "-M", "main")
            source_sha = self._git(work, "rev-parse", "HEAD").stdout.strip()

            source = deepcopy(self.example["source_trajectory_receipt"])
            source["repository_full_name"] = "isolated/fixture"
            source["source_commit_sha"] = source_sha
            source["resulting_commit_sha"] = source_sha
            source = reseal_source(source)

            request = deepcopy(self.example["lifecycle_request"])
            request["head_branch"] = "agent/integration"
            state = deepcopy(self.example["lifecycle_state"])
            state["head_branch"] = "agent/integration"
            policy = deepcopy(self.example["lifecycle_policy"])
            request, state, policy = bind_source(
                source, request, state, policy
            )

            self._git(work, "switch", "-c", request["head_branch"])
            (work / "change.txt").write_text("change\n", encoding="utf-8")
            local = self.build(
                source_trajectory_receipt=source,
                lifecycle_request=request,
                lifecycle_state=state,
                lifecycle_policy=policy,
            ).receipt
            assert local is not None
            self.assertTrue(local["local_commit_authority_granted"])

            self._git(work, "add", "change.txt")
            self._git(work, "commit", "-m", "bounded change")
            commit_sha = self._git(work, "rev-parse", "HEAD").stdout.strip()
            committed = committed_state(state, commit_sha)
            push = self.build(
                source_trajectory_receipt=source,
                lifecycle_request=request,
                lifecycle_state=committed,
                lifecycle_policy=policy,
            ).receipt
            assert push is not None
            self.assertTrue(push["push_authority_granted"])

            self._git(work, "remote", "add", "origin", str(remote))
            self._git(work, "push", "-u", "origin", request["head_branch"])
            pushed = deepcopy(committed)
            pushed["branch_pushed"] = True
            pushed["pushed_head_sha"] = commit_sha
            pushed = reseal_state(pushed)
            pr = self.build(
                source_trajectory_receipt=source,
                lifecycle_request=request,
                lifecycle_state=pushed,
                lifecycle_policy=policy,
            ).receipt
            assert pr is not None
            self.assertTrue(pr["pull_request_authority_granted"])

    def test_all_disposition_routes(self):
        run_route_checker()

    @staticmethod
    def _git(cwd: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["git", *args],
            cwd=cwd,
            check=True,
            text=True,
            capture_output=True,
        )


if __name__ == "__main__":
    unittest.main()
