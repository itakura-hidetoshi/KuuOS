from __future__ import annotations

import json
from pathlib import Path

from runtime.kuuos_memoryos_qi_world_blocker_integration_v0_35 import (
    BOUNDARY,
    NON_AUTHORITY,
    RETRIEVAL_VERSION,
    SNAPSHOT_VERSION,
    VERSION,
)

ROOT = Path(__file__).resolve().parents[1]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    require(
        VERSION == "kuuos_memoryos_qi_world_blocker_integration_v0_35",
        "version mismatch",
    )
    require(
        SNAPSHOT_VERSION == "memoryos_qi_world_blocker_snapshot_v0_35",
        "snapshot version mismatch",
    )
    require(
        RETRIEVAL_VERSION == "memoryos_qi_world_blocker_retrieval_v0_35",
        "retrieval version mismatch",
    )

    for field in (
        "grants_execution_authority",
        "grants_truth_authority",
        "grants_blocker_discharge_authority",
        "grants_world_commit_authority",
        "grants_memory_overwrite_authority",
    ):
        require(NON_AUTHORITY[field] is False, f"authority boundary lost: {field}")

    for field in (
        "qi_history_preserved",
        "blocker_certificate_preserved_as_context",
        "memory_cannot_discharge_blocker",
        "missing_blocker_evidence_fails_closed",
        "world_store_is_exact_source_not_truth",
        "world_generation_history_is_append_only",
        "memory_projection_is_read_only",
        "candidate_world_not_collapsed_to_fact",
    ):
        require(BOUNDARY[field] is True, f"boundary lost: {field}")

    manifest_path = (
        ROOT / "manifests/kuuos_memoryos_qi_world_blocker_integration_v0_35.json"
    )
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    require(manifest["version"] == VERSION, "manifest version mismatch")
    require(manifest["runtime_kernel"].endswith("_v0_35.py"), "runtime not registered")
    require(manifest["memory_append_only"] is True, "append-only flag missing")
    require(
        manifest["memory_can_discharge_blocker"] is False,
        "memory blocker discharge must remain forbidden",
    )
    require(
        manifest["memory_can_commit_world"] is False,
        "MemoryOS WORLD commit authority must remain forbidden",
    )

    runtime = (
        ROOT / "runtime/kuuos_memoryos_qi_world_blocker_integration_v0_35.py"
    ).read_text(encoding="utf-8")
    for phrase in (
        "inactive_errors = {",
        "structural_errors = [",
        "QUARANTINE_BLOCKER_EVIDENCE_INCOMPLETE",
        "blocked_capability_inventory_mismatch",
    ):
        require(phrase in runtime, f"runtime quarantine boundary missing: {phrase}")

    documentation = (
        ROOT / "docs/KUUOS_MEMORYOS_QI_WORLD_BLOCKER_INTEGRATION_v0_35.md"
    ).read_text(encoding="utf-8")
    for phrase in (
        "Qi process history ≠ current snapshot",
        "structurally exact inactive evidence → quarantine",
        "structurally inconsistent evidence → reject",
        "blocker memory ≠ blocker discharge",
        "WORLD-store commit ≠ truth",
        "MemoryOS retrieval ≠ execution authority",
    ):
        require(phrase in documentation, f"documentation boundary missing: {phrase}")

    tests = (
        ROOT / "tests/test_memoryos_qi_world_blocker_integration_v0_35.py"
    ).read_text(encoding="utf-8")
    for phrase in (
        "test_real_incomplete_blocker_certificate_is_quarantined",
        "test_real_structural_blocker_corruption_is_rejected",
        "test_blocked_capability_inventory_mismatch_is_rejected",
    ):
        require(phrase in tests, f"regression test missing: {phrase}")

    formal = (
        ROOT
        / "formal/KUOS/OpenHorizon/MemoryOSQiWorldBlockerIntegrationKernelV0_35.lean"
    ).read_text(encoding="utf-8")
    require(
        "memoryos_qi_world_blocker_integration_boundary" in formal,
        "formal boundary theorem missing",
    )
    require(
        "memory_cannot_discharge_blocker" in formal,
        "formal blocker theorem missing",
    )

    root = (ROOT / "formal/KUOS.lean").read_text(encoding="utf-8")
    require(
        "import KUOS.OpenHorizon.MemoryOSQiWorldBlockerIntegrationKernelV0_35"
        in root,
        "formal root import missing",
    )

    print("MemoryOS Qi-WORLD blocker integration v0.35 checks passed")


if __name__ == "__main__":
    main()
