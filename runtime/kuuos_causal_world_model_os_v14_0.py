#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy
from dataclasses import asdict, dataclass
import json
import os
import pathlib
import time
from typing import Any, Mapping

from runtime.kuuos_causal_world_model_core_v14_0 import (
    apply_intervention,
    apply_observation,
    command_digest,
    model_digest,
    normalize_variable,
    propagate,
    sha,
    valid_digest,
    valid_name,
    validate_graph,
    variable_deltas,
)

VERSION = "kuuos_causal_world_model_os_v14_0"
READY = "KUUOS_CAUSAL_WORLD_MODEL_OS_V14_0_READY"
BLOCKED = "KUUOS_CAUSAL_WORLD_MODEL_OS_V14_0_BLOCKED"
LICENSE_READY = "KUUOS_CAUSAL_WORLD_MODEL_OS_V14_0_LICENSE_READY"
COMMAND_KINDS = {"initialize", "observe", "intervene", "undo", "counterfactual", "inspect"}
PROCESS_KEYS = (
    "process_tensor_digest",
    "memory_kernel_digest",
    "history_window_digest",
    "instrument_trace_digest",
    "non_markov_context_digest",
)


@dataclass(frozen=True)
class KuuOSCausalWorldModelOSV14Result:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    command_kind: str
    transaction_id: str
    world_id: str
    state_mutated: bool
    counterfactual_generated: bool
    undo_applied: bool
    revision: int
    before_world_model_digest: str
    after_world_model_digest: str
    state_path: str
    event_ledger_path: str
    result_path: str
    audit_path: str
    blockers: list[str]
    warnings: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _m(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _read_json(path: pathlib.Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return value if isinstance(value, dict) else {}


def _write_json(path: pathlib.Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(dict(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    os.replace(temporary, path)


def _records(path: pathlib.Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    values: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict):
            values.append(value)
    return values


def _append_jsonl(path: pathlib.Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(dict(payload), ensure_ascii=False, sort_keys=True) + "\n")


def _latest_digest(path: pathlib.Path) -> str:
    values = _records(path)
    return str(values[-1].get("record_digest", "CORRUPT")) if values else "GENESIS"


def _safe_id(value: str) -> str:
    return "".join(ch if ch.isalnum() or ch in "_.-" else "_" for ch in value)[:128] or "invalid"


def _state_boundary() -> dict[str, bool]:
    return {
        "causal_world_model_internal_state": True,
        "direct_world_model_mutation_enabled": True,
        "external_world_actuation_authority": False,
        "world_model_state_not_truth_authority": True,
        "counterfactual_projection_not_fact": True,
        "decision_authority_separate": True,
        "execution_authority_separate": True,
        "reversible_snapshot_required": True,
        "uncertainty_visible": True,
        "non_markov_memory_lineage_preserved": True,
        "process_tensor_context_required": True,
    }


def _process_context(command: Mapping[str, Any], blockers: list[str]) -> dict[str, str]:
    source = _m(command.get("process_tensor_context"))
    result = {key: str(source.get(key, "")) for key in PROCESS_KEYS}
    for key, value in result.items():
        if not value:
            blockers.append(f"process_tensor_context_{key}_missing")
    return result


def _license_variables(license_packet: Mapping[str, Any], blockers: list[str]) -> tuple[set[str], set[str]]:
    allowed_raw = license_packet.get("allowed_variables", [])
    protected_raw = license_packet.get("protected_variables", [])
    allowed = {str(value) for value in allowed_raw} if isinstance(allowed_raw, list) else set()
    protected = {str(value) for value in protected_raw} if isinstance(protected_raw, list) else set()
    if not allowed:
        blockers.append("causal_world_model_allowed_variables_missing")
    if not protected.issubset(allowed):
        blockers.append("causal_world_model_protected_variable_not_allowed")
    for name in allowed | protected:
        if not valid_name(name):
            blockers.append("causal_world_model_license_variable_name_invalid")
    return allowed, protected


def _check_variables(
    names: set[str], *, allowed: set[str], protected: set[str], allow_protected: bool, blockers: list[str]
) -> None:
    for name in names:
        if not valid_name(name):
            blockers.append("causal_world_model_variable_name_invalid")
        if name not in allowed:
            blockers.append("causal_world_model_variable_not_licensed")
        if name in protected and not allow_protected:
            blockers.append("causal_world_model_protected_variable_mutation")


def _license_checks(kind: str, license_packet: Mapping[str, Any], blockers: list[str]) -> None:
    if license_packet.get("license_status") != LICENSE_READY:
        blockers.append("causal_world_model_os_license_not_ready")
    for flag in ("state_read_allowed", "event_ledger_append_allowed", "result_write_allowed", "audit_append_allowed"):
        if license_packet.get(flag) is not True:
            blockers.append(flag.replace("allowed", "not_allowed"))
    allowed_kinds_raw = license_packet.get("allowed_command_kinds", [])
    allowed_kinds = {str(value) for value in allowed_kinds_raw} if isinstance(allowed_kinds_raw, list) else set()
    if kind not in allowed_kinds:
        blockers.append("causal_world_model_command_kind_not_licensed")
    kind_flags = {
        "initialize": ("initialize_allowed", "state_write_allowed", "direct_world_model_mutation_allowed"),
        "observe": ("observation_update_allowed", "state_write_allowed", "snapshot_write_allowed", "direct_world_model_mutation_allowed"),
        "intervene": ("intervention_allowed", "state_write_allowed", "snapshot_write_allowed", "direct_world_model_mutation_allowed"),
        "undo": ("undo_allowed", "state_write_allowed", "snapshot_read_allowed", "snapshot_write_allowed", "direct_world_model_mutation_allowed"),
        "counterfactual": ("counterfactual_allowed",),
        "inspect": ("inspect_allowed",),
    }
    for flag in kind_flags.get(kind, ()):
        if license_packet.get(flag) is not True:
            blockers.append(flag.replace("allowed", "not_allowed"))


def _validate_state(state: Mapping[str, Any], world_id: str, blockers: list[str]) -> None:
    if not state:
        blockers.append("causal_world_model_state_missing_or_invalid")
        return
    if state.get("version") != "kuuos_causal_world_model_state_v14_0":
        blockers.append("causal_world_model_state_version_invalid")
    if str(state.get("world_id", "")) != world_id:
        blockers.append("causal_world_model_world_id_mismatch")
    if not valid_digest(state, "world_model_digest"):
        blockers.append("causal_world_model_state_digest_invalid")
    variables = _m(state.get("variables"))
    mechanisms = _m(state.get("mechanisms"))
    if not variables:
        blockers.append("causal_world_model_variables_missing")
    validate_graph(variables, mechanisms, blockers)
    boundary = _m(state.get("boundary"))
    for name, expected in _state_boundary().items():
        if boundary.get(name) is not expected:
            blockers.append(f"causal_world_model_state_boundary_{name}_invalid")


def _finalize_state(
    state: dict[str, Any], *, before_digest: str, transaction_id: str, command_hash: str,
    process_context: Mapping[str, Any]
) -> None:
    prior_lineage = _m(state.get("lineage"))
    prior_history = str(prior_lineage.get("history_digest", "GENESIS"))
    context_digest = sha(dict(process_context))
    state["lineage"] = {
        "previous_world_model_digest": before_digest,
        "last_transaction_id": transaction_id,
        "last_command_digest": command_hash,
        "process_tensor_context_digest": context_digest,
        "history_digest": sha(
            {
                "previous_history_digest": prior_history,
                "previous_world_model_digest": before_digest,
                "transaction_id": transaction_id,
                "command_digest": command_hash,
                "process_tensor_context_digest": context_digest,
            }
        ),
    }
    state["boundary"] = _state_boundary()
    state["updated_epoch"] = int(time.time())
    state["world_model_digest"] = model_digest(state)


def _snapshot_path(root: pathlib.Path, transaction_id: str) -> pathlib.Path:
    return root / "kuuos_causal_world_model_snapshots_v14_0" / f"{_safe_id(transaction_id)}.json"


def _result_path(root: pathlib.Path, transaction_id: str) -> pathlib.Path:
    return root / "kuuos_causal_world_model_results_v14_0" / f"{_safe_id(transaction_id)}.json"


def build_kuuos_causal_world_model_os_v14_0(
    *, runtime_context: Mapping[str, Any], command: Mapping[str, Any], license_packet: Mapping[str, Any]
) -> KuuOSCausalWorldModelOSV14Result:
    ctx = _m(runtime_context)
    cmd = _m(command)
    lic = _m(license_packet)
    blockers: list[str] = []
    warnings: list[str] = []

    root_value = ctx.get("runtime_root")
    root = pathlib.Path(str(root_value)).expanduser().resolve() if root_value else pathlib.Path(".").resolve()
    if not root_value:
        blockers.append("runtime_root_missing")
    if root == pathlib.Path("/").resolve():
        blockers.append("runtime_root_forbidden")
    if ctx.get("kuuos_causal_world_model_os_v14_0_enabled") is not True:
        blockers.append("kuuos_causal_world_model_os_v14_0_enabled_not_true")
    if ctx.get("apply_kuuos_causal_world_model_os_v14_0") is not True:
        blockers.append("apply_kuuos_causal_world_model_os_v14_0_not_true")

    state_path = root / "kuuos_causal_world_model_state_v14_0.json"
    event_ledger_path = root / "kuuos_causal_world_model_event_ledger_v14_0.jsonl"
    audit_path = root / "kuuos_causal_world_model_audit_v14_0.jsonl"

    kind = str(cmd.get("kind", ""))
    transaction_id = str(cmd.get("transaction_id", ""))
    world_id = str(cmd.get("world_id", ""))
    result_path = _result_path(root, transaction_id)
    if kind not in COMMAND_KINDS:
        blockers.append("causal_world_model_command_kind_invalid")
    if not transaction_id or not valid_name(transaction_id):
        blockers.append("causal_world_model_transaction_id_invalid")
    if not world_id or not valid_name(world_id):
        blockers.append("causal_world_model_world_id_invalid")

    command_hash = command_digest(cmd) if cmd else ""
    if str(cmd.get("command_digest", "")) != command_hash:
        blockers.append("causal_world_model_command_digest_invalid")
    if str(lic.get("bound_command_digest", "")) != command_hash:
        blockers.append("causal_world_model_command_not_bound_to_license")
    _license_checks(kind, lic, blockers)
    process_context = _process_context(cmd, blockers)
    allowed, protected = _license_variables(lic, blockers)

    events = _records(event_ledger_path)
    if transaction_id and any(str(record.get("transaction_id", "")) == transaction_id for record in events):
        blockers.append("causal_world_model_transaction_replay")

    state = _read_json(state_path)
    before_digest = str(state.get("world_model_digest", "GENESIS")) if state else "GENESIS"
    after_digest = before_digest
    revision = int(state.get("revision", 0) or 0) if state else 0
    state_mutated = False
    counterfactual_generated = False
    undo_applied = False
    operation_result: dict[str, Any] = {}
    payload = _m(cmd.get("payload"))
    new_state: dict[str, Any] | None = None
    snapshot: tuple[pathlib.Path, dict[str, Any]] | None = None

    if kind == "initialize":
        if state:
            blockers.append("causal_world_model_initialize_overwrite_forbidden")
        variables_raw = _m(payload.get("variables"))
        mechanisms_raw = _m(payload.get("mechanisms"))
        if not variables_raw:
            blockers.append("causal_world_model_initialize_variables_missing")
        if len(variables_raw) > int(lic.get("max_variables", 256) or 256):
            blockers.append("causal_world_model_variable_limit_exceeded")
        if len(mechanisms_raw) > int(lic.get("max_mechanisms", 256) or 256):
            blockers.append("causal_world_model_mechanism_limit_exceeded")
        _check_variables(set(str(name) for name in variables_raw), allowed=allowed, protected=protected, allow_protected=True, blockers=blockers)
        variables = {str(name): normalize_variable(_m(value)) for name, value in variables_raw.items()}
        validate_graph(variables, mechanisms_raw, blockers)
        if not blockers:
            new_state = {
                "version": "kuuos_causal_world_model_state_v14_0",
                "world_id": world_id,
                "revision": 1,
                "variables": variables,
                "mechanisms": deepcopy(dict(mechanisms_raw)),
                "active_interventions": {},
                "created_epoch": int(time.time()),
                "lineage": {"history_digest": "GENESIS"},
                "boundary": _state_boundary(),
            }
            propagate(new_state, blockers)
            if not blockers:
                _finalize_state(new_state, before_digest="GENESIS", transaction_id=transaction_id, command_hash=command_hash, process_context=process_context)
                operation_result = {"initialized_variables": sorted(variables), "mechanism_targets": sorted(mechanisms_raw)}

    elif kind in COMMAND_KINDS - {"initialize"}:
        _validate_state(state, world_id, blockers)

        if kind == "observe":
            values = _m(payload.get("values"))
            uncertainties = _m(payload.get("uncertainties"))
            release_raw = payload.get("release_interventions", [])
            release = {str(value) for value in release_raw} if isinstance(release_raw, list) else set()
            touched = set(str(name) for name in values) | release
            if not values:
                blockers.append("causal_observation_values_missing")
            _check_variables(touched, allowed=allowed, protected=protected, allow_protected=False, blockers=blockers)
            path = _snapshot_path(root, transaction_id)
            if path.exists():
                blockers.append("causal_world_model_snapshot_already_exists")
            if not blockers:
                snapshot = (path, deepcopy(state))
                new_state = apply_observation(state, values, uncertainties, release, transaction_id, blockers)
                if not blockers:
                    new_state["revision"] = revision + 1
                    _finalize_state(new_state, before_digest=before_digest, transaction_id=transaction_id, command_hash=command_hash, process_context=process_context)
                    operation_result = {"observed_variables": sorted(values), "released_interventions": sorted(release)}

        elif kind == "intervene":
            values = _m(payload.get("set"))
            uncertainties = _m(payload.get("uncertainties"))
            release_raw = payload.get("release", [])
            release = {str(value) for value in release_raw} if isinstance(release_raw, list) else set()
            touched = set(str(name) for name in values) | release
            if not values and not release:
                blockers.append("causal_intervention_empty")
            _check_variables(touched, allowed=allowed, protected=protected, allow_protected=False, blockers=blockers)
            path = _snapshot_path(root, transaction_id)
            if path.exists():
                blockers.append("causal_world_model_snapshot_already_exists")
            if not blockers:
                snapshot = (path, deepcopy(state))
                new_state = apply_intervention(state, values, uncertainties, release, transaction_id, blockers)
                if not blockers:
                    new_state["revision"] = revision + 1
                    _finalize_state(new_state, before_digest=before_digest, transaction_id=transaction_id, command_hash=command_hash, process_context=process_context)
                    operation_result = {"set_interventions": sorted(values), "released_interventions": sorted(release)}

        elif kind == "undo":
            target_id = str(payload.get("target_transaction_id", ""))
            target_path = _snapshot_path(root, target_id)
            target = _read_json(target_path)
            if not target_id or not valid_name(target_id):
                blockers.append("causal_undo_target_transaction_id_invalid")
            if not target:
                blockers.append("causal_undo_snapshot_missing_or_invalid")
            elif not valid_digest(target, "world_model_digest"):
                blockers.append("causal_undo_snapshot_digest_invalid")
            elif str(target.get("world_id", "")) != world_id:
                blockers.append("causal_undo_snapshot_world_id_mismatch")
            undo_path = _snapshot_path(root, transaction_id)
            if undo_path.exists():
                blockers.append("causal_world_model_snapshot_already_exists")
            if not blockers:
                snapshot = (undo_path, deepcopy(state))
                new_state = deepcopy(target)
                new_state["revision"] = revision + 1
                new_state["restored_from_transaction_id"] = target_id
                propagate(new_state, blockers)
                if not blockers:
                    _finalize_state(new_state, before_digest=before_digest, transaction_id=transaction_id, command_hash=command_hash, process_context=process_context)
                    operation_result = {"undo_target_transaction_id": target_id, "restored_snapshot_digest": target["world_model_digest"]}
                    undo_applied = True

        elif kind == "counterfactual":
            values = _m(payload.get("do"))
            uncertainties = _m(payload.get("uncertainties"))
            release_raw = payload.get("release", [])
            release = {str(value) for value in release_raw} if isinstance(release_raw, list) else set()
            touched = set(str(name) for name in values) | release
            if not values and not release:
                blockers.append("causal_counterfactual_intervention_empty")
            _check_variables(touched, allowed=allowed, protected=protected, allow_protected=False, blockers=blockers)
            if not blockers:
                projected = apply_intervention(state, values, uncertainties, release, transaction_id, blockers, projection_only=True)
                if not blockers:
                    operation_result = {
                        "source_world_model_digest": before_digest,
                        "counterfactual_do": dict(values),
                        "released_interventions": sorted(release),
                        "projected_variables": deepcopy(projected.get("variables", {})),
                        "projected_active_interventions": deepcopy(projected.get("active_interventions", {})),
                        "variable_deltas": variable_deltas(state, projected),
                        "counterfactual_projection_digest": sha(
                            {
                                "source_world_model_digest": before_digest,
                                "do": dict(values),
                                "release": sorted(release),
                                "projected_variables": projected.get("variables", {}),
                                "process_tensor_context": process_context,
                            }
                        ),
                        "boundary": {
                            "projection_only": True,
                            "counterfactual_not_fact": True,
                            "persistent_world_model_not_mutated": True,
                            "external_world_not_actuated": True,
                        },
                    }
                    counterfactual_generated = True

        elif kind == "inspect" and not blockers:
            operation_result = {
                "world_id": world_id,
                "revision": revision,
                "world_model_digest": before_digest,
                "graph_digest": str(state.get("graph_digest", "")),
                "variables": deepcopy(state.get("variables", {})),
                "mechanisms": deepcopy(state.get("mechanisms", {})),
                "active_interventions": deepcopy(state.get("active_interventions", {})),
                "lineage": deepcopy(state.get("lineage", {})),
                "boundary": deepcopy(state.get("boundary", {})),
            }

    if new_state is not None and not blockers:
        if snapshot is not None:
            _write_json(snapshot[0], snapshot[1])
        _write_json(state_path, new_state)
        state_mutated = True
        after_digest = str(new_state.get("world_model_digest", ""))
        revision = int(new_state.get("revision", revision) or revision)
        operation_result["variable_deltas"] = variable_deltas(state, new_state)

    success = not blockers and (
        (kind in {"initialize", "observe", "intervene", "undo"} and state_mutated)
        or (kind == "counterfactual" and counterfactual_generated)
        or kind == "inspect"
    )

    event_record: dict[str, Any] = {}
    if success:
        event_record = {
            "version": "kuuos_causal_world_model_event_v14_0",
            "record_type": "kuuos_causal_world_model_event",
            "world_id": world_id,
            "transaction_id": transaction_id,
            "command_kind": kind,
            "command_digest": command_hash,
            "state_mutated": state_mutated,
            "counterfactual_generated": counterfactual_generated,
            "undo_applied": undo_applied,
            "revision": revision,
            "before_world_model_digest": before_digest,
            "after_world_model_digest": after_digest,
            "operation_result_digest": sha(operation_result),
            "process_tensor_context": process_context,
            "prev_record_digest": _latest_digest(event_ledger_path),
            "boundary": {
                "single_os_kernel_event": True,
                "direct_world_model_mutation_traceable": True,
                "external_world_actuation_authority": False,
                "world_model_state_not_truth_authority": True,
                "counterfactual_projection_not_fact": True,
                "decision_authority_separate": True,
                "execution_authority_separate": True,
                "non_markov_memory_lineage_preserved": True,
                "replay_protected": True,
            },
            "epoch": int(time.time()),
        }
        event_record["record_digest"] = sha(event_record)
        _append_jsonl(event_ledger_path, event_record)

    status = READY if success else BLOCKED
    result_payload = {
        "version": VERSION,
        "status": status,
        "packet_id": "kuuos-causal-world-model-v14-" + sha(
            {"world_id": world_id, "transaction_id": transaction_id, "kind": kind, "blockers": blockers}
        )[:16],
        "world_id": world_id,
        "transaction_id": transaction_id,
        "command_kind": kind,
        "state_mutated": state_mutated,
        "counterfactual_generated": counterfactual_generated,
        "undo_applied": undo_applied,
        "revision": revision,
        "before_world_model_digest": before_digest,
        "after_world_model_digest": after_digest,
        "operation_result": operation_result,
        "event_record_digest": str(event_record.get("record_digest", "")),
        "blockers": blockers,
        "warnings": warnings,
        "boundary": {
            "causal_world_model_os_v14": True,
            "direct_world_model_mutation_is_internal_model_state_change": True,
            "external_world_actuation_authority": False,
            "world_model_state_not_truth_authority": True,
            "counterfactual_projection_not_fact": True,
            "undo_is_real_state_restoration": True,
            "uncertainty_visible": True,
            "process_tensor_memory_required": True,
        },
        "epoch": int(time.time()),
    }
    result_payload["result_digest"] = sha(result_payload)
    if lic.get("result_write_allowed") is True and transaction_id:
        _write_json(result_path, result_payload)
    if lic.get("audit_append_allowed") is True:
        audit_record = {
            "version": "kuuos_causal_world_model_audit_v14_0",
            "world_id": world_id,
            "transaction_id": transaction_id,
            "command_kind": kind,
            "status": status,
            "command_digest": command_hash,
            "before_world_model_digest": before_digest,
            "after_world_model_digest": after_digest,
            "blockers": blockers,
            "warnings": warnings,
            "result_digest": result_payload["result_digest"],
            "epoch": int(time.time()),
        }
        audit_record["audit_record_digest"] = sha(audit_record)
        _append_jsonl(audit_path, audit_record)

    return KuuOSCausalWorldModelOSV14Result(
        VERSION,
        status,
        result_payload["packet_id"],
        str(root),
        kind,
        transaction_id,
        world_id,
        state_mutated,
        counterfactual_generated,
        undo_applied,
        revision,
        before_digest,
        after_digest,
        str(state_path),
        str(event_ledger_path),
        str(result_path),
        str(audit_path),
        blockers,
        warnings,
    )
