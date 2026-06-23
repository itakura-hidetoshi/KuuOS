from __future__ import annotations

from copy import deepcopy
import unittest
from unittest.mock import patch

from runtime import kuuos_memoryos_analytic_hilbert_context_v0_38 as kernel


class MemoryOSAnalyticHilbertContextV038Tests(unittest.TestCase):
    def memory_capsule(
        self,
        *,
        sequence_index: int = 0,
        capsule_digest: str = "memory-capsule-0",
        route: str = "READY_FOR_SHIELDED_RETRIEVAL",
        residue: bool = False,
    ) -> dict:
        capability = kernel.v037.v035.blocker_v15.BLOCKED_CAPABILITY_BY_BLOCKER[
            "execution_authority_blocker"
        ]
        return {
            "memory_capsule_digest": capsule_digest,
            "sequence_index": sequence_index,
            "source_world_fragment_digest": "world-fragment-49",
            "source_qi_process_tensor_trace_digest": "qi-trace-37",
            "predictive_state_digest": "predictive-state-37",
            "mission_id": "mission-1",
            "lineage_id": "lineage-1",
            "capsule_route": route,
            "memory_inventory": {
                "working": 1,
                "episodic": 1,
                "semantic": 1,
                "procedural": 1,
            },
            "memory_records": [
                {"record_id": "working-1"},
                {"record_id": "episodic-1"},
                {"record_id": "semantic-1"},
                {"record_id": "procedural-1"},
            ],
            "consolidation_candidate_record_ids": ["semantic-1", "procedural-1"],
            "contradiction_residue": (
                [{"residue_id": "residue-1"}] if residue else []
            ),
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

    def analytic_packet(self, *, complete: bool = True) -> dict:
        flags = {
            field: complete for field in kernel._REQUIRED_ANALYTIC_FLAGS
        }
        return {
            "version": kernel.ANALYTIC_PACKET_VERSION,
            "packet_id": "analytic-packet-49",
            "world_bridge_id": kernel.WORLD_BRIDGE_ID,
            "source_world_fragment_digest": "world-fragment-49",
            "positive_time_observable_surface_digest": "positive-surface-49",
            "os_reflection_form_digest": "reflection-form-49",
            "os_hilbert_carrier_digest": "os-hilbert-49",
            "analytic_vacuum_digest": "analytic-vacuum-49",
            "vacuum_state_digest": "vacuum-state-49",
            "physical_hamiltonian_digest": "hamiltonian-49",
            "physical_time_flow_digest": "physical-time-49",
            "modular_time_flow_digest": "modular-time-49",
            "os_vacuum_norm_milli": 1000,
            **flags,
            **{field: False for field in kernel._FORBIDDEN_PACKET_FLAGS},
        }

    def build_capsule(
        self,
        *,
        memory_capsule: dict | None = None,
        analytic_packet: dict | None = None,
        prior_capsule: dict | None = None,
        created_at_ms: int = 1000,
    ) -> dict:
        with patch.object(
            kernel.v037,
            "validate_predictive_shielded_memory_capsule",
            return_value=[],
        ):
            return kernel.build_memoryos_analytic_hilbert_context_capsule(
                memory_capsule=memory_capsule or self.memory_capsule(),
                analytic_packet=analytic_packet or self.analytic_packet(),
                prior_capsule=prior_capsule,
                created_at_ms=created_at_ms,
            )

    def test_complete_packet_builds_read_only_analytic_capsule(self) -> None:
        capsule = self.build_capsule()
        self.assertEqual(
            capsule["capsule_route"],
            "READY_FOR_READ_ONLY_ANALYTIC_RETRIEVAL",
        )
        self.assertTrue(capsule["analytic_projection"]["candidate_context_only"])
        self.assertFalse(capsule["analytic_projection"]["truth_claim"])
        self.assertFalse(capsule["analytic_projection"]["world_update_performed"])
        self.assertEqual(
            kernel.validate_memoryos_analytic_hilbert_context_capsule(capsule),
            [],
        )

    def test_incomplete_analytic_evidence_routes_to_reobserve(self) -> None:
        capsule = self.build_capsule(analytic_packet=self.analytic_packet(complete=False))
        self.assertEqual(capsule["capsule_route"], "REOBSERVE_ANALYTIC_EVIDENCE")
        self.assertFalse(
            capsule["analytic_projection"]["analytic_evidence_complete"]
        )

    def test_quarantined_memory_source_stays_quarantined(self) -> None:
        memory = self.memory_capsule(route="QUARANTINE_SOURCE_BLOCKER_EVIDENCE")
        capsule = self.build_capsule(memory_capsule=memory)
        self.assertEqual(capsule["capsule_route"], "QUARANTINE_MEMORY_SOURCE")

    def test_contradiction_residue_is_preserved(self) -> None:
        capsule = self.build_capsule(memory_capsule=self.memory_capsule(residue=True))
        self.assertEqual(
            capsule["capsule_route"],
            "PRESERVE_RESIDUE_WITH_ANALYTIC_CONTEXT",
        )
        self.assertEqual(
            capsule["memory_projection"]["contradiction_residue_ids"],
            ["residue-1"],
        )

    def test_world_fragment_mismatch_is_rejected(self) -> None:
        packet = self.analytic_packet()
        packet["source_world_fragment_digest"] = "other-world-fragment"
        with self.assertRaisesRegex(
            ValueError,
            "analytic_source_world_fragment_mismatch",
        ):
            self.build_capsule(analytic_packet=packet)

    def test_truth_and_unique_vacuum_promotion_are_rejected(self) -> None:
        packet = self.analytic_packet()
        packet["world_truth_claim"] = True
        with self.assertRaisesRegex(
            ValueError,
            "analytic_packet_world_truth_claim_forbidden",
        ):
            self.build_capsule(analytic_packet=packet)
        packet = self.analytic_packet()
        packet["unique_vacuum_claim"] = True
        with self.assertRaisesRegex(
            ValueError,
            "analytic_packet_unique_vacuum_claim_forbidden",
        ):
            self.build_capsule(analytic_packet=packet)

    def test_runtime_os_completion_and_time_execution_are_rejected(self) -> None:
        packet = self.analytic_packet()
        packet["runtime_constructed_os_completion"] = True
        with self.assertRaisesRegex(
            ValueError,
            "analytic_packet_runtime_constructed_os_completion_forbidden",
        ):
            self.build_capsule(analytic_packet=packet)
        packet = self.analytic_packet()
        packet["runtime_executed_physical_time"] = True
        with self.assertRaisesRegex(
            ValueError,
            "analytic_packet_runtime_executed_physical_time_forbidden",
        ):
            self.build_capsule(analytic_packet=packet)

    def test_source_memory_sequence_regression_is_rejected(self) -> None:
        first = self.build_capsule()
        memory = self.memory_capsule(
            sequence_index=0,
            capsule_digest="memory-capsule-0",
        )
        prior = deepcopy(first)
        prior["source_memory_sequence_index"] = 1
        prior["analytic_capsule_digest"] = kernel.analytic_capsule_digest(prior)
        with self.assertRaisesRegex(
            ValueError,
            "analytic_source_memory_sequence_regressed",
        ):
            self.build_capsule(
                memory_capsule=memory,
                prior_capsule=prior,
                created_at_ms=1001,
            )

    def test_same_sequence_source_substitution_is_rejected(self) -> None:
        first = self.build_capsule()
        memory = self.memory_capsule(capsule_digest="substituted-memory-capsule")
        with self.assertRaisesRegex(
            ValueError,
            "analytic_source_memory_changed_without_sequence",
        ):
            self.build_capsule(
                memory_capsule=memory,
                prior_capsule=first,
                created_at_ms=1001,
            )

    def test_successor_capsule_preserves_analytic_lineage(self) -> None:
        first = self.build_capsule()
        second = self.build_capsule(
            memory_capsule=self.memory_capsule(
                sequence_index=1,
                capsule_digest="memory-capsule-1",
            ),
            prior_capsule=first,
            created_at_ms=1001,
        )
        self.assertEqual(second["sequence_index"], 1)
        self.assertEqual(
            second["previous_analytic_capsule_digest"],
            first["analytic_capsule_digest"],
        )

    def test_blocked_capability_returns_active_shield_context(self) -> None:
        capsule = self.build_capsule()
        capability = kernel.v037.v035.blocker_v15.BLOCKED_CAPABILITY_BY_BLOCKER[
            "execution_authority_blocker"
        ]
        retrieval = kernel.build_memoryos_analytic_hilbert_retrieval(
            capsule=capsule,
            query_id="query-1",
            requested_surfaces=["vacuum_state", "physical_time"],
            requested_capabilities=[capability],
            created_at_ms=2000,
        )
        self.assertEqual(
            retrieval["route"],
            "RETURN_ANALYTIC_CONTEXT_WITH_ACTIVE_SHIELD",
        )
        self.assertEqual(retrieval["blocked_requested_capabilities"], [capability])
        self.assertFalse(retrieval["automatic_execution"])

    def test_read_only_hilbert_retrieval_has_no_truth_or_execution(self) -> None:
        capsule = self.build_capsule()
        retrieval = kernel.build_memoryos_analytic_hilbert_retrieval(
            capsule=capsule,
            query_id="query-2",
            requested_surfaces=["os_hilbert_vacuum", "modular_time"],
            requested_capabilities=["read_context"],
            created_at_ms=2001,
        )
        self.assertEqual(retrieval["route"], "RETURN_READ_ONLY_HILBERT_CONTEXT")
        self.assertTrue(retrieval["read_only_context"])
        self.assertFalse(retrieval["truth_claim"])
        self.assertFalse(retrieval["automatic_world_update"])
        self.assertEqual(
            kernel.validate_memoryos_analytic_hilbert_retrieval(retrieval),
            [],
        )

    def test_unsupported_analytic_surface_is_rejected(self) -> None:
        capsule = self.build_capsule()
        with self.assertRaisesRegex(
            ValueError,
            "requested_analytic_surface_unsupported",
        ):
            kernel.build_memoryos_analytic_hilbert_retrieval(
                capsule=capsule,
                query_id="query-3",
                requested_surfaces=["metaphysical_kuu"],
                requested_capabilities=[],
                created_at_ms=2002,
            )

    def test_capsule_tampering_is_detected(self) -> None:
        capsule = self.build_capsule()
        capsule["analytic_projection"]["truth_claim"] = True
        errors = kernel.validate_memoryos_analytic_hilbert_context_capsule(capsule)
        self.assertIn("analytic_capsule_projection_truth_claim_invalid", errors)
        self.assertIn("analytic_capsule_digest_invalid", errors)


if __name__ == "__main__":
    unittest.main()
