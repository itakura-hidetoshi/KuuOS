from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

from runtime import kuuos_authorized_atomic_world_commit_v0_34 as core

AtomicCommitResult = core.AtomicCommitResult
ZERO_DIGEST = core.ZERO_DIGEST
build_authorized_world_commit_request = core.build_authorized_world_commit_request
initialize_world_store = core.initialize_world_store
make_initial_world_store = core.make_initial_world_store
make_world_commit_authorization_receipt = core.make_world_commit_authorization_receipt
read_world_store = core.read_world_store
validate_atomic_world_commit_receipt = core.validate_atomic_world_commit_receipt
validate_authorized_world_commit_request = core.validate_authorized_world_commit_request
validate_world_commit_authorization_receipt = core.validate_world_commit_authorization_receipt
validate_world_store = core.validate_world_store


def commit_world_fragment_atomic(
    *,
    store_path: Path,
    source_disposition_envelope: Mapping[str, Any],
    authorization_envelope: Mapping[str, Any],
    request_envelope: Mapping[str, Any],
    committed_at_ms: int,
) -> AtomicCommitResult:
    authorization = validate_world_commit_authorization_receipt(authorization_envelope)
    request = validate_authorized_world_commit_request(request_envelope)
    rebuilt = build_authorized_world_commit_request(
        source_disposition_envelope,
        authorization_envelope,
        requested_at_ms=request["requested_at_ms"],
    )
    if rebuilt["body_digest"] != request_envelope.get("body_digest"):
        raise ValueError("world_commit_request_not_exactly_reconstructible")
    if request["authorization_digest"] != authorization_envelope.get("body_digest"):
        raise ValueError("world_commit_request_authorization_mismatch")
    if request["authorization_id"] != authorization["authorization_id"]:
        raise ValueError("world_commit_request_authorization_id_mismatch")

    store = read_world_store(store_path)
    for receipt_envelope in store["body"]["commits"]:
        receipt = validate_atomic_world_commit_receipt(receipt_envelope)
        if receipt["request_digest"] == request_envelope.get("body_digest"):
            return AtomicCommitResult("REPLAYED", receipt_envelope, store)
    return core.commit_world_fragment_atomic(
        store_path=store_path,
        request_envelope=request_envelope,
        committed_at_ms=committed_at_ms,
    )


__all__ = [
    "AtomicCommitResult",
    "ZERO_DIGEST",
    "build_authorized_world_commit_request",
    "commit_world_fragment_atomic",
    "initialize_world_store",
    "make_initial_world_store",
    "make_world_commit_authorization_receipt",
    "read_world_store",
    "validate_atomic_world_commit_receipt",
    "validate_authorized_world_commit_request",
    "validate_world_commit_authorization_receipt",
    "validate_world_store",
]
