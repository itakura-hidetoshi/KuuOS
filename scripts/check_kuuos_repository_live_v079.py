#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from runtime.kuuos_repository_snapshot_adapter_v0_79 import capture_explicit_repository_snapshot
from runtime.kuuos_repository_structure_observer_v0_79 import observe_repository_structure

ROOT = Path(__file__).resolve().parents[1]
MANIFESTS = (
    "manifests/kuuos_self_organization_v0_78.json",
    "manifests/kuuos_repository_structure_alignment_v0_79.json",
    "manifests/kuuos_repository_alignment_normal_form_v0_80.json",
    "manifests/kuuos_repository_incremental_preservation_v0_81.json",
    "manifests/kuuos_repository_certificate_chain_v0_82.json",
    "manifests/kuuos_repository_git_revision_adapter_v0_83.json",
    "manifests/kuuos_repository_merge_certificate_v0_84.json",
    "manifests/kuuos_repository_revision_dag_v0_85.json",
    "manifests/kuuos_repository_frontier_certificate_v0_86.json",
    "manifests/kuuos_repository_self_evolution_portfolio_v0_87.json",
    "manifests/kuuos_repository_self_evolution_shadow_v0_88.json",
    "manifests/kuuos_repository_evolution_admission_v0_89.json",
    "manifests/kuuos_repository_external_approval_v0_90.json",
    "manifests/kuuos_repository_application_authorization_v0_91.json",
)
BASE_PATHS = (
    "scripts/run_kuuos_runtime_full_check_v0_55.py",
    "formal/KuuOSFormal.lean",
    "lakefile.toml",
    ".github/workflows/kuuos-self-organization-v078.yml",
)


def contract_paths() -> tuple[str, ...]:
    paths = set(BASE_PATHS + MANIFESTS)
    for manifest in MANIFESTS:
        payload = json.loads((ROOT / manifest).read_text(encoding="utf-8"))
        for key in ("fixture", "tests", "validator", "documentation"):
            value = payload.get(key)
            if isinstance(value, str):
                paths.add(value)
        for value in payload.get("runtime_modules", []):
            if isinstance(value, str):
                paths.add(value)
    return tuple(sorted(paths))


def main() -> int:
    snapshot = capture_explicit_repository_snapshot(ROOT, contract_paths())
    observation = observe_repository_structure(snapshot)
    print(json.dumps(observation.to_dict(), ensure_ascii=False, indent=2))
    return 0 if observation.weighted_defect_score == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
