#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from runtime import kuuos_memoryos_predictive_shielded_memory_v0_37 as memory_kernel
from runtime.kuuos_observe_os_fixture_v0_1 import prepared_assessed_state, source_act_state
from runtime.kuuos_verify_os_fixture_v0_1 import prepared_corroborated_state
from runtime.kuuos_os_associated_fields_v0_61 import (
    project_bound_os_triplet,
    project_memory_capsule,
    project_observe_state,
    project_verify_state,
)
from runtime.v01_observe_os_effect_grounded_observation import _finish as finish_observe
from runtime.v01_verify_os_evidence_bound_verification import _finish as finish_verify


class OSGaugeAssociatedFieldsV061Tests(unittest.TestCase):
    def committed_observe(self, root: Path) -> dict:
        act_state = source_act_state(root / "act")
        store, state = prepared_assessed_state(
            root=root / "observe",
            observe_id="observe-v061",
            act_state=act_state,
        )
        committed, _ = finish_observe(
            store=store,
            state=state,
            verdict="MATCHED",
            tick=10,
        )
        return committed

    def committed_verify(self, root: Path, observe_state: dict) -> dict:
        store, state = prepared_corroborated_state(
            root=root / "verify",
            verify_id="verify-v061",
            observe_state=observe_state,
        )
        committed, _ = finish_verify(
            store=store,
            state=state,
            verdict="PASSED",
            criterion_satisfied=True,
            tick=4,
        )
        return committed

    def memory_capsule(self, verify_state: dict, *, bind_verify: bool = True) -> dict:
        verify_digest = verify_state["verify_state_digest"]
        records = [
            {
                "record_id": "episodic-v061",
                "memory_type": "episodic",
                "content_digest": "episodic-content-v061",
                "source_digests": [verify_digest if bind_verify else "unbound-source"],
                "confidence_milli": 900,
                "uncertainty_milli": 100,
                "status": "EPISODIC_SOURCE",
                "truth_claim": False,
                "action_authority": False,
                "overwrite_performed": False,
            },
            {
                "record_id": "semantic-v061",
                "memory_type": "semantic",
                "content_digest": "semantic-content-v061",
                "source_digests": [verify_digest if bind_verify else "unbound-source-2"],
                "confidence_milli": 700,
                "uncertainty_milli": 300,
                "status": "SEMANTIC_CONSOLIDATION_CANDIDATE",
                "truth_claim": False,
                "action_authority": False,
                "overwrite_performed": False,
            },
        ]
        source_snapshot = {
            "memory_snapshot_digest": "memory-source-v061",
            "sequence_index": 0,
            "mission_id": "mission-v061",
            "lineage_id": verify_state["lineage_id"],
            "memory_route": "PRESERVE_BLOCKED_CONTEXT",
            "qi_context": {"process_tensor_trace_digest": "qi-trace-v061"},
            "world_context": {"current_world_fragment_digest": "world-v061"},
            "blocker_context": {
                "active_blockers": ["execution_authority_blocker"],
                "missing_blockers": [],
                "blocked_capabilities": [
                    memory_kernel.v035.blocker_v15.BLOCKED_CAPABILITY_BY_BLOCKER[
                        "execution_authority_blocker"
                    ]
                ],
                "all_required_blockers_active": True,
            },
        }
        predictive = {
            "representation_kind": "OBSERVABLE_PREDICTIVE_STATE_CANDIDATE",
            "observable_history_digest": "history-v061",
            "prediction_target": "next_observation_distribution",
            "prediction_digest": "prediction-v061",
            "uncertainty_milli": 250,
            "history_sufficient": True,
            "latent_state_truth_claim": False,
            "action_authority": False,
        }
        with patch.object(
            memory_kernel.v035,
            "validate_memoryos_qi_world_blocker_snapshot",
            return_value=[],
        ):
            return memory_kernel.build_predictive_shielded_memory_capsule(
                source_snapshot=source_snapshot,
                memory_records=records,
                predictive_state_candidate=predictive,
                world_imagination_candidates=[],
                contradiction_residue=[],
                created_at_ms=130_000,
            )

    def test_committed_os_states_project_to_distinct_associated_fields(self) -> None:
        with tempfile.TemporaryDirectory(prefix="kuuos-os-gauge-v061-") as temporary:
            root = Path(temporary)
            observe = self.committed_observe(root)
            verify = self.committed_verify(root, observe)
            memory = self.memory_capsule(verify)
            triplet = project_bound_os_triplet(
                observe_state=observe,
                verify_state=verify,
                memory_capsule=memory,
            )
        self.assertEqual(set(triplet), {"observe", "verify", "memory"})
        self.assertEqual(triplet["observe"].field.owner, "ObserveOS")
        self.assertEqual(triplet["verify"].field.owner, "VerifyOS")
        self.assertEqual(triplet["memory"].field.owner, "MemoryOS")
        for field in triplet.values():
            self.assertEqual(field.values[:4], (1.0, 1.0, 1.0, 1.0))
            self.assertEqual(len(field.values), 12)

    def test_projection_preserves_exact_source_digests(self) -> None:
        with tempfile.TemporaryDirectory(prefix="kuuos-os-digest-v061-") as temporary:
            root = Path(temporary)
            observe = self.committed_observe(root)
            verify = self.committed_verify(root, observe)
            memory = self.memory_capsule(verify)
            observe_field = project_observe_state(observe)
            verify_field = project_verify_state(verify)
            memory_field = project_memory_capsule(memory)
        self.assertEqual(observe_field.source_digest, observe["observe_state_digest"])
        self.assertEqual(verify_field.source_digest, verify["verify_state_digest"])
        self.assertEqual(memory_field.source_digest, memory["memory_capsule_digest"])

    def test_memory_requires_exact_verify_source_binding(self) -> None:
        with tempfile.TemporaryDirectory(prefix="kuuos-os-binding-v061-") as temporary:
            root = Path(temporary)
            observe = self.committed_observe(root)
            verify = self.committed_verify(root, observe)
            memory = self.memory_capsule(verify, bind_verify=False)
            with self.assertRaisesRegex(ValueError, "memory_verify_source_binding_missing"):
                project_bound_os_triplet(
                    observe_state=observe,
                    verify_state=verify,
                    memory_capsule=memory,
                )


if __name__ == "__main__":
    unittest.main()
