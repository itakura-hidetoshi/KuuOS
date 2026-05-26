#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "manifests" / "qi_process_tensor_review_bundle_manifest_v0_1.json"
RELEASE = ROOT / "packets" / "qi_process_tensor_review_release_packet_v0_1.json"
FINALITY = ROOT / "packets" / "qi_process_tensor_review_finality_packet_v0_1.json"


def load(path: pathlib.Path) -> dict:
    if not path.is_file():
        return {}
    value = json.loads(path.read_text(encoding="utf-8"))
    return value if isinstance(value, dict) else {}


def check_no_authority(name: str, payload: dict, errors: list[str]) -> None:
    if payload.get("authority") != "none":
        errors.append(f"{name}:authority_not_none")
    for key in [
        "grants_execution_authority",
        "grants_probe_execution_authority",
        "grants_next_tick_execution_authority",
        "grants_control_packet_authority",
        "grants_memory_overwrite_authority",
    ]:
        if payload.get(key) is not False:
            errors.append(f"{name}:{key}_not_false")


def main() -> int:
    errors: list[str] = []
    manifest = load(MANIFEST)
    release = load(RELEASE)
    finality = load(FINALITY)
    if not manifest:
        errors.append("manifest_missing")
    if not release:
        errors.append("release_packet_missing")
    if not finality:
        errors.append("finality_packet_missing")

    if release.get("packet_version") != "qi_process_tensor_review_release_packet_v0_1":
        errors.append("release_packet_version_mismatch")
    if release.get("packet_status") != "QI_PROCESS_TENSOR_REVIEW_RELEASE_READY":
        errors.append("release_packet_status_mismatch")
    if release.get("source_manifest") != "manifests/qi_process_tensor_review_bundle_manifest_v0_1.json":
        errors.append("release_source_manifest_mismatch")
    if release.get("release_scope") != "qi-process-tensor-review-only":
        errors.append("release_scope_mismatch")
    if release.get("release_only") is not True or release.get("review_only") is not True or release.get("read_only") is not True:
        errors.append("release_boundary_flags_mismatch")

    if finality.get("packet_version") != "qi_process_tensor_review_finality_packet_v0_1":
        errors.append("finality_packet_version_mismatch")
    if finality.get("packet_status") != "QI_PROCESS_TENSOR_REVIEW_FINALITY_READY":
        errors.append("finality_packet_status_mismatch")
    if finality.get("source_manifest") != "manifests/qi_process_tensor_review_bundle_manifest_v0_1.json":
        errors.append("finality_source_manifest_mismatch")
    if finality.get("source_release_packet") != "packets/qi_process_tensor_review_release_packet_v0_1.json":
        errors.append("finality_source_release_packet_mismatch")
    if finality.get("finality_scope") != "qi-process-tensor-review-only":
        errors.append("finality_scope_mismatch")
    for key in ["finality_only", "release_only", "review_only", "read_only", "additive_only_future", "overwrite_forbidden"]:
        if finality.get(key) is not True:
            errors.append(f"finality:{key}_not_true")

    check_no_authority("manifest", manifest, errors)
    check_no_authority("release", release, errors)
    check_no_authority("finality", finality, errors)

    release_non_claims = set(release.get("non_claims", []))
    finality_non_claims = set(finality.get("non_claims", []))
    if "does_not_execute_probe" not in release_non_claims:
        errors.append("release_non_claim_does_not_execute_probe_missing")
    if "not_a_probe_executor" not in finality_non_claims:
        errors.append("finality_non_claim_not_a_probe_executor_missing")
    if "probe_execution_boundary_remains_closed" not in set(finality.get("finality_claims", [])):
        errors.append("finality_probe_boundary_claim_missing")

    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1
    print("PASS: Qi process tensor review finality packet check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
