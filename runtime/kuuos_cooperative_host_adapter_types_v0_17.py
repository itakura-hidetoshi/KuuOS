#!/usr/bin/env python3
from __future__ import annotations

from typing import Any, Mapping

from runtime.kuuos_context_gauge_atlas_types_v0_13 import sha, without

VERSION = "kuuos_cooperative_host_adapter_v0_17"
PROJECTION_VERSION = "kuuos_cooperative_host_projection_v0_17"
LICENSE_VERSION = "kuuos_cooperative_host_license_v0_17"
TICK_VERSION = "kuuos_cooperative_host_tick_v0_17"
RECEIPT_VERSION = "kuuos_cooperative_host_receipt_v0_17"
READY = "KUUOS_COOPERATIVE_HOST_ADAPTER_V0_17_READY"
BLOCKED = "KUUOS_COOPERATIVE_HOST_ADAPTER_V0_17_BLOCKED"
REPLAYED = "KUUOS_COOPERATIVE_HOST_ADAPTER_V0_17_REPLAYED"

NON_AUTHORITY_FLAGS = {
    "grants_execution_authority": False,
    "grants_truth_authority": False,
    "grants_final_commitment_authority": False,
    "grants_memory_overwrite_authority": False,
    "grants_clinical_authority": False,
    "grants_theorem_authority": False,
    "grants_completed_identity_authority": False,
}

REQUIRED_BOUNDARY = {
    "projection_is_read_only": True,
    "projection_does_not_claim_lease": True,
    "connector_call_inside_runtime_forbidden": True,
    "explicit_host_license_required": True,
    "one_job_per_invocation": True,
    "one_bounded_slice_per_invocation": True,
    "trusted_registry_only": True,
    "source_bundle_digest_binding_required": True,
    "ticket_checkpoint_binding_required": True,
    "duplicate_invocation_idempotent": True,
    "input_bundle_not_overwritten_by_default": True,
    "lower_authority_preserved": True,
    "graph_semantics_forbidden": True,
}


def digest_without(value: Mapping[str, Any], field: str) -> str:
    return sha(without(value, field))


def projection_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "projection_digest")


def license_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "host_license_digest")


def tick_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "host_tick_digest")


def receipt_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "host_receipt_digest")


def invocation_digest(*, invocation_id: str, source_bundle_digest: str, projection: str, worker_id: str) -> str:
    return sha(
        {
            "invocation_id": str(invocation_id),
            "source_bundle_digest": str(source_bundle_digest),
            "projection_digest": str(projection),
            "worker_id": str(worker_id),
        }
    )
