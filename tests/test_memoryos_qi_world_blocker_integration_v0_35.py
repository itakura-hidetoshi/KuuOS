from __future__ import annotations

from copy import deepcopy
import unittest
from unittest.mock import patch

from runtime import kuuos_memoryos_qi_world_blocker_integration_v0_35 as kernel


class MemoryOSQiWorldBlockerIntegrationV035Tests(unittest.TestCase):
    def episode(self) -> dict:
        return {
            "version": "kuuos_nonmarkov_cognitive_episode_v0_23",
            "mission_id": "mission-1",
            "lineage_id": "lineage-1",
            "verification_route": "passed",
            "observation_route": "matched",
            "plan_route": "complete_candidate",
            "process_tensor_trace_digest": "process-trace-1",
            "memory_mode": "history_replay_ready",
            "cognitive_episode_digest": "episode-digest-1",
            "handoff": {
                "qi_process_tensor": {
                    "recoverability_projection": {"recovery_unsafe": False},
                    "process_summary": {
                        "process_history_length": 3,
                        "nonmarkov_memory_visible": True,
                    },
                }
            },
        }

    def source_receipt(self) -> dict:
        return {"cross_cycle_receipt_digest": "cross-cycle-receipt-1"}

    def blocker_certificate(self, *, complete: bool = True) -> dict:
        vector = {name: complete for name in kernel.blocker_v15.BLOCKER_ORDER}
        if complete:
            active = list(kernel.blocker_v15.BLOCKER_ORDER)
            missing = []
        else:
            vector["world_identity_blocker"] = False
            active = [
                name
                for name in kernel.blocker_v15.BLOCKER_ORDER
                if vector[name]
            ]
            missing = ["world_identity_blocker"]
        return {
            "source_cross_cycle_receipt_digest": "cross-cycle-receipt-1",
            "blocker_certificate_digest": "blocker-certificate-1",
            "composed_blocker_vector": vector,
            "active_blockers": active,
            "missing_blockers": missing,
            "all_required_blockers_active": complete,
            "blocked_capabilities": [
                kernel.blocker_v15.BLOCKED_CAPABILITY_BY_BLOCKER[name]
                for name in active
            ],
            "disposition": (
                "BLOCKED_UNLICENSED_CROSS_CYCLE_TRANSITION"
                if complete
                else "QUARANTINE_BLOCKER_EVIDENCE_INCOMPLETE"
            ),
            "contextual_not_root_sovereignty": True,
            "repairable_by_new_evidence": True,
        }

    def world_store(self, *, generation: int = 0, fragment: str = "fragment-0") -> dict:
        body = {
            "store_version": kernel.world_v034.STORE_VERSION,
            "world_store_id": "world-store-1",
            "root_lineage_digest": "root-lineage-1",
            "genesis_world_fragment_digest": "fragment-0",
            "current_world_fragment_digest": fragment,
            "generation": generation,
            "last_commit_digest": "commit-digest-" + str(generation),
            "commits": [{} for _ in range(generation)],
        }
        return {"body": body, "body_digest": "world-store-digest-" + str(generation)}

    def patches(self):
        return (
            patch.object(
                kernel.memory_v023,
                "validate_nonmarkov_cognitive_episode",
                return_value=[],
            ),
            patch.object(
                kernel.blocker_v15,
                "validate_cross_cycle_blocker_certificate",
                return_value=[],
            ),
            patch.object(
                kernel.world_v034,
                "validate_world_store",
                side_effect=lambda envelope: deepcopy(envelope["body"]),
            ),
        )

    def source_only_patches(self):
        return (
            patch.object(
                kernel.memory_v023,
                "validate_nonmarkov_cognitive_episode",
                return_value=[],
            ),
            patch.object(
                kernel.world_v034,
                "validate_world_store",
                side_effect=lambda envelope: deepcopy(envelope["body"]),
            ),
        )

    def build_snapshot(
        self,
        *,
        complete: bool = True,
        generation: int = 0,
        fragment: str = "fragment-0",
        prior_snapshot: dict | None = None,
    ) -> dict:
        p1, p2, p3 = self.patches()
        with p1, p2, p3:
            return kernel.build_memoryos_qi_world_blocker_snapshot(
                cognitive_episode=self.episode(),
                source_cross_cycle_receipt=self.source_receipt(),
                blocker_certificate=self.blocker_certificate(complete=complete),
                world_store=self.world_store(
                    generation=generation,
                    fragment=fragment,
                ),
                prior_snapshot=prior_snapshot,
                created_at_ms=1000 + generation,
            )

    def test_genesis_snapshot_preserves_three_contexts_without_authority(self) -> None:
        snapshot = self.build_snapshot()
        self.assertEqual(snapshot["memory_route"], "PRESERVE_BLOCKED_CONTEXT")
        self.assertEqual(
            snapshot["world_context"]["transition"],
            "GENESIS_MEMORY_PROJECTION",
        )
        self.assertTrue(snapshot["qi_context"]["process_history_preserved"])
        self.assertFalse(
            snapshot["blocker_context"]["memory_may_discharge_blocker"]
        )
        self.assertFalse(snapshot["world_context"]["memory_may_commit_world"])
        self.assertEqual(
            kernel.validate_memoryos_qi_world_blocker_snapshot(snapshot),
            [],
        )

    def test_missing_blocker_evidence_is_quarantined(self) -> None:
        snapshot = self.build_snapshot(complete=False)
        self.assertEqual(
            snapshot["memory_route"],
            "QUARANTINE_INCOMPLETE_BLOCKER_EVIDENCE",
        )
        self.assertEqual(
            snapshot["blocker_context"]["missing_blockers"],
            ["world_identity_blocker"],
        )

    def test_real_incomplete_blocker_certificate_is_quarantined(self) -> None:
        source = {
            "cross_cycle_receipt_digest": "cross-cycle-receipt-incomplete"
        }
        certificate = kernel.blocker_v15.build_cross_cycle_blocker_certificate(source)
        blocker_errors = kernel.blocker_v15.validate_cross_cycle_blocker_certificate(
            source, certificate
        )
        self.assertTrue(blocker_errors)
        self.assertTrue(
            all(
                error.startswith("blocker_") and error.endswith("_inactive")
                for error in blocker_errors
            )
        )
        p1, p2 = self.source_only_patches()
        with p1, p2:
            snapshot = kernel.build_memoryos_qi_world_blocker_snapshot(
                cognitive_episode=self.episode(),
                source_cross_cycle_receipt=source,
                blocker_certificate=certificate,
                world_store=self.world_store(),
                created_at_ms=1100,
            )
        self.assertEqual(
            snapshot["memory_route"],
            "QUARANTINE_INCOMPLETE_BLOCKER_EVIDENCE",
        )
        self.assertTrue(snapshot["blocker_context"]["missing_blockers"])
        self.assertFalse(
            snapshot["blocker_context"]["all_required_blockers_active"]
        )

    def test_real_structural_blocker_corruption_is_rejected(self) -> None:
        source = {
            "cross_cycle_receipt_digest": "cross-cycle-receipt-corrupt"
        }
        certificate = kernel.blocker_v15.build_cross_cycle_blocker_certificate(source)
        certificate["blocked_capabilities"] = ["invented-capability"]
        p1, p2 = self.source_only_patches()
        with p1, p2, self.assertRaisesRegex(
            ValueError,
            "blocker_certificate_invalid",
        ):
            kernel.build_memoryos_qi_world_blocker_snapshot(
                cognitive_episode=self.episode(),
                source_cross_cycle_receipt=source,
                blocker_certificate=certificate,
                world_store=self.world_store(),
                created_at_ms=1101,
            )

    def test_blocked_capability_inventory_mismatch_is_rejected(self) -> None:
        certificate = self.blocker_certificate()
        certificate["blocked_capabilities"] = ["invented-capability"]
        p1, p2, p3 = self.patches()
        with p1, p2, p3, self.assertRaisesRegex(
            ValueError,
            "blocked_capability_inventory_mismatch",
        ):
            kernel.build_memoryos_qi_world_blocker_snapshot(
                cognitive_episode=self.episode(),
                source_cross_cycle_receipt=self.source_receipt(),
                blocker_certificate=certificate,
                world_store=self.world_store(),
                created_at_ms=1102,
            )

    def test_world_generation_advance_is_recorded_append_only(self) -> None:
        first = self.build_snapshot()
        second = self.build_snapshot(
            generation=1,
            fragment="fragment-1",
            prior_snapshot=first,
        )
        self.assertEqual(second["sequence_index"], 1)
        self.assertEqual(
            second["previous_memory_snapshot_digest"],
            first["memory_snapshot_digest"],
        )
        self.assertEqual(
            second["world_context"]["transition"],
            "WORLD_GENERATION_ADVANCED",
        )

    def test_world_fragment_change_without_generation_fails_closed(self) -> None:
        first = self.build_snapshot()
        with self.assertRaisesRegex(
            ValueError,
            "world_fragment_changed_without_generation",
        ):
            self.build_snapshot(
                generation=0,
                fragment="fragment-other",
                prior_snapshot=first,
            )

    def test_retrieval_surfaces_active_capability_blocker(self) -> None:
        snapshot = self.build_snapshot()
        capability = (
            kernel.blocker_v15.BLOCKED_CAPABILITY_BY_BLOCKER[
                "execution_authority_blocker"
            ]
        )
        retrieval = kernel.build_memoryos_conditioned_retrieval(
            snapshot=snapshot,
            requested_capabilities=[capability, "read_context"],
            query_id="query-1",
            created_at_ms=2000,
        )
        self.assertEqual(
            retrieval["route"],
            "RETURN_CONTEXT_WITH_ACTIVE_BLOCKER",
        )
        self.assertEqual(
            retrieval["blocked_requested_capabilities"],
            [capability],
        )
        self.assertFalse(retrieval["automatic_blocker_discharge"])
        self.assertFalse(retrieval["automatic_execution"])
        self.assertEqual(
            kernel.validate_memoryos_conditioned_retrieval(retrieval),
            [],
        )

    def test_incomplete_blocker_certificate_quarantines_retrieval(self) -> None:
        snapshot = self.build_snapshot(complete=False)
        retrieval = kernel.build_memoryos_conditioned_retrieval(
            snapshot=snapshot,
            requested_capabilities=["read_context"],
            query_id="query-2",
            created_at_ms=2001,
        )
        self.assertEqual(retrieval["route"], "QUARANTINE_RETRIEVAL")

    def test_snapshot_tampering_is_detected(self) -> None:
        snapshot = self.build_snapshot()
        snapshot["world_context"]["memory_may_commit_world"] = True
        errors = kernel.validate_memoryos_qi_world_blocker_snapshot(snapshot)
        self.assertIn("snapshot_world_memory_may_commit_world_invalid", errors)
        self.assertIn("snapshot_digest_invalid", errors)


if __name__ == "__main__":
    unittest.main()
