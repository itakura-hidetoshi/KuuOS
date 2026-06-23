from __future__ import annotations

from copy import deepcopy
import unittest
from unittest.mock import patch

from runtime import kuuos_memoryos_analytic_hilbert_context_v0_38 as kernel


class MemoryOSAnalyticHilbertContextV038Tests(unittest.TestCase):
    def source_capsule(
        self,
        *,
        sequence_index: int = 0,
        digest: str = "memory-capsule-0",
        route: str = "READY_FOR_SHIELDED_RETRIEVAL",
        residue: list[dict] | None = None,
    ) -> dict:
        return {
            "memory_capsule_digest": digest,
            "sequence_index": sequence_index,
            "predictive_state_digest": "predictive-state-1",
            "source_world_fragment_digest": "world-fragment-1",
            "source_qi_process_tensor_trace_digest": "qi-trace-1",
            "mission_id": "mission-1",
            "lineage_id": "lineage-1",
            "capsule_route": route,
            "memory_records": [
                {
                    "record_id": "episodic-1",
                    "content_digest": "episodic-content-1",
                },
                {
                    "record_id": "semantic-1",
                    "content_digest": "semantic-content-1",
                },
            ],
            "contradiction_residue": residue or [],
            "blocker_projection": {
                "active_blockers": ["execution_authority_blocker"],
                "blocked_capabilities": ["actos_invoke"],
            },
        }

    def analytic_receipt(self) -> dict:
        return {
            "receipt_kind": kernel.RECEIPT_KIND,
            "bridge_version": kernel.ANALYTIC_BRIDGE_VERSION,
            "formal_module_digest": "world-v049-formal-module-digest",
            "os_completion_claim_supplied": True,
            "vacuum_nonzero_theorem_registered": True,
            "runtime_constructed_completion": False,
            "runtime_computed_hilbert_vectors": False,
            "runtime_computed_inner_products": False,
            "runtime_computed_norms": False,
            "runtime_evaluated_vacuum_state": False,
            "runtime_executed_modular_time": False,
            "runtime_executed_physical_time": False,
            "identifies_world_with_vacuum": False,
            "identifies_memory_candidate_with_vacuum": False,
            "identifies_kuu_with_zero": False,
            "truth_authority": False,
            "execution_authority": False,
        }

    def candidates(self) -> list[dict]:
        return [
            {
                "candidate_id": "analytic-context-episodic-1",
                "source_kind": "memory_record",
                "source_id": "episodic-1",
                "source_digest": "episodic-content-1",
                "observable_class_digest": "observable-class-1",
                "hilbert_context_digest": "hilbert-context-1",
                "relation_to_vacuum": kernel.VACUUM_RELATION,
                "candidate_context_only": True,
                "actual_hilbert_vector_claim": False,
                "inner_product_claim": False,
                "norm_claim": False,
                "probability_claim": False,
                "vacuum_identity_claim": False,
                "truth_claim": False,
                "execution_authority": False,
                "plan_activation": False,
            }
        ]

    def build(
        self,
        *,
        source_capsule: dict | None = None,
        receipt: dict | None = None,
        candidates: list[dict] | None = None,
        prior_context: dict | None = None,
        created_at_ms: int = 1000,
    ) -> dict:
        with patch.object(
            kernel.v037,
            "validate_predictive_shielded_memory_capsule",
            return_value=[],
        ):
            return kernel.build_memoryos_analytic_hilbert_context(
                source_capsule=source_capsule or self.source_capsule(),
                analytic_receipt=receipt or self.analytic_receipt(),
                analytic_context_candidates=(
                    candidates if candidates is not None else self.candidates()
                ),
                created_at_ms=created_at_ms,
                prior_context=prior_context,
            )

    def test_read_only_analytic_context_is_bound_to_v037_and_v049(self) -> None:
        context = self.build()
        self.assertEqual(context["route"], "RETURN_READ_ONLY_ANALYTIC_CONTEXT")
        self.assertEqual(
            context["source_memory_capsule_digest"], "memory-capsule-0"
        )
        self.assertEqual(
            context["analytic_receipt"]["bridge_version"],
            kernel.ANALYTIC_BRIDGE_VERSION,
        )
        self.assertFalse(
            context["analytic_receipt"]["runtime_computed_hilbert_vectors"]
        )
        self.assertEqual(
            kernel.validate_memoryos_analytic_hilbert_context(context), []
        )

    def test_memory_candidate_cannot_claim_actual_hilbert_vector(self) -> None:
        candidates = self.candidates()
        candidates[0]["actual_hilbert_vector_claim"] = True
        with self.assertRaisesRegex(
            ValueError, "analytic_candidate_actual_hilbert_vector_claim_forbidden"
        ):
            self.build(candidates=candidates)

    def test_vacuum_identity_promotion_is_rejected(self) -> None:
        candidates = self.candidates()
        candidates[0]["vacuum_identity_claim"] = True
        with self.assertRaisesRegex(
            ValueError, "analytic_candidate_vacuum_identity_claim_forbidden"
        ):
            self.build(candidates=candidates)

    def test_inner_product_claim_is_rejected(self) -> None:
        candidates = self.candidates()
        candidates[0]["inner_product_claim"] = True
        with self.assertRaisesRegex(
            ValueError, "analytic_candidate_inner_product_claim_forbidden"
        ):
            self.build(candidates=candidates)

    def test_blocker_source_routes_to_quarantine(self) -> None:
        capsule = self.source_capsule(route="QUARANTINE_SOURCE_BLOCKER_EVIDENCE")
        context = self.build(source_capsule=capsule)
        self.assertEqual(context["route"], "QUARANTINE_SOURCE_CAPSULE")
        self.assertFalse(
            context["blocker_projection"][
                "analytic_context_may_discharge_blocker"
            ]
        )

    def test_review_residue_routes_to_review(self) -> None:
        capsule = self.source_capsule(route="REVIEW_CONTRADICTION_RESIDUE")
        context = self.build(source_capsule=capsule)
        self.assertEqual(context["route"], "REVIEW_BEFORE_ANALYTIC_CONTEXT")

    def test_open_residue_is_preserved_with_context(self) -> None:
        residue = [
            {
                "residue_id": "residue-1",
                "left_digest": "left-1",
                "right_digest": "right-1",
                "status": "OPEN",
                "resolved_by_consolidation": False,
                "silent_collapse": False,
            }
        ]
        capsule = self.source_capsule(
            route="PRESERVE_RESIDUE_WITH_CONTEXT", residue=residue
        )
        context = self.build(source_capsule=capsule)
        self.assertEqual(
            context["route"], "RETURN_ANALYTIC_CONTEXT_WITH_RESIDUE"
        )
        self.assertEqual(context["contradiction_residue"], residue)

    def test_append_only_candidate_removal_is_rejected(self) -> None:
        first = self.build()
        capsule = self.source_capsule(sequence_index=1, digest="memory-capsule-1")
        with self.assertRaisesRegex(
            ValueError, "analytic_context_candidates_append_only_violation"
        ):
            self.build(
                source_capsule=capsule,
                candidates=[],
                prior_context=first,
                created_at_ms=1001,
            )

    def test_append_only_extension_succeeds(self) -> None:
        first = self.build()
        candidates = self.candidates()
        candidates.append(
            {
                "candidate_id": "analytic-context-predictive-1",
                "source_kind": "predictive_state",
                "source_id": "predictive_state",
                "source_digest": "predictive-state-1",
                "observable_class_digest": "observable-class-2",
                "hilbert_context_digest": "hilbert-context-2",
                "relation_to_vacuum": kernel.VACUUM_RELATION,
                "candidate_context_only": True,
                "actual_hilbert_vector_claim": False,
                "inner_product_claim": False,
                "norm_claim": False,
                "probability_claim": False,
                "vacuum_identity_claim": False,
                "truth_claim": False,
                "execution_authority": False,
                "plan_activation": False,
            }
        )
        second = self.build(
            source_capsule=self.source_capsule(
                sequence_index=1, digest="memory-capsule-1"
            ),
            candidates=candidates,
            prior_context=first,
            created_at_ms=1001,
        )
        self.assertEqual(second["sequence_index"], 1)
        self.assertEqual(
            second["previous_analytic_context_digest"],
            first["analytic_context_digest"],
        )

    def test_source_capsule_substitution_same_sequence_is_rejected(self) -> None:
        first = self.build()
        substituted = self.source_capsule(digest="substituted-capsule")
        with self.assertRaisesRegex(
            ValueError, "source_memory_capsule_substituted_same_sequence"
        ):
            self.build(source_capsule=substituted, prior_context=first)

    def test_analytic_receipt_substitution_is_rejected(self) -> None:
        first = self.build()
        receipt = deepcopy(self.analytic_receipt())
        receipt["formal_module_digest"] = "substituted-formal-module"
        with self.assertRaisesRegex(
            ValueError, "analytic_receipt_changed_within_lineage"
        ):
            self.build(receipt=receipt, prior_context=first)

    def test_tampering_is_detected(self) -> None:
        context = self.build()
        context["blocker_projection"][
            "analytic_context_may_discharge_blocker"
        ] = True
        errors = kernel.validate_memoryos_analytic_hilbert_context(context)
        self.assertIn("analytic_context_blocker_discharge_invalid", errors)
        self.assertIn("analytic_context_digest_invalid", errors)


if __name__ == "__main__":
    unittest.main()
