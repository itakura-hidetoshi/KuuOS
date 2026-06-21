from __future__ import annotations

from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterator, Mapping
import json
import os

from runtime import kuuos_verifyos_world_adoption_entry_v0_33 as v033

try:
    import fcntl
except ImportError:  # pragma: no cover - POSIX is used by the reference runtime.
    fcntl = None

VERSION = "v0.34"
AUTH_VERSION = "world_commit_authorization_receipt_v0_34"
REQUEST_VERSION = "authorized_world_commit_request_v0_34"
RECEIPT_VERSION = "atomic_world_commit_receipt_v0_34"
STORE_VERSION = "atomic_world_store_v0_34"
ZERO_DIGEST = "0" * 64


def canonical_json(value: Any) -> str:
    return v033.canonical_json(value)


def digest(value: Any) -> str:
    return v033.digest(value)


def make_envelope(body: Mapping[str, Any]) -> dict[str, Any]:
    return v033.make_envelope(body)


def validate_envelope(envelope: Mapping[str, Any], *, label: str) -> dict[str, Any]:
    return v033.core.validate_envelope(envelope, label=label)


def _hex_digest(value: Any, *, field: str) -> str:
    if not isinstance(value, str) or len(value) != 64:
        raise ValueError(f"{field}_invalid")
    try:
        int(value, 16)
    except ValueError as exc:
        raise ValueError(f"{field}_invalid") from exc
    return value


def _text(value: Any, *, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field}_invalid")
    return value.strip()


def _nat(value: Any, *, field: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < 0:
        raise ValueError(f"{field}_invalid")
    return value


def _positive_nat(value: Any, *, field: str) -> int:
    value = _nat(value, field=field)
    if value == 0:
        raise ValueError(f"{field}_invalid")
    return value


def _require_true(body: Mapping[str, Any], fields: tuple[str, ...], *, label: str) -> None:
    for field in fields:
        if body.get(field) is not True:
            raise ValueError(f"{label}_required_flag_invalid:{field}")


def _require_false(body: Mapping[str, Any], fields: tuple[str, ...], *, label: str) -> None:
    for field in fields:
        if body.get(field) is not False:
            raise ValueError(f"{label}_boundary_invalid:{field}")


def _validate_adopt_candidate(
    disposition_envelope: Mapping[str, Any],
) -> dict[str, Any]:
    disposition = v033.validate_world_disposition_candidate(disposition_envelope)
    if disposition["route"] != "ADOPT_CANDIDATE":
        raise ValueError("world_disposition_not_adopt_candidate")
    if disposition["verification_verdict"] != "PASSED":
        raise ValueError("adopt_candidate_not_verification_passed")
    if disposition["source_feedback_route"] != "WORLD_UPDATE_CANDIDATE":
        raise ValueError("adopt_candidate_source_route_invalid")
    if disposition["candidate_world_fragment_digest"] != disposition["proposed_world_fragment_digest"]:
        raise ValueError("adopt_candidate_fragment_invalid")
    if disposition.get("disposition_is_candidate") is not True:
        raise ValueError("disposition_candidate_flag_missing")
    if disposition.get("world_commit_required_separately") is not True:
        raise ValueError("separate_world_commit_not_required")
    if disposition.get("same_root_required") is not True:
        raise ValueError("same_root_not_required")
    if disposition.get("automatic_world_commit") is not False:
        raise ValueError("automatic_world_commit_forbidden")
    return disposition


def make_world_commit_authorization_receipt(
    *,
    authorization_id: str,
    source_disposition_envelope: Mapping[str, Any],
    world_store_id: str,
    expected_generation: int,
    expected_prior_commit_digest: str,
    fencing_token: int,
    lease_epoch: int,
    scope_digest: str,
    host_license_digest: str,
    issued_by: str,
    issued_at_ms: int,
    not_before_ms: int,
    expires_at_ms: int,
) -> dict[str, Any]:
    disposition = _validate_adopt_candidate(source_disposition_envelope)
    authorization_id = _text(authorization_id, field="authorization_id")
    world_store_id = _text(world_store_id, field="world_store_id")
    issued_by = _text(issued_by, field="issued_by")
    expected_generation = _nat(expected_generation, field="expected_generation")
    fencing_token = _positive_nat(fencing_token, field="fencing_token")
    lease_epoch = _positive_nat(lease_epoch, field="lease_epoch")
    expected_prior_commit_digest = _hex_digest(
        expected_prior_commit_digest,
        field="expected_prior_commit_digest",
    )
    scope_digest = _hex_digest(scope_digest, field="scope_digest")
    host_license_digest = _hex_digest(host_license_digest, field="host_license_digest")
    issued_at_ms = _nat(issued_at_ms, field="issued_at_ms")
    not_before_ms = _nat(not_before_ms, field="not_before_ms")
    expires_at_ms = _nat(expires_at_ms, field="expires_at_ms")
    if not issued_at_ms <= not_before_ms < expires_at_ms:
        raise ValueError("world_commit_authorization_window_invalid")

    body = {
        "authorization_version": AUTH_VERSION,
        "authorization_id": authorization_id,
        "source_disposition_digest": source_disposition_envelope["body_digest"],
        "verification_receipt_digest": disposition["verification_receipt_digest"],
        "source_feedback_digest": disposition["source_feedback_digest"],
        "source_evidence_receipt_digest": disposition["source_evidence_receipt_digest"],
        "source_report_digest": disposition["source_report_digest"],
        "source_state_digest": disposition["source_state_digest"],
        "root_lineage_digest": disposition["root_lineage_digest"],
        "prior_world_fragment_digest": disposition["prior_world_fragment_digest"],
        "proposed_world_fragment_digest": disposition["proposed_world_fragment_digest"],
        "candidate_world_fragment_digest": disposition["candidate_world_fragment_digest"],
        "mission_candidate_id": disposition["mission_candidate_id"],
        "observation_candidate_id": disposition["observation_candidate_id"],
        "source_item_id": disposition["source_item_id"],
        "world_store_id": world_store_id,
        "expected_generation": expected_generation,
        "target_generation": expected_generation + 1,
        "expected_prior_commit_digest": expected_prior_commit_digest,
        "fencing_token": fencing_token,
        "lease_epoch": lease_epoch,
        "scope_digest": scope_digest,
        "host_license_digest": host_license_digest,
        "issued_by": issued_by,
        "issued_at_ms": issued_at_ms,
        "not_before_ms": not_before_ms,
        "expires_at_ms": expires_at_ms,
        "max_commits": 1,
        "single_use": True,
        "local_commit_authorization_only": True,
        "open_horizon_preserved": True,
        "global_cycle_limit": None,
        "global_generation_limit": None,
        "global_time_horizon_limit": None,
        "grants_world_fragment_commit": True,
        "grants_constitutional_root_rewrite": False,
        "grants_memory_history_overwrite": False,
        "grants_truth_authority": False,
        "grants_causal_attribution": False,
        "grants_plan_activation": False,
        "grants_actos_invocation": False,
        "grants_automatic_rollback": False,
        "grants_mission_completion": False,
    }
    authorization = make_envelope(body)
    validate_world_commit_authorization_receipt(authorization)
    return authorization


def validate_world_commit_authorization_receipt(
    authorization_envelope: Mapping[str, Any],
) -> dict[str, Any]:
    body = validate_envelope(authorization_envelope, label="world_commit_authorization")
    if body.get("authorization_version") != AUTH_VERSION:
        raise ValueError("world_commit_authorization_version_invalid")
    for field in (
        "source_disposition_digest",
        "verification_receipt_digest",
        "source_feedback_digest",
        "source_evidence_receipt_digest",
        "source_report_digest",
        "source_state_digest",
        "root_lineage_digest",
        "prior_world_fragment_digest",
        "proposed_world_fragment_digest",
        "candidate_world_fragment_digest",
        "expected_prior_commit_digest",
        "scope_digest",
        "host_license_digest",
    ):
        _hex_digest(body.get(field), field=field)
    for field in (
        "authorization_id",
        "mission_candidate_id",
        "observation_candidate_id",
        "source_item_id",
        "world_store_id",
        "issued_by",
    ):
        _text(body.get(field), field=field)
    expected_generation = _nat(body.get("expected_generation"), field="expected_generation")
    target_generation = _nat(body.get("target_generation"), field="target_generation")
    if target_generation != expected_generation + 1:
        raise ValueError("target_generation_invalid")
    _positive_nat(body.get("fencing_token"), field="fencing_token")
    _positive_nat(body.get("lease_epoch"), field="lease_epoch")
    issued_at_ms = _nat(body.get("issued_at_ms"), field="issued_at_ms")
    not_before_ms = _nat(body.get("not_before_ms"), field="not_before_ms")
    expires_at_ms = _nat(body.get("expires_at_ms"), field="expires_at_ms")
    if not issued_at_ms <= not_before_ms < expires_at_ms:
        raise ValueError("world_commit_authorization_window_invalid")
    if body.get("max_commits") != 1 or body.get("single_use") is not True:
        raise ValueError("world_commit_authorization_not_single_use")
    _require_true(
        body,
        (
            "local_commit_authorization_only",
            "open_horizon_preserved",
            "grants_world_fragment_commit",
        ),
        label="world_commit_authorization",
    )
    for field in (
        "global_cycle_limit",
        "global_generation_limit",
        "global_time_horizon_limit",
    ):
        if body.get(field) is not None:
            raise ValueError(f"open_horizon_shrunk:{field}")
    _require_false(
        body,
        (
            "grants_constitutional_root_rewrite",
            "grants_memory_history_overwrite",
            "grants_truth_authority",
            "grants_causal_attribution",
            "grants_plan_activation",
            "grants_actos_invocation",
            "grants_automatic_rollback",
            "grants_mission_completion",
        ),
        label="world_commit_authorization",
    )
    if body["candidate_world_fragment_digest"] != body["proposed_world_fragment_digest"]:
        raise ValueError("authorized_candidate_fragment_invalid")
    return body


def build_authorized_world_commit_request(
    source_disposition_envelope: Mapping[str, Any],
    authorization_envelope: Mapping[str, Any],
    *,
    requested_at_ms: int,
) -> dict[str, Any]:
    disposition = _validate_adopt_candidate(source_disposition_envelope)
    authorization = validate_world_commit_authorization_receipt(authorization_envelope)
    exact_bindings = {
        "source_disposition_digest": source_disposition_envelope.get("body_digest"),
        "verification_receipt_digest": disposition["verification_receipt_digest"],
        "source_feedback_digest": disposition["source_feedback_digest"],
        "source_evidence_receipt_digest": disposition["source_evidence_receipt_digest"],
        "source_report_digest": disposition["source_report_digest"],
        "source_state_digest": disposition["source_state_digest"],
        "root_lineage_digest": disposition["root_lineage_digest"],
        "prior_world_fragment_digest": disposition["prior_world_fragment_digest"],
        "proposed_world_fragment_digest": disposition["proposed_world_fragment_digest"],
        "candidate_world_fragment_digest": disposition["candidate_world_fragment_digest"],
        "mission_candidate_id": disposition["mission_candidate_id"],
        "observation_candidate_id": disposition["observation_candidate_id"],
        "source_item_id": disposition["source_item_id"],
    }
    for field, expected in exact_bindings.items():
        if authorization.get(field) != expected:
            raise ValueError(f"world_commit_authorization_binding_mismatch:{field}")
    requested_at_ms = _nat(requested_at_ms, field="requested_at_ms")
    if not authorization["not_before_ms"] <= requested_at_ms < authorization["expires_at_ms"]:
        raise ValueError("world_commit_authorization_not_current")
    request_id = "world-commit-" + digest({
        "authorization_digest": authorization_envelope["body_digest"],
        "source_disposition_digest": source_disposition_envelope["body_digest"],
        "requested_at_ms": requested_at_ms,
    })[:24]
    body = {
        "request_version": REQUEST_VERSION,
        "request_id": request_id,
        "authorization_digest": authorization_envelope["body_digest"],
        "authorization_id": authorization["authorization_id"],
        **exact_bindings,
        "world_store_id": authorization["world_store_id"],
        "expected_generation": authorization["expected_generation"],
        "target_generation": authorization["target_generation"],
        "expected_prior_commit_digest": authorization["expected_prior_commit_digest"],
        "fencing_token": authorization["fencing_token"],
        "lease_epoch": authorization["lease_epoch"],
        "scope_digest": authorization["scope_digest"],
        "host_license_digest": authorization["host_license_digest"],
        "requested_at_ms": requested_at_ms,
        "authorization_issued_at_ms": authorization["issued_at_ms"],
        "authorization_not_before_ms": authorization["not_before_ms"],
        "authorization_expires_at_ms": authorization["expires_at_ms"],
        "commit_index": 1,
        "single_use": True,
        "optimistic_concurrency_required": True,
        "fencing_required": True,
        "atomic_replace_required": True,
        "append_only_history_required": True,
        "rollback_reference_required": True,
        "same_root_required": True,
        "local_commit_authorization_only": True,
        "open_horizon_preserved": True,
        "global_cycle_limit": None,
        "global_generation_limit": None,
        "global_time_horizon_limit": None,
        "grants_world_fragment_commit": True,
        "grants_constitutional_root_rewrite": False,
        "grants_memory_history_overwrite": False,
        "grants_truth_authority": False,
        "grants_causal_attribution": False,
        "grants_plan_activation": False,
        "grants_actos_invocation": False,
        "grants_automatic_rollback": False,
        "grants_mission_completion": False,
    }
    request = make_envelope(body)
    validate_authorized_world_commit_request(request)
    return request


def validate_authorized_world_commit_request(
    request_envelope: Mapping[str, Any],
) -> dict[str, Any]:
    body = validate_envelope(request_envelope, label="authorized_world_commit_request")
    if body.get("request_version") != REQUEST_VERSION:
        raise ValueError("world_commit_request_version_invalid")
    for field in (
        "authorization_digest",
        "source_disposition_digest",
        "verification_receipt_digest",
        "source_feedback_digest",
        "source_evidence_receipt_digest",
        "source_report_digest",
        "source_state_digest",
        "root_lineage_digest",
        "prior_world_fragment_digest",
        "proposed_world_fragment_digest",
        "candidate_world_fragment_digest",
        "expected_prior_commit_digest",
        "scope_digest",
        "host_license_digest",
    ):
        _hex_digest(body.get(field), field=field)
    for field in (
        "request_id",
        "authorization_id",
        "mission_candidate_id",
        "observation_candidate_id",
        "source_item_id",
        "world_store_id",
    ):
        _text(body.get(field), field=field)
    expected_generation = _nat(body.get("expected_generation"), field="expected_generation")
    if body.get("target_generation") != expected_generation + 1:
        raise ValueError("target_generation_invalid")
    _positive_nat(body.get("fencing_token"), field="fencing_token")
    _positive_nat(body.get("lease_epoch"), field="lease_epoch")
    issued_at_ms = _nat(body.get("authorization_issued_at_ms"), field="authorization_issued_at_ms")
    not_before_ms = _nat(body.get("authorization_not_before_ms"), field="authorization_not_before_ms")
    requested_at_ms = _nat(body.get("requested_at_ms"), field="requested_at_ms")
    expires_at_ms = _nat(body.get("authorization_expires_at_ms"), field="authorization_expires_at_ms")
    if not issued_at_ms <= not_before_ms <= requested_at_ms < expires_at_ms:
        raise ValueError("world_commit_request_window_invalid")
    if body.get("commit_index") != 1 or body.get("single_use") is not True:
        raise ValueError("world_commit_request_not_single_use")
    _require_true(
        body,
        (
            "optimistic_concurrency_required",
            "fencing_required",
            "atomic_replace_required",
            "append_only_history_required",
            "rollback_reference_required",
            "same_root_required",
            "local_commit_authorization_only",
            "open_horizon_preserved",
            "grants_world_fragment_commit",
        ),
        label="world_commit_request",
    )
    for field in (
        "global_cycle_limit",
        "global_generation_limit",
        "global_time_horizon_limit",
    ):
        if body.get(field) is not None:
            raise ValueError(f"open_horizon_shrunk:{field}")
    _require_false(
        body,
        (
            "grants_constitutional_root_rewrite",
            "grants_memory_history_overwrite",
            "grants_truth_authority",
            "grants_causal_attribution",
            "grants_plan_activation",
            "grants_actos_invocation",
            "grants_automatic_rollback",
            "grants_mission_completion",
        ),
        label="world_commit_request",
    )
    if body["candidate_world_fragment_digest"] != body["proposed_world_fragment_digest"]:
        raise ValueError("world_commit_request_candidate_fragment_invalid")
    return body


def make_initial_world_store(
    *,
    world_store_id: str,
    root_lineage_digest: str,
    current_world_fragment_digest: str,
    created_at_ms: int,
) -> dict[str, Any]:
    world_store_id = _text(world_store_id, field="world_store_id")
    root_lineage_digest = _hex_digest(root_lineage_digest, field="root_lineage_digest")
    current_world_fragment_digest = _hex_digest(
        current_world_fragment_digest,
        field="current_world_fragment_digest",
    )
    created_at_ms = _nat(created_at_ms, field="created_at_ms")
    body = {
        "store_version": STORE_VERSION,
        "world_store_id": world_store_id,
        "root_lineage_digest": root_lineage_digest,
        "genesis_world_fragment_digest": current_world_fragment_digest,
        "current_world_fragment_digest": current_world_fragment_digest,
        "generation": 0,
        "last_commit_digest": ZERO_DIGEST,
        "last_fencing_token": 0,
        "last_lease_epoch": 0,
        "created_at_ms": created_at_ms,
        "updated_at_ms": created_at_ms,
        "commits": [],
        "append_only_history": True,
        "history_deletion_forbidden": True,
        "constitutional_root_immutable": True,
        "open_horizon_preserved": True,
        "global_cycle_limit": None,
        "global_generation_limit": None,
        "global_time_horizon_limit": None,
    }
    store = make_envelope(body)
    validate_world_store(store)
    return store


def validate_atomic_world_commit_receipt(
    receipt_envelope: Mapping[str, Any],
) -> dict[str, Any]:
    body = validate_envelope(receipt_envelope, label="atomic_world_commit_receipt")
    if body.get("receipt_version") != RECEIPT_VERSION:
        raise ValueError("world_commit_receipt_version_invalid")
    for field in (
        "request_digest",
        "authorization_digest",
        "source_disposition_digest",
        "verification_receipt_digest",
        "source_feedback_digest",
        "source_evidence_receipt_digest",
        "source_report_digest",
        "source_state_digest",
        "root_lineage_digest",
        "previous_world_fragment_digest",
        "committed_world_fragment_digest",
        "previous_commit_digest",
        "rollback_reference_digest",
        "scope_digest",
        "host_license_digest",
    ):
        _hex_digest(body.get(field), field=field)
    for field in (
        "commit_id",
        "authorization_id",
        "world_store_id",
        "mission_candidate_id",
        "observation_candidate_id",
        "source_item_id",
    ):
        _text(body.get(field), field=field)
    generation_before = _nat(body.get("generation_before"), field="generation_before")
    generation_after = _nat(body.get("generation_after"), field="generation_after")
    if generation_after != generation_before + 1:
        raise ValueError("world_commit_generation_transition_invalid")
    _positive_nat(body.get("fencing_token"), field="fencing_token")
    _positive_nat(body.get("lease_epoch"), field="lease_epoch")
    requested_at_ms = _nat(body.get("requested_at_ms"), field="requested_at_ms")
    committed_at_ms = _nat(body.get("committed_at_ms"), field="committed_at_ms")
    expires_at_ms = _nat(body.get("authorization_expires_at_ms"), field="authorization_expires_at_ms")
    if not requested_at_ms <= committed_at_ms < expires_at_ms:
        raise ValueError("world_commit_completion_outside_authorization_window")
    _require_true(
        body,
        (
            "authorization_consumed",
            "optimistic_concurrency_matched",
            "fencing_accepted",
            "atomic_replace_committed",
            "append_only_history_preserved",
            "immutable_commit_receipt",
            "rollback_reference_preserved",
            "rollback_requires_fresh_authorization",
            "rollback_is_not_history_deletion",
            "same_root_preserved",
            "world_commit_recorded",
            "local_commit_authorization_only",
            "open_horizon_preserved",
        ),
        label="world_commit_receipt",
    )
    for field in (
        "global_cycle_limit",
        "global_generation_limit",
        "global_time_horizon_limit",
    ):
        if body.get(field) is not None:
            raise ValueError(f"open_horizon_shrunk:{field}")
    _require_false(
        body,
        (
            "world_commit_is_truth",
            "world_commit_is_causal_attribution",
            "constitutional_root_rewritten",
            "memory_history_overwritten",
            "automatic_rollback_performed",
            "automatic_mission_completion",
            "grants_plan_activation",
            "grants_actos_invocation",
        ),
        label="world_commit_receipt",
    )
    return body


def validate_world_store(store_envelope: Mapping[str, Any]) -> dict[str, Any]:
    body = validate_envelope(store_envelope, label="atomic_world_store")
    if body.get("store_version") != STORE_VERSION:
        raise ValueError("world_store_version_invalid")
    _text(body.get("world_store_id"), field="world_store_id")
    for field in (
        "root_lineage_digest",
        "genesis_world_fragment_digest",
        "current_world_fragment_digest",
        "last_commit_digest",
    ):
        _hex_digest(body.get(field), field=field)
    generation = _nat(body.get("generation"), field="generation")
    last_fencing_token = _nat(body.get("last_fencing_token"), field="last_fencing_token")
    last_lease_epoch = _nat(body.get("last_lease_epoch"), field="last_lease_epoch")
    created_at_ms = _nat(body.get("created_at_ms"), field="created_at_ms")
    updated_at_ms = _nat(body.get("updated_at_ms"), field="updated_at_ms")
    if updated_at_ms < created_at_ms:
        raise ValueError("world_store_time_invalid")
    _require_true(
        body,
        (
            "append_only_history",
            "history_deletion_forbidden",
            "constitutional_root_immutable",
            "open_horizon_preserved",
        ),
        label="world_store",
    )
    for field in (
        "global_cycle_limit",
        "global_generation_limit",
        "global_time_horizon_limit",
    ):
        if body.get(field) is not None:
            raise ValueError(f"open_horizon_shrunk:{field}")
    commits = body.get("commits")
    if not isinstance(commits, list) or len(commits) != generation:
        raise ValueError("world_store_commit_history_length_invalid")
    previous_fragment = body["genesis_world_fragment_digest"]
    previous_commit_digest = ZERO_DIGEST
    previous_fencing_token = 0
    previous_lease_epoch = 0
    for index, receipt_envelope in enumerate(commits):
        if not isinstance(receipt_envelope, dict):
            raise ValueError("world_store_commit_entry_invalid")
        receipt = validate_atomic_world_commit_receipt(receipt_envelope)
        if receipt["world_store_id"] != body["world_store_id"]:
            raise ValueError("world_store_commit_store_id_mismatch")
        if receipt["root_lineage_digest"] != body["root_lineage_digest"]:
            raise ValueError("world_store_commit_root_lineage_mismatch")
        if receipt["generation_before"] != index or receipt["generation_after"] != index + 1:
            raise ValueError("world_store_commit_generation_chain_invalid")
        if receipt["previous_world_fragment_digest"] != previous_fragment:
            raise ValueError("world_store_fragment_chain_invalid")
        if receipt["previous_commit_digest"] != previous_commit_digest:
            raise ValueError("world_store_receipt_chain_invalid")
        if receipt["fencing_token"] <= previous_fencing_token:
            raise ValueError("world_store_fencing_chain_invalid")
        if receipt["lease_epoch"] < previous_lease_epoch:
            raise ValueError("world_store_lease_epoch_chain_invalid")
        previous_fragment = receipt["committed_world_fragment_digest"]
        previous_commit_digest = receipt_envelope["body_digest"]
        previous_fencing_token = receipt["fencing_token"]
        previous_lease_epoch = receipt["lease_epoch"]
    if generation == 0:
        if body["current_world_fragment_digest"] != body["genesis_world_fragment_digest"]:
            raise ValueError("world_store_genesis_fragment_mismatch")
        if body["last_commit_digest"] != ZERO_DIGEST:
            raise ValueError("world_store_genesis_commit_digest_invalid")
        if last_fencing_token != 0 or last_lease_epoch != 0:
            raise ValueError("world_store_genesis_fencing_invalid")
    else:
        if body["current_world_fragment_digest"] != previous_fragment:
            raise ValueError("world_store_current_fragment_mismatch")
        if body["last_commit_digest"] != previous_commit_digest:
            raise ValueError("world_store_last_commit_digest_mismatch")
        if last_fencing_token != previous_fencing_token:
            raise ValueError("world_store_last_fencing_token_mismatch")
        if last_lease_epoch != previous_lease_epoch:
            raise ValueError("world_store_last_lease_epoch_mismatch")
    return body


def _read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(Path(path).read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError("world_store_not_found") from exc
    if not isinstance(value, dict):
        raise ValueError("world_store_file_invalid")
    return value


def read_world_store(store_path: Path) -> dict[str, Any]:
    store = _read_json(Path(store_path))
    validate_world_store(store)
    return store


def _fsync_directory(path: Path) -> None:
    flags = getattr(os, "O_DIRECTORY", 0) | os.O_RDONLY
    try:
        directory_fd = os.open(str(path), flags)
    except OSError:
        return
    try:
        os.fsync(directory_fd)
    finally:
        os.close(directory_fd)


def _atomic_write_json(path: Path, value: Mapping[str, Any]) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = path.with_name(
        f".{path.name}.tmp.{os.getpid()}.{digest(value)[:16]}"
    )
    payload = canonical_json(value) + "\n"
    try:
        with temp_path.open("x", encoding="utf-8") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_path, path)
        _fsync_directory(path.parent)
    finally:
        try:
            temp_path.unlink()
        except FileNotFoundError:
            pass


@contextmanager
def _exclusive_store_lock(store_path: Path) -> Iterator[None]:
    lock_path = Path(store_path).with_name(Path(store_path).name + ".lock")
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    with lock_path.open("a+b") as lock_handle:
        if fcntl is None:
            raise RuntimeError("posix_file_lock_required")
        fcntl.flock(lock_handle.fileno(), fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(lock_handle.fileno(), fcntl.LOCK_UN)


def initialize_world_store(*, store_path: Path, store_envelope: Mapping[str, Any]) -> dict[str, Any]:
    validate_world_store(store_envelope)
    store_path = Path(store_path)
    with _exclusive_store_lock(store_path):
        if store_path.exists():
            raise ValueError("world_store_already_exists")
        _atomic_write_json(store_path, store_envelope)
        return read_world_store(store_path)


@dataclass(frozen=True)
class AtomicCommitResult:
    status: str
    receipt: dict[str, Any]
    store: dict[str, Any]


def commit_world_fragment_atomic(
    *,
    store_path: Path,
    request_envelope: Mapping[str, Any],
    committed_at_ms: int,
) -> AtomicCommitResult:
    request = validate_authorized_world_commit_request(request_envelope)
    committed_at_ms = _nat(committed_at_ms, field="committed_at_ms")
    if not request["requested_at_ms"] <= committed_at_ms < request["authorization_expires_at_ms"]:
        raise ValueError("world_commit_completion_outside_authorization_window")
    store_path = Path(store_path)
    with _exclusive_store_lock(store_path):
        store_envelope = read_world_store(store_path)
        store = validate_world_store(store_envelope)
        for receipt_envelope in store["commits"]:
            receipt = validate_atomic_world_commit_receipt(receipt_envelope)
            if receipt["request_digest"] == request_envelope.get("body_digest"):
                return AtomicCommitResult("REPLAYED", receipt_envelope, store_envelope)
            if receipt["authorization_id"] == request["authorization_id"]:
                raise ValueError("world_commit_authorization_already_consumed")
            if receipt["authorization_digest"] == request["authorization_digest"]:
                raise ValueError("world_commit_authorization_digest_already_consumed")
            if receipt["source_disposition_digest"] == request["source_disposition_digest"]:
                raise ValueError("world_disposition_already_committed")

        if store["world_store_id"] != request["world_store_id"]:
            raise ValueError("world_store_id_mismatch")
        if store["root_lineage_digest"] != request["root_lineage_digest"]:
            raise ValueError("world_store_root_lineage_mismatch")
        if store["generation"] != request["expected_generation"]:
            raise ValueError("world_store_generation_conflict")
        if store["last_commit_digest"] != request["expected_prior_commit_digest"]:
            raise ValueError("world_store_prior_commit_conflict")
        if store["current_world_fragment_digest"] != request["prior_world_fragment_digest"]:
            raise ValueError("world_store_prior_fragment_conflict")
        if request["fencing_token"] <= store["last_fencing_token"]:
            raise ValueError("stale_fencing_token")
        if request["lease_epoch"] < store["last_lease_epoch"]:
            raise ValueError("stale_lease_epoch")

        rollback_reference_digest = digest({
            "world_store_id": store["world_store_id"],
            "root_lineage_digest": store["root_lineage_digest"],
            "generation": store["generation"],
            "world_fragment_digest": store["current_world_fragment_digest"],
            "previous_commit_digest": store["last_commit_digest"],
        })
        commit_id = "world-commit-receipt-" + digest({
            "request_digest": request_envelope["body_digest"],
            "committed_at_ms": committed_at_ms,
            "generation_after": store["generation"] + 1,
        })[:24]
        receipt_body = {
            "receipt_version": RECEIPT_VERSION,
            "commit_id": commit_id,
            "request_digest": request_envelope["body_digest"],
            "authorization_digest": request["authorization_digest"],
            "authorization_id": request["authorization_id"],
            "source_disposition_digest": request["source_disposition_digest"],
            "verification_receipt_digest": request["verification_receipt_digest"],
            "source_feedback_digest": request["source_feedback_digest"],
            "source_evidence_receipt_digest": request["source_evidence_receipt_digest"],
            "source_report_digest": request["source_report_digest"],
            "source_state_digest": request["source_state_digest"],
            "root_lineage_digest": request["root_lineage_digest"],
            "world_store_id": request["world_store_id"],
            "previous_world_fragment_digest": store["current_world_fragment_digest"],
            "committed_world_fragment_digest": request["candidate_world_fragment_digest"],
            "generation_before": store["generation"],
            "generation_after": store["generation"] + 1,
            "previous_commit_digest": store["last_commit_digest"],
            "fencing_token": request["fencing_token"],
            "lease_epoch": request["lease_epoch"],
            "scope_digest": request["scope_digest"],
            "host_license_digest": request["host_license_digest"],
            "mission_candidate_id": request["mission_candidate_id"],
            "observation_candidate_id": request["observation_candidate_id"],
            "source_item_id": request["source_item_id"],
            "requested_at_ms": request["requested_at_ms"],
            "committed_at_ms": committed_at_ms,
            "authorization_expires_at_ms": request["authorization_expires_at_ms"],
            "rollback_reference_digest": rollback_reference_digest,
            "authorization_consumed": True,
            "optimistic_concurrency_matched": True,
            "fencing_accepted": True,
            "atomic_replace_committed": True,
            "append_only_history_preserved": True,
            "immutable_commit_receipt": True,
            "rollback_reference_preserved": True,
            "rollback_requires_fresh_authorization": True,
            "rollback_is_not_history_deletion": True,
            "same_root_preserved": True,
            "world_commit_recorded": True,
            "local_commit_authorization_only": True,
            "open_horizon_preserved": True,
            "global_cycle_limit": None,
            "global_generation_limit": None,
            "global_time_horizon_limit": None,
            "world_commit_is_truth": False,
            "world_commit_is_causal_attribution": False,
            "constitutional_root_rewritten": False,
            "memory_history_overwritten": False,
            "automatic_rollback_performed": False,
            "automatic_mission_completion": False,
            "grants_plan_activation": False,
            "grants_actos_invocation": False,
        }
        receipt_envelope = make_envelope(receipt_body)
        validate_atomic_world_commit_receipt(receipt_envelope)

        updated_body = dict(store)
        updated_body.update({
            "current_world_fragment_digest": request["candidate_world_fragment_digest"],
            "generation": store["generation"] + 1,
            "last_commit_digest": receipt_envelope["body_digest"],
            "last_fencing_token": request["fencing_token"],
            "last_lease_epoch": request["lease_epoch"],
            "updated_at_ms": committed_at_ms,
            "commits": [*store["commits"], receipt_envelope],
        })
        updated_store_envelope = make_envelope(updated_body)
        validate_world_store(updated_store_envelope)
        _atomic_write_json(store_path, updated_store_envelope)
        persisted_store = read_world_store(store_path)
        if persisted_store["body_digest"] != updated_store_envelope["body_digest"]:
            raise RuntimeError("world_store_post_commit_readback_mismatch")
        return AtomicCommitResult("COMMITTED", receipt_envelope, persisted_store)


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
