from __future__ import annotations

from dataclasses import replace
from pathlib import Path
import tempfile
import unittest

from runtime.kuuos_repository_checkpoint_evolution_workspace_types_v1_04 import (
    FAILURE_CANDIDATE_BINDING,
    FAILURE_COMPARE_AND_SWAP,
    FAILURE_PATH_CONFLICT,
    FAILURE_PLAN_BINDING,
    TRANSITION_ABORTED,
    TRANSITION_COMMITTED,
    WORKSPACE_MATERIALIZED,
    WORKSPACE_READY,
    repository_checkpoint_evolution_workspace_digest,
    repository_checkpoint_workspace_transition_digest,
)
from runtime.kuuos_repository_checkpoint_evolution_workspace_v1_04 import (
    build_workspace_file,
    build_workspace_operation,
    build_workspace_plan,
    build_workspace_seed,
    execute_repository_checkpoint_workspace_plan,
    fork_repository_checkpoint_evolution_workspace,
    initialize_workspace,
    repository_checkpoint_workspace_diff,
    repository_checkpoint_workspace_transition_issues,
    reset_repository_checkpoint_evolution_workspace,
    workspace_issues,
)
from runtime.kuuos_repository_self_evolution_types_v0_87 import (
    RepositoryEvolutionCandidate,
)
from runtime.v103_receipt_policy import RECEIPT_REJECTED
from runtime.v103_result import checkpoint_receipt_result_digest
from runtime.v104_workspace_export import (
    materialize_repository_checkpoint_evolution_workspace,
)
from runtime.v104_workspace_serialization import (
    repository_checkpoint_evolution_workspace_from_dict,
)
from tests.test_kuuos_repository_checkpoint_creation_receipt_v1_03 import (
    RepositoryCheckpointCreationReceiptV103Tests,
)


class RepositoryCheckpointEvolutionWorkspaceV104Tests(unittest.TestCase):
    def setUp(self) -> None:
        fixture = RepositoryCheckpointCreationReceiptV103Tests(
            methodName="test_committed_receipt_is_deterministic_and_confirmed"
        )
        fixture.setUp()
        self.fixture = fixture
        self.receipt = fixture._certify()
        self.base_files = (
            build_workspace_file("README.md", "base\n"),
            build_workspace_file("old/name.txt", "legacy\n"),
            build_workspace_file("scripts/run.sh", "#!/bin/sh\necho base\n", executable=True),
            build_workspace_file("src/app.py", "print('base')\n"),
        )
        self.seed = build_workspace_seed(
            "checkpoint-workspace-seed-v104",
            self.receipt,
            fixture.result,
            fixture.final_state,
            self.base_files,
        )
        self.workspace = initialize_workspace("workspace-v104-a", self.seed)

    def _file(self, path):
        return next(file for file in self.workspace.files if file.path == path)

    def _plan_candidate(self, operations, *, candidate_id="candidate-v104-a"):
        plan = build_workspace_plan(
            "workspace-plan-v104-a",
            candidate_id,
            self.seed.checkpoint_oid,
            tuple(operations),
        )
        candidate = RepositoryEvolutionCandidate(
            candidate_id=candidate_id,
            source_frontier_commit_sha=self.seed.checkpoint_oid,
            proposal_digest=plan.proposal_digest,
            changed_paths=plan.changed_paths,
            baseline_score=10,
            predicted_score=4,
            risk_score=2,
            reversible=True,
            protected_paths_preserved=True,
            normal_form_preserved=True,
            external_approval_required=False,
        )
        return plan, candidate

    def _full_plan(self):
        old = {file.path: file for file in self.workspace.files}
        operations = (
            build_workspace_operation(
                "op-1",
                "ADD",
                "docs/new.md",
                new_content="# New\n",
            ),
            build_workspace_operation(
                "op-2",
                "DELETE",
                "old/name.txt",
                expected_old_content_digest=old["old/name.txt"].content_digest,
            ),
            build_workspace_operation(
                "op-3",
                "MOVE",
                "scripts/run.sh",
                target_path="bin/run.sh",
                expected_old_content_digest=old["scripts/run.sh"].content_digest,
            ),
            build_workspace_operation(
                "op-4",
                "REPLACE",
                "src/app.py",
                expected_old_content_digest=old["src/app.py"].content_digest,
                new_content="print('evolved')\n",
            ),
        )
        return self._plan_candidate(operations)

    def test_seed_and_initial_workspace_are_deterministic(self) -> None:
        seed = build_workspace_seed(
            self.seed.seed_id,
            self.receipt,
            self.fixture.result,
            self.fixture.final_state,
            reversed(self.base_files),
        )
        workspace = initialize_workspace(self.workspace.workspace_id, seed)
        self.assertEqual(seed, self.seed)
        self.assertEqual(workspace, self.workspace)
        self.assertEqual(workspace.status, WORKSPACE_READY)

    def test_rejected_or_aborted_receipt_cannot_seed_workspace(self) -> None:
        rejected = replace(self.receipt, status=RECEIPT_REJECTED, receipt_digest="")
        rejected = replace(
            rejected,
            receipt_digest=checkpoint_receipt_result_digest(rejected),
        )
        with self.assertRaisesRegex(ValueError, "not_confirmed"):
            build_workspace_seed(
                "bad-seed",
                rejected,
                self.fixture.result,
                self.fixture.final_state,
                self.base_files,
            )
        source_state = self.fixture.fixture._state(current_oid="b" * 40)
        self.fixture.result, self.fixture.final_state, self.fixture.final_registry = (
            self.fixture.fixture._execute(source_checkpoint_state=source_state)
        )
        self.fixture.inputs = self.fixture.fixture._values(
            source_checkpoint_state=source_state
        )
        self.fixture._build_evidence()
        aborted_receipt = self.fixture._certify()
        with self.assertRaisesRegex(ValueError, "not_committed"):
            build_workspace_seed(
                "aborted-seed",
                aborted_receipt,
                self.fixture.result,
                self.fixture.final_state,
                self.base_files,
            )

    def test_atomic_plan_materializes_exact_tree_and_diff(self) -> None:
        plan, candidate = self._full_plan()
        final, transition = execute_repository_checkpoint_workspace_plan(
            "workspace-transition-v104-a",
            self.workspace,
            self.seed,
            candidate,
            plan,
        )
        self.assertEqual(transition.status, TRANSITION_COMMITTED)
        self.assertEqual(final.status, WORKSPACE_MATERIALIZED)
        self.assertEqual(final.sequence_number, 1)
        paths = tuple(file.path for file in final.files)
        self.assertEqual(
            paths,
            ("README.md", "bin/run.sh", "docs/new.md", "src/app.py"),
        )
        self.assertEqual(
            next(file.content for file in final.files if file.path == "src/app.py"),
            "print('evolved')\n",
        )
        self.assertTrue(next(file for file in final.files if file.path == "bin/run.sh").executable)
        diff = repository_checkpoint_workspace_diff(self.seed, final)
        self.assertEqual(diff["added_paths"], ["bin/run.sh", "docs/new.md"])
        self.assertEqual(diff["deleted_paths"], ["old/name.txt", "scripts/run.sh"])
        self.assertEqual(diff["modified_paths"], ["src/app.py"])

    def test_compare_and_swap_failure_preserves_exact_source(self) -> None:
        operation = build_workspace_operation(
            "op-1",
            "REPLACE",
            "src/app.py",
            expected_old_content_digest="b" * 64,
            new_content="bad\n",
        )
        plan, candidate = self._plan_candidate((operation,))
        final, transition = execute_repository_checkpoint_workspace_plan(
            "workspace-transition-v104-cas",
            self.workspace,
            self.seed,
            candidate,
            plan,
        )
        self.assertIs(final, self.workspace)
        self.assertEqual(transition.status, TRANSITION_ABORTED)
        self.assertEqual(transition.failure_kind, FAILURE_COMPARE_AND_SWAP)
        self.assertTrue(transition.source_preserved_on_abort)
        self.assertEqual(transition.sequence_before, transition.sequence_after)

    def test_move_target_conflict_aborts_without_partial_state(self) -> None:
        operation = build_workspace_operation(
            "op-1",
            "MOVE",
            "old/name.txt",
            target_path="README.md",
            expected_old_content_digest=self._file("old/name.txt").content_digest,
        )
        plan, candidate = self._plan_candidate((operation,))
        final, transition = execute_repository_checkpoint_workspace_plan(
            "workspace-transition-v104-conflict",
            self.workspace,
            self.seed,
            candidate,
            plan,
        )
        self.assertIs(final, self.workspace)
        self.assertEqual(transition.failure_kind, FAILURE_PATH_CONFLICT)

    def test_candidate_source_and_proposal_are_exactly_bound(self) -> None:
        plan, candidate = self._full_plan()
        wrong_source = replace(candidate, source_frontier_commit_sha="b" * 40)
        _, source_transition = execute_repository_checkpoint_workspace_plan(
            "workspace-transition-v104-source",
            self.workspace,
            self.seed,
            wrong_source,
            plan,
        )
        self.assertEqual(source_transition.failure_kind, FAILURE_CANDIDATE_BINDING)
        wrong_proposal = replace(candidate, proposal_digest="c" * 64)
        _, proposal_transition = execute_repository_checkpoint_workspace_plan(
            "workspace-transition-v104-proposal",
            self.workspace,
            self.seed,
            wrong_proposal,
            plan,
        )
        self.assertEqual(proposal_transition.failure_kind, FAILURE_PLAN_BINDING)

    def test_plan_rejects_path_conflict_and_traversal(self) -> None:
        with self.assertRaisesRegex(ValueError, "path_conflict"):
            build_workspace_plan(
                "bad-plan",
                "bad-candidate",
                self.seed.checkpoint_oid,
                (
                    build_workspace_operation("op-1", "ADD", "same.txt", new_content="a"),
                    build_workspace_operation("op-2", "ADD", "same.txt", new_content="b"),
                ),
            )
        with self.assertRaisesRegex(ValueError, "not_canonical"):
            build_workspace_file("../escape.txt", "bad")

    def test_reset_restores_seed_and_increments_sequence(self) -> None:
        plan, candidate = self._full_plan()
        final, _ = execute_repository_checkpoint_workspace_plan(
            "workspace-transition-v104-reset-source",
            self.workspace,
            self.seed,
            candidate,
            plan,
        )
        reset = reset_repository_checkpoint_evolution_workspace(final, self.seed)
        self.assertEqual(reset.status, WORKSPACE_READY)
        self.assertEqual(reset.files, self.seed.files)
        self.assertEqual(reset.sequence_number, final.sequence_number + 1)

    def test_forks_evolve_independently(self) -> None:
        left = fork_repository_checkpoint_evolution_workspace("workspace-left", self.seed)
        right = fork_repository_checkpoint_evolution_workspace("workspace-right", self.seed)
        operation = build_workspace_operation("op-1", "ADD", "left.txt", new_content="left")
        plan, candidate = self._plan_candidate((operation,), candidate_id="candidate-left")
        evolved, _ = execute_repository_checkpoint_workspace_plan(
            "workspace-transition-left",
            left,
            self.seed,
            candidate,
            plan,
        )
        self.assertIn("left.txt", tuple(file.path for file in evolved.files))
        self.assertNotIn("left.txt", tuple(file.path for file in right.files))
        self.assertEqual(right.files, self.seed.files)

    def test_filesystem_materialization_writes_exact_files_and_modes(self) -> None:
        plan, candidate = self._full_plan()
        final, _ = execute_repository_checkpoint_workspace_plan(
            "workspace-transition-v104-export",
            self.workspace,
            self.seed,
            candidate,
            plan,
        )
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / "workspace"
            written = materialize_repository_checkpoint_evolution_workspace(
                final,
                destination,
            )
            self.assertEqual(written, tuple(file.path for file in final.files))
            self.assertEqual(
                (destination / "src/app.py").read_text(encoding="utf-8"),
                "print('evolved')\n",
            )
            self.assertEqual((destination / "bin/run.sh").stat().st_mode & 0o777, 0o755)
            self.assertFalse((destination / "old/name.txt").exists())
            with self.assertRaisesRegex(FileExistsError, "destination_exists"):
                materialize_repository_checkpoint_evolution_workspace(final, destination)

    def test_serialized_workspace_round_trip_is_exact(self) -> None:
        plan, candidate = self._full_plan()
        final, _ = execute_repository_checkpoint_workspace_plan(
            "workspace-transition-v104-json",
            self.workspace,
            self.seed,
            candidate,
            plan,
        )
        self.assertEqual(
            repository_checkpoint_evolution_workspace_from_dict(final.to_dict()),
            final,
        )

    def test_workspace_and_transition_tamper_are_detected(self) -> None:
        plan, candidate = self._full_plan()
        final, transition = execute_repository_checkpoint_workspace_plan(
            "workspace-transition-v104-tamper",
            self.workspace,
            self.seed,
            candidate,
            plan,
        )
        tampered_workspace = replace(final, tree_digest="b" * 64, workspace_digest="")
        tampered_workspace = replace(
            tampered_workspace,
            workspace_digest=repository_checkpoint_evolution_workspace_digest(
                tampered_workspace
            ),
        )
        self.assertIn("workspace_tree_digest_mismatch", workspace_issues(tampered_workspace))
        tampered_transition = replace(
            transition,
            sequence_after=transition.sequence_after + 1,
            transition_digest="",
        )
        tampered_transition = replace(
            tampered_transition,
            transition_digest=repository_checkpoint_workspace_transition_digest(
                tampered_transition
            ),
        )
        self.assertIn(
            "workspace_committed_sequence_invalid",
            repository_checkpoint_workspace_transition_issues(tampered_transition),
        )

    def test_same_input_has_same_output_and_seed_is_unchanged(self) -> None:
        plan, candidate = self._full_plan()
        first = execute_repository_checkpoint_workspace_plan(
            "workspace-transition-v104-deterministic",
            self.workspace,
            self.seed,
            candidate,
            plan,
        )
        second = execute_repository_checkpoint_workspace_plan(
            "workspace-transition-v104-deterministic",
            self.workspace,
            self.seed,
            candidate,
            plan,
        )
        self.assertEqual(first, second)
        self.assertEqual(self.seed.files, tuple(sorted(self.base_files, key=lambda item: item.path)))
        self.assertEqual(self.workspace.files, self.seed.files)

    def test_materialized_workspace_is_one_candidate_transition(self) -> None:
        plan, candidate = self._full_plan()
        final, _ = execute_repository_checkpoint_workspace_plan(
            "workspace-transition-v104-once",
            self.workspace,
            self.seed,
            candidate,
            plan,
        )
        unchanged, transition = execute_repository_checkpoint_workspace_plan(
            "workspace-transition-v104-twice",
            final,
            self.seed,
            candidate,
            plan,
        )
        self.assertIs(unchanged, final)
        self.assertEqual(transition.status, TRANSITION_ABORTED)


if __name__ == "__main__":
    unittest.main()
