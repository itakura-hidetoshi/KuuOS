#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from runtime.kuuos_repository_snapshot_adapter_v0_79 import capture_explicit_repository_snapshot
from runtime.kuuos_repository_structure_observer_v0_79 import observe_repository_structure
from scripts.check_kuuos_repository_live_v079 import contract_paths as prior_contract_paths

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = "manifests/kuuos_repository_reference_update_authorization_v0_96.json"
REGISTRY = "ci/check_registry.d/repository_reference_update_authorization_v0_96.json"
RUNTIME_REGISTRY = "ci/check_registry.d/repository_runtime_v0_96.json"


def contract_paths() -> tuple[str, ...]:
    paths = set(prior_contract_paths())
    paths.update((MANIFEST, REGISTRY, RUNTIME_REGISTRY))
    payload = json.loads((ROOT / MANIFEST).read_text(encoding="utf-8"))
    for key in ("tests", "validator", "cumulative_runtime", "documentation"):
        value = payload.get(key)
        if isinstance(value, str):
            paths.add(value)
    for value in payload.get("runtime_modules", []):
        if isinstance(value, str):
            paths.add(value)
    strict_root = payload.get("strict_formal_root")
    if isinstance(strict_root, str):
        paths.add(f"formal/{strict_root}.lean")
    for module in payload.get("aggregate_lean_modules", []):
        if isinstance(module, str):
            paths.add("formal/" + module.replace(".", "/") + ".lean")
    return tuple(sorted(paths))


def main() -> int:
    snapshot = capture_explicit_repository_snapshot(ROOT, contract_paths())
    observation = observe_repository_structure(snapshot)
    print(json.dumps(observation.to_dict(), ensure_ascii=False, indent=2))
    return 0 if observation.weighted_defect_score == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
