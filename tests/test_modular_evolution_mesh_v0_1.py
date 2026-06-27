from __future__ import annotations

import json
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
import unittest

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPOSITORY_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from kuuos.contracts.module import ModuleContract
from kuuos.kernel.ledger import (
    AppendOnlyLedger,
    LedgerIntegrityError,
    StaleLedgerHeadError,
)
from kuuos.orchestration.dependency_graph import DependencyResolver
from kuuos.orchestration.registry import CapabilityRegistry, RegistryConflictError


MANIFEST_DIRECTORY = REPOSITORY_ROOT / "manifests" / "modules"
EXTERNAL_CAPABILITIES = {
    "kernel.ledger.append",
    "kernel.provenance.resolve",
}


class ModularEvolutionMeshV01Tests(unittest.TestCase):
    def test_builtin_manifests_are_valid_and_registered(self) -> None:
        registry = CapabilityRegistry.from_manifest_directory(MANIFEST_DIRECTORY)
        self.assertEqual(
            (
                "kuuos.memory.core",
                "kuuos.observe.core",
                "kuuos.verify.core",
            ),
            tuple(module.module_id for module in registry.modules),
        )
        self.assertEqual(
            "kuuos.observe.core",
            registry.active_provider("observation.candidate").module_id,
        )
        self.assertEqual(
            "kuuos.verify.core",
            registry.active_provider("verification.disposition").module_id,
        )
        self.assertEqual(
            "kuuos.memory.core",
            registry.active_provider("memory.retrieval").module_id,
        )
        self.assertEqual(64, len(registry.snapshot().digest))

    def test_memory_resolution_builds_observe_verify_memory_order(self) -> None:
        registry = CapabilityRegistry.from_manifest_directory(MANIFEST_DIRECTORY)
        resolver = DependencyResolver(
            registry,
            external_capabilities=EXTERNAL_CAPABILITIES,
        )
        plan = resolver.resolve(["memory.retrieval"])
        self.assertEqual(
            (
                "kuuos.observe.core",
                "kuuos.verify.core",
                "kuuos.memory.core",
            ),
            plan.module_ids,
        )
        self.assertEqual(64, len(plan.digest))

    def test_candidate_module_cannot_claim_effect_execution(self) -> None:
        manifest_path = MANIFEST_DIRECTORY / "observe_core_v0_1.json"
        payload = json.loads(manifest_path.read_text(encoding="utf-8"))
        payload["owns"].append("effect_execution")
        payload["must_not_own"].remove("effect_execution")
        with self.assertRaisesRegex(
            ValueError,
            "authority_surface_ownership_violation",
        ):
            ModuleContract.from_mapping(payload)

    def test_registry_duplicate_replay_is_idempotent_but_conflict_fails(self) -> None:
        manifest_path = MANIFEST_DIRECTORY / "observe_core_v0_1.json"
        payload = json.loads(manifest_path.read_text(encoding="utf-8"))
        contract = ModuleContract.from_mapping(payload)
        registry = CapabilityRegistry()
        self.assertTrue(registry.register(contract))
        self.assertFalse(registry.register(contract))
        changed = dict(payload)
        changed["version"] = "0.1.1"
        with self.assertRaisesRegex(
            RegistryConflictError,
            "module_id_already_registered",
        ):
            registry.register(ModuleContract.from_mapping(changed))

    def test_ledger_append_replay_stale_rejection_and_integrity(self) -> None:
        with TemporaryDirectory() as directory:
            path = Path(directory) / "events.jsonl"
            ledger = AppendOnlyLedger(path)
            first = ledger.append(
                event_id="registry-snapshot-1",
                kind="registry.snapshot.committed",
                payload={"digest": "a" * 64},
            )
            self.assertFalse(first.replayed)
            replay = ledger.append(
                event_id="registry-snapshot-1",
                kind="registry.snapshot.committed",
                payload={"digest": "a" * 64},
            )
            self.assertTrue(replay.replayed)
            with self.assertRaisesRegex(StaleLedgerHeadError, "stale_ledger_head"):
                ledger.append(
                    event_id="dependency-plan-1",
                    kind="dependency.plan.committed",
                    payload={"digest": "b" * 64},
                    expected_head_digest="0" * 64,
                )
            second = ledger.append(
                event_id="dependency-plan-1",
                kind="dependency.plan.committed",
                payload={"digest": "b" * 64},
                expected_head_digest=ledger.head_digest,
            )
            self.assertEqual(2, second.event.sequence)
            self.assertEqual(2, len(ledger.read()))
            lines = path.read_text(encoding="utf-8").splitlines()
            tampered = json.loads(lines[1])
            tampered["payload"]["digest"] = "c" * 64
            lines[1] = json.dumps(tampered, sort_keys=True)
            path.write_text("\n".join(lines) + "\n", encoding="utf-8")
            with self.assertRaisesRegex(
                LedgerIntegrityError,
                "ledger_event_digest_mismatch",
            ):
                ledger.read()


if __name__ == "__main__":
    unittest.main()
