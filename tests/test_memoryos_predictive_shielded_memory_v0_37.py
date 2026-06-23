from __future__ import annotations

from copy import deepcopy
import unittest
from unittest.mock import patch

from runtime import kuuos_memoryos_predictive_shielded_memory_v0_37 as kernel


class MemoryOSPredictiveShieldedMemoryV037Tests(unittest.TestCase):
    def source_snapshot(
        self,
        *,
        sequence_index: int = 0,
        digest: str = "source-snapshot-0",
        complete_blockers: bool = True,
    ) -> dict:
        return {
            "memory_snapshot_digest": digest,
            "sequence_index": sequence_index,
            "mission_id": "mission-1",
            "lineage_id": "lineage-1",
            "memory_route": (
                "PRESERVE_BLOCKED_CONTEXT"
                if complete_blockers
                else "QUARANTINE_INCOMPLETE_BLOCKER_EVIDENCE"
            ),
            "qi_context": {
                "process_tensor_trace_digest": "qi-process-trace-1",
            },
            "world_context": {
                "current_world_fragment_digest": "world-fragment-1",
            },
            "blocker_context": {
                "active_blockers": ["execution_authority_blocker"],
                "missing_blockers": (
                    [] if complete_blockers else ["world_identity_blocker"]
                ),
                "blocked_capabilities": [
                    kernel.v035.blocker_v15.BLOCKED_CAPABILITY_BY_BLOCKER[
                        "execution_authority_blocker"
                    ]
                ],
                "all_required_blockers_active": complete_blockers,
            },
        }

    def records(self) -> list[dict]:
        return [
            {
                "record_id": "working-1",
                "memory_type": "working",
                "content_digest": "working-content-1",
                "source_digests": ["source-1"],
                "confidence_milli": 800,
                "uncertainty_milli": 200,
                "status": "WORKING_CONTEXT",
                "truth_claim": False,
                "action_authority": False,
                "overwrite_performed": False,
            },
            {
                "record_id": "episodic-1",
                "memory_type": "episodic",
                "content_digest": "episodic-content-1",
                "source_digests": ["source-1"],
                "confidence_milli": 900,
                "uncertainty_milli": 100,
                "status": "EPISODIC_SOURCE",
                "truth_claim": False,
                "action_authority": False,
                "overwrite_performed": False,
            },
            {
                "record_id": "semantic-1",
                "memory_type": "semantic",
                "content_digest": "semantic-content-1",
                "source_digests": ["source-1", "source-2"],
                "confidence_milli": 650,
                "uncertainty_milli": 350,
                "status": "SEMANTIC_CONSOLIDATION_CANDIDATE",
                "truth_claim": False,
                "action_authority": False,
                "overwrite_performed": False,
            },
            {
                "record_id": "procedural-1",
                "memory_type": "procedural",
                "content_digest": "procedural-content-1",
                "source_digests": ["source-3"],
                "confidence_milli": 600,
                "uncertainty_milli": 400,
                "status": "PROCEDURAL_REUSE_CANDIDATE",
                "truth_claim": False,
                "action_authority": False,
                "overwrite_performed": False,
            },
        ]

    def predictive_state(self, *, sufficient: bool = True) -> dict:
        return {
            "representation_kind": "OBSERVABLE_PREDICTIVE_STATE_CANDIDATE",
            "observable_history_digest": "observable-history-1",
            "prediction_target": "next_observation_distribution",
            "prediction_digest": "prediction-1",
            "uncertainty_milli": 300,
            "history_sufficient": sufficient,
            "latent_state_truth_claim": False,
            "action_authority": False,
        }

    def world_candidates(self) -> list[dict]:
        return [
            {
                "candidate_id": "world-candidate-1",
                "source_world_fragment_digest": "world-fragment-1",
                "counterfactual_digest": "counterfactual-1",
                "uncertainty_milli": 500,
                "truth_claim": False,
                "commit_authority": False,
                "execution_authority": False,
                "replaces_sourced_world": False,
            }
        ]

    def residue(self, *, status: str = "OPEN") -> list[dict]:
        return [
            {
                "residue_id": "residue-1",
                "left_digest": "claim-left-1",
                "right_digest": "claim-right-1",
                "status": status,
                "resolved_by_consolidation": False,
                "silent_collapse": False,
            }
        ]

    def build_capsule(
        self,
        *,
        source_snapshot: dict | None = None,
        records: list[dict] | None = None,
        predictive_state: dict | None = None,
        world_candidates: list[dict] | None = None,
        residue: list[dict] | None = None,
        prior_capsule: dict | None = None,
        created_at_ms: int = 1000,
    ) -> dict:
        with patch.object(
            kernel.v035,
            "validate_memoryos_qi_world_blocker_snapshot",
            return_value=[],
        ):
            return kernel.build_predictive_shielded_memory_capsule(
                source_snapshot=source_snapshot or self.source_snapshot(),
                memory_records=records if records is not None else self.records(),
                predictive_state_candidate=(
                    predictive_state or self.predictive_state()
                ),
                world_imagination_candidates=(
                    world_candidates
                    if world_candidates is not None
                    else self.world_candidates()
                ),
                contradiction_residue=residue if residue is not None else [],
                prior_capsule=prior_capsule,
                created_at_ms=created_at_ms,
            )

    def test_memory_hierarchy_is_separated_without_authority_promotion(self) -> None:
        capsule = self.build_capsule()
        self.assertEqual(
            capsule["capsule_route"],
            "READY_FOR_SHIELDED_RETRIEVAL",
        )
        self.assertEqual(
            capsule["memory_inventory"],
            {"working": 1, "episodic": 1, "semantic": 1, "procedural": 1},
        )
        self.assertEqual(
            capsule["consolidation_candidate_record_ids"],
            ["semantic-1", "procedural-1"],
        )
        self.assertFalse(capsule["automatic_consolidation_performed"])
        self.assertEqual(
            kernel.validate_predictive_shielded_memory_capsule(capsule),
            [],
        )

    def test_semantic_truth_promotion_is_rejected(self) -> None:
        records = self.records()
        records[2]["truth_claim"] = True
        with self.assertRaisesRegex(ValueError, "record_truth_claim_forbidden"):
            self.build_capsule(records=records)

    def test_procedural_execution_promotion_is_rejected(self) -> None:
        records = self.records()
        records[3]["action_authority"] = True
        with self.assertRaisesRegex(ValueError, "record_action_authority_forbidden"):
            self.build_capsule(records=records)

    def test_insufficient_predictive_history_routes_to_reobserve(self) -> None:
        capsule = self.build_capsule(
            predictive_state=self.predictive_state(sufficient=False)
        )
        self.assertEqual(
            capsule["capsule_route"],
            "REOBSERVE_PREDICTIVE_STATE",
        )

    def test_incomplete_blocker_source_routes_to_quarantine(self) -> None:
        capsule = self.build_capsule(
            source_snapshot=self.source_snapshot(complete_blockers=False)
        )
        self.assertEqual(
            capsule["capsule_route"],
            "QUARANTINE_SOURCE_BLOCKER_EVIDENCE",
        )

    def test_open_contradiction_residue_is_preserved(self) -> None:
        capsule = self.build_capsule(residue=self.residue())
        self.assertEqual(
            capsule["capsule_route"],
            "PRESERVE_RESIDUE_WITH_CONTEXT",
        )
        self.assertFalse(
            capsule["contradiction_residue"][0]["resolved_by_consolidation"]
        )

    def test_review_residue_routes_to_review(self) -> None:
        capsule = self.build_capsule(residue=self.residue(status="REVIEW"))
        self.assertEqual(
            capsule["capsule_route"],
            "REVIEW_CONTRADICTION_RESIDUE",
        )

    def test_append_only_record_removal_is_rejected(self) -> None:
        first = self.build_capsule()
        next_source = self.source_snapshot(
            sequence_index=1,
            digest="source-snapshot-1",
        )
        with self.assertRaisesRegex(
            ValueError,
            "memory_records_append_only_violation",
        ):
            self.build_capsule(
                source_snapshot=next_source,
                records=self.records()[1:],
                prior_capsule=first,
                created_at_ms=1001,
            )

    def test_append_only_extension_succeeds(self) -> None:
        first = self.build_capsule()
        records = self.records()
        records.append(
            {
                "record_id": "episodic-2",
                "memory_type": "episodic",
                "content_digest": "episodic-content-2",
                "source_digests": ["source-4"],
                "confidence_milli": 750,
                "uncertainty_milli": 250,
                "status": "EPISODIC_SOURCE",
                "truth_claim": False,
                "action_authority": False,
                "overwrite_performed": False,
            }
        )
        second = self.build_capsule(
            source_snapshot=self.source_snapshot(
                sequence_index=1,
                digest="source-snapshot-1",
            ),
            records=records,
            prior_capsule=first,
            created_at_ms=1001,
        )
        self.assertEqual(second["sequence_index"], 1)
        self.assertEqual(
            second["previous_memory_capsule_digest"],
            first["memory_capsule_digest"],
        )

    def test_world_candidate_cannot_replace_sourced_world(self) -> None:
        candidates = self.world_candidates()
        candidates[0]["replaces_sourced_world"] = True
        with self.assertRaisesRegex(
            ValueError,
            "world_candidate_replaces_sourced_world_forbidden",
        ):
            self.build_capsule(world_candidates=candidates)

    def test_blocked_capability_returns_active_shield_context(self) -> None:
        capsule = self.build_capsule()
        capability = kernel.v035.blocker_v15.BLOCKED_CAPABILITY_BY_BLOCKER[
            "execution_authority_blocker"
        ]
        retrieval = kernel.build_theory_grounded_memory_retrieval(
            capsule=capsule,
            query_id="query-1",
            requested_memory_types=["episodic", "semantic"],
            requested_capabilities=[capability],
            created_at_ms=2000,
        )
        self.assertEqual(
            retrieval["route"],
            "RETURN_CONTEXT_WITH_ACTIVE_SHIELD",
        )
        self.assertEqual(
            retrieval["blocked_requested_capabilities"],
            [capability],
        )
        self.assertFalse(retrieval["automatic_execution"])
        self.assertEqual(
            kernel.validate_theory_grounded_memory_retrieval(retrieval),
            [],
        )

    def test_read_only_retrieval_returns_predictive_candidate(self) -> None:
        capsule = self.build_capsule()
        retrieval = kernel.build_theory_grounded_memory_retrieval(
            capsule=capsule,
            query_id="query-2",
            requested_memory_types=["working", "episodic"],
            requested_capabilities=["read_context"],
            created_at_ms=2001,
        )
        self.assertEqual(
            retrieval["route"],
            "RETURN_PREDICTIVE_CONTEXT_CANDIDATE",
        )
        self.assertTrue(retrieval["candidate_context_only"])
        self.assertFalse(retrieval["truth_claim"])

    def test_capsule_tampering_is_detected(self) -> None:
        capsule = self.build_capsule()
        capsule["blocker_projection"]["memory_may_discharge_blocker"] = True
        errors = kernel.validate_predictive_shielded_memory_capsule(capsule)
        self.assertIn(
            "capsule_blocker_memory_may_discharge_blocker_invalid",
            errors,
        )
        self.assertIn("capsule_digest_invalid", errors)


if __name__ == "__main__":
    unittest.main()
