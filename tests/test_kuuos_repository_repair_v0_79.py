from __future__ import annotations

from dataclasses import replace
import unittest

from runtime.kuuos_repository_repair_candidates_v0_79 import generate_repository_repair_candidates
from runtime.kuuos_repository_repair_cycle_v0_79 import run_repository_repair_cycle
from runtime.kuuos_repository_shadow_repair_v0_79 import (
    apply_candidate_to_snapshot,
    evaluate_repository_candidates,
)
from runtime.kuuos_repository_structure_observer_v0_79 import observe_repository_structure
from runtime.kuuos_repository_structure_types_v0_79 import APPLIED, NO_CHANGE, RepositorySnapshot
from tests.kuuos_repository_repair_fixture_v0_79 import defective_repository_snapshot


class RepositoryRepairV079Tests(unittest.TestCase):
    def test_observation_finds_four_structural_defects(self) -> None:
        snapshot = defective_repository_snapshot()
        observation = observe_repository_structure(snapshot)
        self.assertEqual(observation.weighted_defect_score, 70)
        self.assertEqual(len(observation.missing_runtime_validator_registrations), 1)
        self.assertEqual(len(observation.missing_lake_roots), 1)
        self.assertEqual(len(observation.missing_aggregate_imports), 1)
        self.assertEqual(len(observation.direct_pr_trigger_workflows), 1)
        self.assertEqual(observation.missing_referenced_paths, ())

    def test_finite_candidates_all_improve_in_shadow(self) -> None:
        snapshot = defective_repository_snapshot()
        observation = observe_repository_structure(snapshot)
        candidates = generate_repository_repair_candidates(snapshot, observation)
        self.assertEqual(len(candidates), 4)
        evaluated = evaluate_repository_candidates(snapshot, observation, candidates)
        self.assertTrue(all(item[3].admissible for item in evaluated))
        self.assertTrue(all(item[3].strict_improvement for item in evaluated))
        self.assertTrue(all(item[2].protected_paths_preserved for item in evaluated))

    def test_four_cycles_repair_all_registered_structure(self) -> None:
        snapshot = defective_repository_snapshot()
        receipts = []
        for index in range(5):
            snapshot, receipt = run_repository_repair_cycle(
                f"cycle-{index}",
                snapshot,
            )
            receipts.append(receipt)
            if receipt.status == NO_CHANGE:
                break
        final_observation = observe_repository_structure(snapshot)
        self.assertEqual(final_observation.weighted_defect_score, 0)
        self.assertEqual([item.status for item in receipts[:4]], [APPLIED] * 4)
        self.assertEqual(receipts[4].status, NO_CHANGE)
        self.assertTrue(all(not item.external_approval_required for item in receipts))
        self.assertTrue(all(not item.arbitrary_code_generation_used for item in receipts))
        texts = snapshot.texts
        self.assertIn("scripts/check_fixture_v079.py", texts["scripts/run_kuuos_runtime_full_check_v0_55.py"])
        self.assertIn('"FixtureFormalV0_79"', texts["lakefile.toml"])
        self.assertIn("import KUOS.WORLD.FixtureV0_79", texts["formal/KuuOSFormal.lean"])
        self.assertNotIn("pull_request:", texts[".github/workflows/fixture-v079.yml"])

    def test_stale_patch_is_rejected(self) -> None:
        snapshot = defective_repository_snapshot()
        observation = observe_repository_structure(snapshot)
        candidate = generate_repository_repair_candidates(snapshot, observation)[0]
        texts = snapshot.texts
        target = candidate.patches[0].path
        texts[target] = texts[target] + "\n# concurrent change\n"
        stale_snapshot = RepositorySnapshot(
            snapshot.root_label,
            snapshot.all_paths,
            tuple(sorted(texts.items())),
        )
        rebound = replace(candidate, source_snapshot_digest=stale_snapshot.digest)
        with self.assertRaisesRegex(ValueError, "candidate_before_digest_mismatch"):
            apply_candidate_to_snapshot(stale_snapshot, rebound)


if __name__ == "__main__":
    unittest.main()
