"""v0.38: five original persisted stores, shared typed four-edge history.

Real v1.3 native OS fixture; no mock validators or Python-only
synthetic success. Original store files are independently replayed.
All checks remain local, not semantic refinement or global descent.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import shutil
from tempfile import TemporaryDirectory
import unittest

from runtime.kuuos_belief_os_types_v0_1 import sha
from runtime.kuuos_plan_os_kernel_v0_1 import build_plan_phase_activation_receipt
from runtime.kuuos_plan_os_store_v0_1 import PlanStore
from runtime.kuuos_qi_world_native_full_cycle_v1_3 import (
    build_native_full_cycle_receipt, validate_native_full_cycle_receipt,
)
from runtime.kuuos_lean_python_plan_act_store_provenance_v0_34 import (
    NUMERIC_AND_ISSUER_OBSTRUCTIONS,
)
from runtime.kuuos_lean_python_five_store_chain_compat_v0_38 import (
    NODES, EDGES, SCOPED_COMPATIBLE, NO_DATA, BLOCKED,
    audit_native_five_store_chain_compatibility,
)


class FiveOriginalStoreChainCompatTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = TemporaryDirectory(prefix="kuuos-v038-five-stores-")
        cls.addClassCleanup(cls.tmp.cleanup)
        cls.root = Path(cls.tmp.name)
        cls.native = build_native_full_cycle_receipt(cls.root)
        assert validate_native_full_cycle_receipt(cls.native) == []
        cls.states = {key: cls.native["native_artifacts"][key] for key in NODES}
        cls.activation = build_plan_phase_activation_receipt(
            state=cls.states["PlanOS"],
            mission_cycle_phase="plan",
            mission_cycle_state_digest=sha("native-full-cycle-plan-phase-state"),
            plan_phase_receipt_digest=sha("native-full-cycle-plan-phase-receipt"),
            now_ms=80_000,
        )
        cls.roots = {
            "PlanOS": cls.root / "plan",
            "ActOS": cls.root / "act",
            "ObserveOS": cls.root / "downstream" / "observe",
            "VerifyOS": cls.root / "downstream" / "verify",
            "LearnOS": cls.root / "downstream" / "learn",
        }

    def audit(self, *, states=None, activation=None, roots=None):
        return audit_native_five_store_chain_compatibility(
            self.states if states is None else states,
            self.activation if activation is None else activation,
            self.roots if roots is None else roots,
        )

    def test_original_five_stores_and_full_receipt_exist(self):
        self.assertEqual(validate_native_full_cycle_receipt(self.native), [])
        self.assertEqual(PlanStore(self.roots["PlanOS"]).recover(),
                         self.states["PlanOS"])
        self.assertEqual(tuple(self.states), NODES)

    def test_original_full_five_store_chain_local_compatibility(self):
        result = self.audit()
        self.assertEqual(result.status, SCOPED_COMPATIBLE, result.issues)
        self.assertTrue(result.five_stores_individually_replayed)
        self.assertTrue(result.four_original_typed_edges_checked)
        self.assertTrue(result.full_native_path_local_conditions_checked)
        self.assertTrue(result.store_bytes_stable_during_audit)
        self.assertEqual(len(result.edge_statuses), len(EDGES))
        self.assertEqual(result.path_audit_status, "SCOPED_PATH_CHECKED")
        self.assertEqual(result.numeric_and_issuer_obstructions,
                         NUMERIC_AND_ISSUER_OBSTRUCTIONS)
        self.assertEqual(len(result.checked_original_store_paths), 15)
        self.assertEqual(len(result.final_native_state_digests), 5)
        self.assertEqual(len(result.persisted_store_commit_counts), 5)
        self.assertTrue(all(count > 0
                            for _, count in result.persisted_store_commit_counts))

    def test_all_original_edges_retained(self):
        self.assertEqual(
            EDGES,
            ("PlanOS->ActOS", "ActOS->ObserveOS",
             "ObserveOS->VerifyOS", "VerifyOS->LearnOS"),
        )
        result = self.audit()
        self.assertEqual(tuple(a for a, _ in result.edge_statuses), EDGES)
        self.assertEqual(len({v for _, v in result.edge_statuses}), 4)

    def test_string_paths_accepted(self):
        roots = {name: str(path) for name, path in self.roots.items()}
        self.assertEqual(self.audit(roots=roots).status, SCOPED_COMPATIBLE)

    def test_real_concrete_path_objects_accepted(self):
        self.assertTrue(all(isinstance(v, Path) for v in self.roots.values()))
        self.assertEqual(self.audit().status, SCOPED_COMPATIBLE)

    def test_custom_path_object_not_converted(self):
        class HostileRoot:
            def __fspath__(self):
                raise AssertionError("untrusted conversion forbidden")
        roots = dict(self.roots, LearnOS=HostileRoot())
        self.assertEqual(self.audit(roots=roots).status, BLOCKED)

    def test_duplicate_nonadjacent_root_blocks(self):
        roots = dict(self.roots, LearnOS=self.roots["PlanOS"])
        self.assertEqual(self.audit(roots=roots).status, BLOCKED)

    def test_activation_receipt_missing_kept_no_data(self):
        result = audit_native_five_store_chain_compatibility(
            self.states, None, self.roots,
        )
        self.assertEqual(result.status, NO_DATA)

    def test_plan_node_missing_kept_no_data(self):
        states = {k: v for k, v in self.states.items() if k != "PlanOS"}
        self.assertEqual(self.audit(states=states).status, NO_DATA)

    def test_missing_learn_store_kept_no_data(self):
        roots = dict(self.roots, LearnOS=self.root / "missing-learn")
        self.assertEqual(self.audit(roots=roots).status, NO_DATA)

    def test_untrusted_named_root_or_state_is_blocked(self):
        self.assertEqual(self.audit(roots={"PlanOS": "x", "other": "y"}).status, BLOCKED)
        states = dict(self.states, UnknownOS={})
        self.assertEqual(self.audit(states=states).status, BLOCKED)

    def test_invalid_state_type_is_blocked(self):
        states = dict(self.states, VerifyOS=[])
        self.assertEqual(self.audit(states=states).status, BLOCKED)

    def test_forged_activation_digest_blocks(self):
        activation = deepcopy(self.activation)
        activation["plan_activation_receipt_digest"] = "forged"
        self.assertEqual(self.audit(activation=activation).status, BLOCKED)

    def test_forged_activation_host_permission_blocks(self):
        activation = deepcopy(self.activation)
        activation["host_license_granted"] = True
        self.assertEqual(self.audit(activation=activation).status, BLOCKED)

    def test_tampering_any_one_original_intermediate_blocks(self):
        fields = (
            ("PlanOS", "plan_state_digest"),
            ("ActOS", "act_state_digest"),
            ("ObserveOS", "observe_state_digest"),
            ("VerifyOS", "verify_state_digest"),
            ("LearnOS", "learn_state_digest"),
        )
        for os_name, digest_field in fields:
            with self.subTest(os=os_name):
                states = deepcopy(self.states)
                states[os_name][digest_field] = "forged"
                self.assertEqual(self.audit(states=states).status, BLOCKED)

    def test_corrupt_original_plan_snapshot_blocks(self):
        with TemporaryDirectory(prefix="kuuos-v038-corrupt-") as temp:
            dst = Path(temp) / "plan"
            shutil.copytree(self.roots["PlanOS"], dst)
            path = dst / "plan-snapshot.json"
            obj = json.loads(path.read_text(encoding="utf-8"))
            obj["plan_state_digest"] = "forged"
            path.write_text(json.dumps(obj), encoding="utf-8")
            self.assertEqual(self.audit(roots=dict(self.roots, PlanOS=dst)).status,
                             BLOCKED)

    def test_corrupt_original_plan_ledger_blocks(self):
        with TemporaryDirectory(prefix="kuuos-v038-corrupt-") as temp:
            dst = Path(temp) / "plan"
            shutil.copytree(self.roots["PlanOS"], dst)
            with (dst / "plan-ledger.jsonl").open("a", encoding="utf-8") as handle:
                handle.write("{}\n")
            self.assertEqual(self.audit(roots=dict(self.roots, PlanOS=dst)).status,
                             BLOCKED)

    def test_any_original_store_missing_ledger_retains_no_data(self):
        for name, ledger in (
            ("PlanOS", "plan-ledger.jsonl"),
            ("ActOS", "act-ledger.jsonl"),
            ("ObserveOS", "observe-ledger.jsonl"),
            ("VerifyOS", "verify-ledger.jsonl"),
            ("LearnOS", "learn-ledger.jsonl"),
        ):
            with self.subTest(os=name):
                with TemporaryDirectory(prefix="kuuos-v038-missing-") as temp:
                    dst = Path(temp) / name
                    shutil.copytree(self.roots[name], dst)
                    (dst / ledger).unlink()
                    result = self.audit(roots=dict(self.roots, **{name: dst}))
                    self.assertEqual(result.status, NO_DATA, result.issues)

    def test_store_root_symlink_cannot_be_trusted(self):
        with TemporaryDirectory(prefix="kuuos-v038-link-") as temp:
            link = Path(temp) / "plan"
            link.symlink_to(self.roots["PlanOS"], target_is_directory=True)
            self.assertEqual(self.audit(
                roots=dict(self.roots, PlanOS=link)).status, BLOCKED)

    def test_store_file_symlink_cannot_be_trusted(self):
        with TemporaryDirectory(prefix="kuuos-v038-link-") as temp:
            dst = Path(temp) / "learn"
            shutil.copytree(self.roots["LearnOS"], dst)
            ledger = dst / "learn-ledger.jsonl"
            ledger.unlink()
            ledger.symlink_to(self.roots["LearnOS"] / "learn-ledger.jsonl")
            self.assertEqual(self.audit(
                roots=dict(self.roots, LearnOS=dst)).status, BLOCKED)

    def test_no_original_file_writes_and_no_host_reexecution(self):
        before = {
            str(p.relative_to(self.root)): p.read_bytes()
            for p in self.root.rglob("*") if p.is_file()
        }
        self.assertEqual(self.audit().status, SCOPED_COMPATIBLE)
        after = {
            str(p.relative_to(self.root)): p.read_bytes()
            for p in self.root.rglob("*") if p.is_file()
        }
        self.assertEqual(before, after)

    def test_no_promotion_to_formal_global_truth_or_authority(self):
        result = self.audit()
        self.assertEqual(result.status, SCOPED_COMPATIBLE)
        for name in (
            "external_activation_issuer_authenticated",
            "actual_act_numeric_witnesses_proved",
            "external_receipt_authenticated",
            "global_atomic_snapshot_proved",
            "formal_global_descent_proved",
            "lean_python_semantic_refinement_proved",
            "execution_authority_granted", "truth_authority_granted",
            "causal_authority_granted", "clinical_authority_granted",
            "git_authority_granted", "memory_overwrite_authority_granted",
            "future_learning_activated_now", "original_store_mutated",
        ):
            self.assertIs(getattr(result, name), False, name)


if __name__ == "__main__":
    unittest.main()
