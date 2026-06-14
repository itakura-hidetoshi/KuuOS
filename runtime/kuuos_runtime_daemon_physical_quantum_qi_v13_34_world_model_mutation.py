#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy
from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import re
import time
from typing import Any, Mapping, MutableMapping, MutableSequence


@dataclass(frozen=True)
class PhysicalQuantumQiV13_34WorldModelMutationResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    mutation_status: str
    mutation_id: str
    operations_applied: int
    world_model_mutated: bool
    rollback_snapshot_written: bool
    mutation_ledger_appended: bool
    before_world_model_digest: str
    after_world_model_digest: str
    world_model_state_path: str
    rollback_snapshot_path: str
    mutation_ledger_path: str
    receipt_path: str
    audit_path: str
    blockers: list[str]
    warnings: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _m(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _sha(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def _without_digest(value: Mapping[str, Any], field: str) -> dict[str, Any]:
    payload = dict(value)
    payload.pop(field, None)
    return payload


def compute_world_model_digest(value: Mapping[str, Any]) -> str:
    return _sha(_without_digest(value, "world_model_digest"))


def compute_world_model_mutation_plan_digest(value: Mapping[str, Any]) -> str:
    return _sha(_without_digest(value, "mutation_plan_digest"))


def _read_json(path: pathlib.Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return value if isinstance(value, dict) else {}


def _latest_records(path: pathlib.Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    records: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict):
            records.append(value)
    return records


def _write_json(path: pathlib.Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(dict(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(tmp, path)


def _append_jsonl(path: pathlib.Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(dict(payload), ensure_ascii=False, sort_keys=True) + "\n")


def _pointer_parts(path: str) -> list[str]:
    if not path.startswith("/") or path == "/":
        raise ValueError("world_model_mutation_path_invalid")
    return [part.replace("~1", "/").replace("~0", "~") for part in path[1:].split("/")]


def _index(token: str, size: int, *, append_allowed: bool = False) -> int:
    if append_allowed and token == "-":
        return size
    try:
        index = int(token)
    except ValueError as exc:
        raise ValueError("world_model_mutation_list_index_invalid") from exc
    if index < 0 or index >= size:
        raise ValueError("world_model_mutation_list_index_out_of_range")
    return index


def _resolve_parent(document: Any, path: str, *, create_dicts: bool) -> tuple[Any, str]:
    parts = _pointer_parts(path)
    current = document
    for token in parts[:-1]:
        if isinstance(current, MutableMapping):
            if token not in current:
                if not create_dicts:
                    raise ValueError("world_model_mutation_path_missing")
                current[token] = {}
            current = current[token]
        elif isinstance(current, MutableSequence):
            current = current[_index(token, len(current))]
        else:
            raise ValueError("world_model_mutation_parent_not_container")
    return current, parts[-1]


def _set_value(document: Any, path: str, value: Any) -> None:
    parent, token = _resolve_parent(document, path, create_dicts=True)
    if isinstance(parent, MutableMapping):
        parent[token] = deepcopy(value)
    elif isinstance(parent, MutableSequence):
        if token == "-":
            parent.append(deepcopy(value))
        else:
            parent[_index(token, len(parent))] = deepcopy(value)
    else:
        raise ValueError("world_model_mutation_parent_not_container")


def _delete_value(document: Any, path: str) -> None:
    parent, token = _resolve_parent(document, path, create_dicts=False)
    if isinstance(parent, MutableMapping):
        if token not in parent:
            raise ValueError("world_model_mutation_path_missing")
        del parent[token]
    elif isinstance(parent, MutableSequence):
        del parent[_index(token, len(parent))]
    else:
        raise ValueError("world_model_mutation_parent_not_container")


def _get_value(document: Any, path: str) -> Any:
    current = document
    for token in _pointer_parts(path):
        if isinstance(current, Mapping):
            if token not in current:
                raise ValueError("world_model_mutation_path_missing")
            current = current[token]
        elif isinstance(current, list):
            current = current[_index(token, len(current))]
        else:
            raise ValueError("world_model_mutation_parent_not_container")
    return current


def _apply_operation(document: dict[str, Any], operation: Mapping[str, Any]) -> None:
    op = str(operation.get("op", ""))
    path = str(operation.get("path", ""))
    if op == "set":
        _set_value(document, path, operation.get("value"))
        return
    if op == "delete":
        _delete_value(document, path)
        return
    if op == "merge":
        target = _get_value(document, path)
        value = operation.get("value")
        if not isinstance(target, MutableMapping) or not isinstance(value, Mapping):
            raise ValueError("world_model_mutation_merge_requires_objects")
        target.update(deepcopy(dict(value)))
        return
    if op == "increment":
        current = _get_value(document, path)
        delta = operation.get("value")
        if isinstance(current, bool) or not isinstance(current, (int, float)):
            raise ValueError("world_model_mutation_increment_target_not_number")
        if isinstance(delta, bool) or not isinstance(delta, (int, float)):
            raise ValueError("world_model_mutation_increment_value_not_number")
        _set_value(document, path, current + delta)
        return
    if op == "append":
        target = _get_value(document, path)
        if not isinstance(target, MutableSequence):
            raise ValueError("world_model_mutation_append_target_not_list")
        target.append(deepcopy(operation.get("value")))
        return
    raise ValueError("world_model_mutation_operation_not_allowed")


def _path_within(path: str, prefix: str) -> bool:
    normalized = prefix.rstrip("/") or "/"
    return path == normalized or path.startswith(normalized + "/")


def _validate_operation_paths(
    operations: list[Mapping[str, Any]], allowed_prefixes: list[str], protected_paths: list[str], blockers: list[str]
) -> None:
    for operation in operations:
        path = str(operation.get("path", ""))
        try:
            _pointer_parts(path)
        except ValueError as exc:
            blockers.append(str(exc))
            continue
        if not any(_path_within(path, prefix) for prefix in allowed_prefixes):
            blockers.append("world_model_mutation_path_not_licensed")
        if any(_path_within(path, protected) or _path_within(protected, path) for protected in protected_paths):
            blockers.append("world_model_mutation_protected_path")


def _safe_mutation_id(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]", "_", value)[:128]


def build_physical_quantum_qi_v13_34_world_model_mutation(
    *,
    runtime_context: Mapping[str, Any],
    v13_34_world_model_mutation_license: Mapping[str, Any],
) -> PhysicalQuantumQiV13_34WorldModelMutationResult:
    ctx = _m(runtime_context)
    lic = _m(v13_34_world_model_mutation_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root_value = ctx.get("runtime_root")
    root = pathlib.Path(str(root_value)).expanduser().resolve() if root_value else pathlib.Path(".").resolve()
    if not root_value:
        blockers.append("runtime_root_missing")
    if root == pathlib.Path("/").resolve():
        blockers.append("runtime_root_forbidden")

    source_path = root / "physical_quantum_qi_v13_33_guarded_intent_activation_record.json"
    intent_packet_path = root / "physical_quantum_qi_guarded_execution_intent_packet.json"
    world_state_path = root / "physical_quantum_qi_world_model_state.json"
    ledger_path = root / "physical_quantum_qi_world_model_mutation_ledger.jsonl"
    receipt_path = root / "physical_quantum_qi_v13_34_world_model_mutation_receipt.json"
    audit_path = root / "physical_quantum_qi_v13_34_world_model_mutation_audit.jsonl"

    if ctx.get("physical_quantum_qi_v13_34_world_model_mutation_enabled") is not True:
        blockers.append("physical_quantum_qi_v13_34_world_model_mutation_enabled_not_true")
    if ctx.get("apply_physical_quantum_qi_v13_34_world_model_mutation") is not True:
        blockers.append("apply_physical_quantum_qi_v13_34_world_model_mutation_not_true")
    if lic.get("license_status") != "PHYSICAL_QUANTUM_QI_V13_34_WORLD_MODEL_MUTATION_LICENSE_READY":
        blockers.append("physical_quantum_qi_v13_34_world_model_mutation_license_not_ready")
    for flag in (
        "v13_33_activation_record_read_allowed",
        "guarded_execution_intent_packet_read_allowed",
        "world_model_state_read_allowed",
        "world_model_state_write_allowed",
        "rollback_snapshot_write_allowed",
        "mutation_ledger_append_allowed",
        "receipt_write_allowed",
        "audit_append_allowed",
        "direct_world_model_mutation_allowed",
    ):
        if lic.get(flag) is not True:
            blockers.append(flag.replace("allowed", "not_allowed"))

    source = _read_json(source_path)
    intent_packet = _read_json(intent_packet_path)
    world_state = _read_json(world_state_path)
    plan = dict(_m(ctx.get("world_model_mutation_plan")))
    mutation_id = str(plan.get("mutation_id", ""))
    safe_id = _safe_mutation_id(mutation_id) or "invalid"
    snapshot_path = root / f"physical_quantum_qi_world_model_rollback_snapshot_{safe_id}.json"

    if not source:
        blockers.append("v13_33_activation_record_missing_or_invalid")
    if not intent_packet:
        blockers.append("guarded_execution_intent_packet_missing_or_invalid")
    if not world_state:
        blockers.append("world_model_state_missing_or_invalid")
    if not plan:
        blockers.append("world_model_mutation_plan_missing")

    if source:
        if source.get("activation_status") != "guarded_intent_activation_completed":
            blockers.append("v13_33_guarded_intent_activation_not_completed")
        if source.get("guarded_execution_intent_status") != "guarded_execution_intent_ready":
            blockers.append("v13_33_guarded_intent_not_ready_for_world_mutation")
        if int(source.get("guarded_execution_intent_count", 0)) != 1:
            blockers.append("v13_33_guarded_intent_count_not_one")
        if not source.get("guarded_intent_activation_record_digest"):
            blockers.append("v13_33_activation_record_digest_missing")
        if str(source.get("source_v13_6_guarded_intent_packet_digest", "")) != str(
            intent_packet.get("guarded_execution_intent_packet_digest", "")
        ):
            blockers.append("v13_33_guarded_intent_packet_digest_mismatch")

    intents = intent_packet.get("guarded_execution_intents", [])
    if not isinstance(intents, list):
        blockers.append("guarded_execution_intents_not_list")
        intents = []
    if intent_packet:
        if intent_packet.get("guarded_execution_intent_status") != "guarded_execution_intent_ready":
            blockers.append("guarded_execution_intent_packet_not_ready")
        if int(intent_packet.get("guarded_execution_intent_count", 0)) != 1 or len(intents) != 1:
            blockers.append("guarded_execution_intent_packet_count_not_one")
        boundary = _m(intent_packet.get("boundary"))
        if boundary.get("requires_guarded_execution_license") is not True:
            blockers.append("guarded_execution_license_boundary_missing")
        if boundary.get("not_direct_execution_authority") is not True:
            blockers.append("guarded_intent_boundary_invalid")

    if not mutation_id:
        blockers.append("world_model_mutation_id_missing")
    if not plan.get("reason"):
        blockers.append("world_model_mutation_reason_missing")
    if plan.get("rollback_required") is not True:
        blockers.append("world_model_mutation_rollback_required_not_true")

    operations_raw = plan.get("operations", [])
    operations = [dict(_m(value)) for value in operations_raw] if isinstance(operations_raw, list) else []
    if not operations:
        blockers.append("world_model_mutation_operations_missing")
    max_operations = int(lic.get("max_operations", 32) or 32)
    if len(operations) > max_operations:
        blockers.append("world_model_mutation_operation_limit_exceeded")

    plan_digest = compute_world_model_mutation_plan_digest(plan) if plan else ""
    if str(plan.get("mutation_plan_digest", "")) != plan_digest:
        blockers.append("world_model_mutation_plan_digest_mismatch")
    if str(lic.get("bound_mutation_plan_digest", "")) != plan_digest:
        blockers.append("world_model_mutation_plan_not_bound_to_license")

    intent_digest = str(intents[0].get("guarded_execution_intent_digest", "")) if intents else ""
    if not intent_digest:
        blockers.append("guarded_execution_intent_digest_missing")
    if str(plan.get("source_guarded_execution_intent_digest", "")) != intent_digest:
        blockers.append("world_model_mutation_intent_digest_mismatch")

    before_digest = compute_world_model_digest(world_state) if world_state else ""
    if world_state and str(world_state.get("world_model_digest", before_digest)) != before_digest:
        blockers.append("world_model_state_embedded_digest_mismatch")
    if str(plan.get("expected_world_model_digest", "")) != before_digest:
        blockers.append("world_model_expected_digest_mismatch")

    allowed_prefixes = [str(value) for value in lic.get("allowed_path_prefixes", []) if str(value)]
    protected_paths = [str(value) for value in lic.get("protected_paths", []) if str(value)]
    if not allowed_prefixes:
        blockers.append("world_model_mutation_allowed_path_prefixes_missing")
    _validate_operation_paths(operations, allowed_prefixes, protected_paths, blockers)

    prior_records = _latest_records(ledger_path)
    if mutation_id and any(str(record.get("mutation_id", "")) == mutation_id for record in prior_records):
        blockers.append("world_model_mutation_id_replay")

    candidate_state = deepcopy(world_state)
    if not blockers:
        try:
            for operation in operations:
                _apply_operation(candidate_state, operation)
        except ValueError as exc:
            blockers.append(str(exc))

    mutated = snapshot_written = ledger_appended = False
    after_digest = before_digest
    if not blockers:
        epoch = int(time.time())
        candidate_state["version"] = "physical_quantum_qi_world_model_state_v13_34"
        candidate_state["revision"] = int(world_state.get("revision", 0) or 0) + 1
        candidate_state["previous_world_model_digest"] = before_digest
        candidate_state["last_mutation_id"] = mutation_id
        candidate_state["last_guarded_execution_intent_digest"] = intent_digest
        candidate_state["last_mutation_epoch"] = epoch
        candidate_state["boundary"] = {
            "world_model_direct_mutation_applied": True,
            "guarded_execution_intent_required": True,
            "explicit_world_model_mutation_license_required": True,
            "rollback_snapshot_required": True,
            "optimistic_digest_lock_required": True,
            "mutation_path_scope_enforced": True,
            "audit_and_receipt_required": True,
        }
        candidate_state["world_model_digest"] = compute_world_model_digest(candidate_state)
        after_digest = candidate_state["world_model_digest"]

        snapshot = {
            "version": "physical_quantum_qi_world_model_rollback_snapshot_v13_34",
            "mutation_id": mutation_id,
            "before_world_model_digest": before_digest,
            "world_model_state": world_state,
            "source_v13_33_activation_record_digest": str(source.get("guarded_intent_activation_record_digest", "")),
            "source_guarded_execution_intent_digest": intent_digest,
            "mutation_plan_digest": plan_digest,
            "epoch": epoch,
        }
        snapshot["rollback_snapshot_digest"] = _sha(snapshot)
        _write_json(snapshot_path, snapshot)
        snapshot_written = True

        _write_json(world_state_path, candidate_state)
        verified_state = _read_json(world_state_path)
        if compute_world_model_digest(verified_state) != after_digest:
            _write_json(world_state_path, world_state)
            blockers.append("world_model_mutation_post_write_verification_failed")
            mutated = False
            after_digest = before_digest
        else:
            mutated = True
            record = {
                "version": "physical_quantum_qi_world_model_mutation_record_v13_34",
                "record_type": "physical_quantum_qi_world_model_direct_mutation",
                "mutation_id": mutation_id,
                "mutation_status": "world_model_direct_mutation_applied",
                "operations_applied": len(operations),
                "before_world_model_digest": before_digest,
                "after_world_model_digest": after_digest,
                "source_v13_33_activation_record_digest": str(source.get("guarded_intent_activation_record_digest", "")),
                "source_guarded_execution_intent_packet_digest": str(
                    intent_packet.get("guarded_execution_intent_packet_digest", "")
                ),
                "source_guarded_execution_intent_digest": intent_digest,
                "mutation_plan_digest": plan_digest,
                "rollback_snapshot_digest": snapshot["rollback_snapshot_digest"],
                "prev_record_digest": str(prior_records[-1].get("record_digest", "GENESIS")) if prior_records else "GENESIS",
                "boundary": {
                    "direct_world_model_mutation_receipt": True,
                    "license_gated_world_model_mutation": True,
                    "rollback_traceable": True,
                    "guarded_intent_traceable": True,
                    "replay_protected": True,
                    "runtime_local_world_model_only": True,
                },
                "epoch": epoch,
            }
            record["record_digest"] = _sha(record)
            _append_jsonl(ledger_path, record)
            ledger_appended = True

    mutation_status = "world_model_direct_mutation_applied" if mutated and not blockers else "world_model_direct_mutation_blocked"
    status = (
        "PHYSICAL_QUANTUM_QI_V13_34_WORLD_MODEL_MUTATION_READY"
        if mutated and snapshot_written and ledger_appended and not blockers
        else "PHYSICAL_QUANTUM_QI_V13_34_WORLD_MODEL_MUTATION_BLOCKED"
    )
    receipt = {
        "version": "kuuos_runtime_daemon_physical_quantum_qi_v13_34_world_model_mutation",
        "status": status,
        "packet_id": "physical-quantum-qi-v13-34-world-model-mutation-"
        + _sha({"mutation_id": mutation_id, "after": after_digest, "blockers": blockers})[:16],
        "mutation_status": mutation_status,
        "mutation_id": mutation_id,
        "operations_applied": len(operations) if mutated else 0,
        "world_model_mutated": mutated,
        "rollback_snapshot_written": snapshot_written,
        "mutation_ledger_appended": ledger_appended,
        "before_world_model_digest": before_digest,
        "after_world_model_digest": after_digest,
        "mutation_plan_digest": plan_digest,
        "source_guarded_execution_intent_digest": intent_digest,
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "audit_record_digest": _sha(receipt)})

    return PhysicalQuantumQiV13_34WorldModelMutationResult(
        receipt["version"], status, receipt["packet_id"], str(root), mutation_status, mutation_id,
        receipt["operations_applied"], mutated, snapshot_written, ledger_appended, before_digest, after_digest,
        str(world_state_path), str(snapshot_path), str(ledger_path), str(receipt_path), str(audit_path), blockers, warnings,
    )
