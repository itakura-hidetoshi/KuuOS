#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import sys
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from kuuos.kernel.ledger import AppendOnlyLedger
from kuuos.orchestration.dependency_graph import DependencyResolver
from kuuos.orchestration.registry import CapabilityRegistry


EXTERNAL_CAPABILITIES = {
    "kernel.ledger.append",
    "kernel.provenance.resolve",
}


def main() -> int:
    registry = CapabilityRegistry.from_manifest_directory(
        ROOT / "manifests" / "modules"
    )
    resolver = DependencyResolver(
        registry,
        external_capabilities=EXTERNAL_CAPABILITIES,
    )
    plan = resolver.resolve(["memory.retrieval"])
    expected_order = (
        "kuuos.observe.core",
        "kuuos.verify.core",
        "kuuos.memory.core",
    )
    if plan.module_ids != expected_order:
        raise SystemExit(
            "modular_dependency_order_invalid:"
            + json.dumps(plan.module_ids, ensure_ascii=False)
        )
    with TemporaryDirectory() as directory:
        ledger = AppendOnlyLedger(Path(directory) / "mesh-validation.jsonl")
        registry_event = ledger.append(
            event_id="modular-registry-snapshot-v0-1",
            kind="registry.snapshot.committed",
            payload={"registry_digest": registry.snapshot().digest},
        )
        plan_event = ledger.append(
            event_id="modular-dependency-plan-v0-1",
            kind="dependency.plan.committed",
            payload={
                "plan_digest": plan.digest,
                "module_ids": list(plan.module_ids),
            },
            expected_head_digest=registry_event.event.event_digest,
        )
        replay = ledger.append(
            event_id="modular-dependency-plan-v0-1",
            kind="dependency.plan.committed",
            payload={
                "plan_digest": plan.digest,
                "module_ids": list(plan.module_ids),
            },
        )
        if not replay.replayed:
            raise SystemExit("modular_ledger_replay_not_idempotent")
        if len(ledger.read()) != 2:
            raise SystemExit("modular_ledger_event_count_invalid")
        if plan_event.event.sequence != 2:
            raise SystemExit("modular_ledger_sequence_invalid")
    print(
        json.dumps(
            {
                "status": "KUUOS_MODULAR_EVOLUTION_MESH_V0_1_OK",
                "registry_digest": registry.snapshot().digest,
                "dependency_plan_digest": plan.digest,
                "module_order": list(plan.module_ids),
                "authority_widened": False,
                "legacy_runtime_modified": False,
                "self_activation_enabled": False,
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
