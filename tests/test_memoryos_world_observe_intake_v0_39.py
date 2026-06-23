from __future__ import annotations

from copy import deepcopy
import unittest
from unittest.mock import patch

from runtime import kuuos_memoryos_world_observe_intake_v0_39 as kernel


class MemoryOSWorldObserveIntakeV039Tests(unittest.TestCase):
    def analytic_capsule(
        self,
        *,
        sequence_index: int = 0,
        capsule_digest: str = "analytic-capsule-0",
        route: str = "READY_FOR_READ_ONLY_ANALYTIC_RETRIEVAL",
        residue: bool = False,
    ) -> dict:
        capability = kernel.v038.v037.v035.blocker_v15.BLOCKED_CAPABILITY_BY_BLOCKER[
            "execution_authority_blocker"
        ]
        return {
            "analytic_capsule_digest": capsule_digest,
            "sequence_index": sequence_index,
            "source_memory_capsule_digest": "memory-capsule-38",
            "source_world_fragment_digest": "world-fragment-50",
            "mission_id": "mission-1",
            "lineage_id": "lineage-1",
            "capsule_route": route,
            "memory_projection": {
                "contradiction_residue_ids": ["residue-1"] if residue else [],
            },
            "blocker_projection": {
                "source_memory_route": "PRESERVE_BLOCKED_CONTEXT",
                "active_blockers": ["execution_authority_blocker"],
                "missing_blockers": [],
                "blocked_capabilities": [capability],
                "all_required_blockers_active": True,
                "shield_gate_required": True,
                "memory_may_discharge_blocker": False,
                "safe_fallback_route": "READ_ONLY_CONTEXT_OR_REOBSERVE",
            },
        }

    def candidate_packet(
        self,
        *,
        complete: bool = True,
        candidate_id: str = "world-candidate-1",
        analytic_digest: str = "analytic-capsule-0",
        value_digest: str = "candidate-value-1",
    ) -> dict:
        return {
            "version": kernel.WORLD_CANDIDATE_VERSION,
            "candidate_id": candidate_id,
            "source_analytic_capsule_digest": analytic_digest,
            "source_world_fragment_digest": "world-fragment-50",
            "observation_id_digest": "observation-id-1",
            "observation_context_digest": "observation-context-1",
            "evidence_receipt_digest": "evidence-receipt-1",
            "observable_digest": "observable-1",
            "admissibility_receipt_digest": "admissibility-1",
            "candidate_value_digest": value_digest,
            **{field: complete for field in kernel._REQUIRED_TRUE_FLAGS},
            **{field: False for field in kernel._FORBIDDEN_PACKET_FLAGS},
        }

    def build_capsule(
        self,
        *,
        analytic_capsule: dict | None = None,
        candidate_packet: dict | None = None,
        prior_capsule: dict | None = None,
        created_at_ms: int = 1000,
    ) -> dict:
        with patch.object(
            kernel.v038,
            "validate_memoryos_analytic_hilbert_context_capsule",
            return_value=[],
        ):
            return kernel.build_memoryos_world_observe_intake_capsule(
                analytic_capsule=analytic_capsule or self.analytic_capsule(),
                world_candidate_packet=candidate_packet or self.candidate_packet(),
                prior_capsule=prior_capsule,
                created_at_ms=created_at_ms,
            )

    def test_complete_candidate_routes_to_observe_owner_review(self) -> None:
        capsule = self.build_capsule()
        self.assertEqual(
            capsule["capsule_route"],
            "READY_FOR_OBSERVE_OWNER_REVIEW",
        )
        self.assertTrue(
            capsule["observe_intake_projection"]["raw_evidence_required"]
        )
        self.assertFalse(
            capsule["observe_intake_projection"]["raw_evidence_supplied"]
        )
        self.assertFalse(
            capsule["observe_intake_projection"]["observe_commit_performed"]
        )
        self.assertEqual(
            kernel.validate_memoryos_world_observe_intake_capsule(capsule),
            [],
        )

    def test_incomplete_candidate_is_held(self) -> None:
        capsule = self.build_capsule(
            candidate_packet=self.candidate_packet(complete=False)
        )
        self.assertEqual(
            capsule["capsule_route"],
            "HOLD_INCOMPLETE_WORLD_CANDIDATE",
        )
        self.assertFalse(
            capsule["world_candidate_projection"]["candidate_complete"]
        )

    def test_quarantined_analytic_source_stays_quarantined(self) -> None:
        source = self.analytic_capsule(route="QUARANTINE_MEMORY_SOURCE")
        capsule = self.build_capsule(analytic_capsule=source)
        self.assertEqual(capsule["capsule_route"], "QUARANTINE_ANALYTIC_SOURCE")

    def test_reobserve_analytic_source_stays_reobserve(self) -> None:
        source = self.analytic_capsule(route="REOBSERVE_ANALYTIC_EVIDENCE")
        capsule = self.build_capsule(analytic_capsule=source)
        self.assertEqual(capsule["capsule_route"], "REOBSERVE_ANALYTIC_SOURCE")

    def test_contradiction_residue_is_preserved_for_owner(self) -> None:
        capsule = self.build_capsule(
            analytic_capsule=self.analytic_capsule(residue=True)
        )
        self.assertEqual(
            capsule["capsule_route"],
            "PRESERVE_RESIDUE_FOR_OBSERVE_OWNER",
        )
        self.assertEqual(capsule["contradiction_residue_ids"], ["residue-1"])

    def test_source_world_mismatch_is_rejected(self) -> None:
        packet = self.candidate_packet()
        packet["source_world_fragment_digest"] = "other-world"
        with self.assertRaisesRegex(
            ValueError,
            "world_candidate_source_world_mismatch",
        ):
            self.build_capsule(candidate_packet=packet)

    def test_source_analytic_capsule_mismatch_is_rejected(self) -> None:
        packet = self.candidate_packet(analytic_digest="other-analytic")
        with self.assertRaisesRegex(
            ValueError,
            "world_candidate_analytic_capsule_mismatch",
        ):
            self.build_capsule(candidate_packet=packet)

    def test_observation_and_authority_impersonation_are_rejected(self) -> None:
        for field in (
            "raw_empirical_evidence",
            "observation_record_claim",
            "verification_result_claim",
            "observe_activation_authority",
            "automatic_observe_commit",
            "plan_activation_authority",
            "actos_authority",
            "world_update_authority",
            "memory_overwrite_authority",
        ):
            packet = self.candidate_packet()
            packet[field] = True
            with self.assertRaisesRegex(
                ValueError,
                f"world_candidate_{field}_forbidden",
            ):
                self.build_capsule(candidate_packet=packet)

    def test_successor_preserves_append_only_intake_lineage(self) -> None:
        first = self.build_capsule()
        second_source = self.analytic_capsule(
            sequence_index=1,
            capsule_digest="analytic-capsule-1",
        )
        second_packet = self.candidate_packet(
            candidate_id="world-candidate-2",
            analytic_digest="analytic-capsule-1",
            value_digest="candidate-value-2",
        )
        second = self.build_capsule(
            analytic_capsule=second_source,
            candidate_packet=second_packet,
            prior_capsule=first,
            created_at_ms=1001,
        )
        self.assertEqual(second["sequence_index"], 1)
        self.assertEqual(
            second["previous_intake_capsule_digest"],
            first["intake_capsule_digest"],
        )

    def test_same_sequence_source_substitution_is_rejected(self) -> None:
        first = self.build_capsule()
        source = self.analytic_capsule(capsule_digest="substituted-analytic")
        packet = self.candidate_packet(analytic_digest="substituted-analytic")
        with self.assertRaisesRegex(
            ValueError,
            "intake_source_analytic_changed_without_sequence",
        ):
            self.build_capsule(
                analytic_capsule=source,
                candidate_packet=packet,
                prior_capsule=first,
                created_at_ms=1001,
            )

    def test_same_candidate_identity_substitution_is_rejected(self) -> None:
        first = self.build_capsule()
        source = self.analytic_capsule(
            sequence_index=1,
            capsule_digest="analytic-capsule-1",
        )
        packet = self.candidate_packet(
            analytic_digest="analytic-capsule-1",
            value_digest="substituted-value",
        )
        with self.assertRaisesRegex(
            ValueError,
            "intake_candidate_identity_substituted",
        ):
            self.build_capsule(
                analytic_capsule=source,
                candidate_packet=packet,
                prior_capsule=first,
                created_at_ms=1001,
            )

    def test_blocked_capability_returns_active_shield(self) -> None:
        capsule = self.build_capsule()
        capability = kernel.v038.v037.v035.blocker_v15.BLOCKED_CAPABILITY_BY_BLOCKER[
            "execution_authority_blocker"
        ]
        envelope = kernel.build_memoryos_world_observe_intake_envelope(
            capsule=capsule,
            query_id="query-1",
            requested_capabilities=[capability],
            created_at_ms=2000,
        )
        self.assertEqual(
            envelope["route"],
            "RETURN_CANDIDATE_WITH_ACTIVE_SHIELD",
        )
        self.assertEqual(envelope["blocked_requested_capabilities"], [capability])
        self.assertFalse(envelope["automatic_execution"])

    def test_read_only_owner_intake_creates_no_observation_record(self) -> None:
        capsule = self.build_capsule()
        envelope = kernel.build_memoryos_world_observe_intake_envelope(
            capsule=capsule,
            query_id="query-2",
            requested_capabilities=["read_context"],
            created_at_ms=2001,
        )
        self.assertEqual(
            envelope["route"],
            "RETURN_READ_ONLY_CANDIDATE_TO_OBSERVE_OWNER",
        )
        self.assertEqual(envelope["target_owner"], "ObserveOS")
        self.assertFalse(envelope["raw_empirical_evidence"])
        self.assertFalse(envelope["observation_record_created"])
        self.assertFalse(envelope["verification_result_created"])
        self.assertTrue(envelope["verification_required"])
        self.assertEqual(
            kernel.validate_memoryos_world_observe_intake_envelope(envelope),
            [],
        )

    def test_capsule_tampering_is_detected(self) -> None:
        capsule = self.build_capsule()
        capsule["observe_intake_projection"]["observe_commit_performed"] = True
        errors = kernel.validate_memoryos_world_observe_intake_capsule(capsule)
        self.assertIn(
            "intake_capsule_observe_observe_commit_performed_invalid",
            errors,
        )
        self.assertIn("intake_capsule_digest_invalid", errors)


if __name__ == "__main__":
    unittest.main()
