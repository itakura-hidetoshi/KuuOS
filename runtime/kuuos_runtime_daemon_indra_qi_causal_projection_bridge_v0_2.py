#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy
from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping

from runtime.kuuos_causal_world_model_core_v14_0 import (
    command_digest,
    valid_digest as valid_v14_digest,
    valid_name,
    validate_graph,
)
from runtime.kuuos_causal_world_model_os_v14_0 import (
    build_kuuos_causal_world_model_os_v14_0,
)
from runtime.kuuos_runtime_daemon_indra_qi_world_model_v0_1 import (
    REQUIRED_BOUNDARIES,
    REQUIRED_PROCESS_CONTEXT,
    compute_indra_qi_world_state_digest,
)

VERSION = "indra_qi_causal_projection_bridge_v0_2"
READY = "INDRA_QI_CAUSAL_PROJECTION_BRIDGE_V0_2_READY"
BLOCKED = "INDRA_QI_CAUSAL_PROJECTION_BRIDGE_V0_2_BLOCKED"
LICENSE_READY = "INDRA_QI_CAUSAL_PROJECTION_BRIDGE_V0_2_LICENSE_READY"
PLAN_VERSION = "indra_qi_causal_projection_plan_v0_2"
RESERVED_VARIABLE_NAMES = {
    "qi",
    "indra_net",
    "gauge_connection",
    "holonomy",
    "emptiness",
    "ultimate_truth",
}
PLAN_BOUNDARIES = {
    "projection_only_from_indra_substrate": True,
    "qi_projected_as_observable_not_substance": True,
    "causal_dag_not_complete_world_ontology": True,
    "causal_edge_not_gauge_connection": True,
    "source_indra_state_not_mutated": True,
    "not_external_world_actuation_authority": True,
    "not_operator_algebra_mutation_authority": True,
    "candidate_weighting_not_truth": True,
    "non_markov_feedback_preserved": True,
    "fail_closed_on_boundary_loss": True,
}


@dataclass(frozen=True)
class IndraQiCausalProjectionBridgeV0_2Result:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    projection_id: str
    source_world_model_id: str
    causal_world_id: str
    transaction_id: str
    projection_status: str
    variable_count: int
    mechanism_count: int
    qi_flow_projection_count: int
    v14_initialize_invoked: bool
    v14_state_initialized: bool
    source_indra_state_unchanged: bool
    source_indra_state_digest: str
    causal_world_model_digest: str
    projection_packet_path: str
    activation_record_path: str
    projection_ledger_path: str
    receipt_path: str
    audit_path: str
    blockers: list[str]
    warnings: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _m(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _items(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _sha(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def _without(value: Mapping[str, Any], field: str) -> dict[str, Any]:
    payload = dict(value)
    payload.pop(field, None)
    return payload


def _valid_digest(value: Mapping[str, Any], field: str) -> bool:
    embedded = str(value.get(field, ""))
    return bool(embedded) and embedded == _sha(_without(value, field))


def _read_json(path: pathlib.Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return value if isinstance(value, dict) else {}


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


def _write_json(path: pathlib.Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(dict(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    os.replace(temporary, path)


def _append_jsonl(path: pathlib.Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(dict(payload), ensure_ascii=False, sort_keys=True) + "\n")


def _text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _source_indexes(source: Mapping[str, Any]) -> tuple[dict[str, Mapping[str, Any]], dict[str, Mapping[str, Any]]]:
    patches = {
        str(_m(item).get("patch_id", "")): _m(item)
        for item in _items(source.get("local_world_patches"))
        if str(_m(item).get("patch_id", ""))
    }
    flows = {
        str(_m(item).get("flow_id", "")): _m(item)
        for item in _items(source.get("qi_flow_channels"))
        if str(_m(item).get("flow_id", ""))
    }
    return patches, flows


def _validate_source(source: Mapping[str, Any], blockers: list[str]) -> None:
    if not source:
        blockers.append("indra_qi_world_state_missing_or_invalid")
        return
    if source.get("version") != "indra_qi_world_model_v0_1":
        blockers.append("indra_qi_world_state_version_invalid")
    if source.get("build_status") != "indra_qi_world_model_ready":
        blockers.append("indra_qi_world_state_not_ready")
    if str(source.get("indra_qi_world_state_digest", "")) != compute_indra_qi_world_state_digest(source):
        blockers.append("indra_qi_world_state_digest_invalid")
    core = _m(source.get("core_statement"))
    if core.get("indra_net") != "gauge_structured_relational_substrate":
        blockers.append("indra_qi_source_indra_net_definition_invalid")
    if core.get("qi") != "gauge_covariant_relational_effective_flow":
        blockers.append("indra_qi_source_qi_definition_invalid")
    if core.get("qi_substance_claim") is not False:
        blockers.append("indra_qi_source_qi_substance_claim_not_false")
    bridge = _m(source.get("causal_world_model_bridge"))
    for field in (
        "causal_dag_not_complete_world_ontology",
        "causal_edge_not_gauge_connection",
        "variable_value_not_qi_itself",
        "internal_causal_mutation_not_external_actuation",
    ):
        if bridge.get(field) is not True:
            blockers.append(f"indra_qi_source_causal_bridge_{field}_missing")
    governance = _m(source.get("governance_boundary"))
    for field, expected in REQUIRED_BOUNDARIES.items():
        if governance.get(field) is not expected:
            blockers.append(f"indra_qi_source_boundary_{field}_mismatch")
    if governance.get("direct_world_update_authority") is not False:
        blockers.append("indra_qi_source_direct_world_update_authority_not_false")
    if governance.get("operator_algebra_update_authority") is not False:
        blockers.append("indra_qi_source_operator_algebra_update_authority_not_false")


def _binding_digest_matches(
    binding: Mapping[str, Any], patches: Mapping[str, Mapping[str, Any]], flows: Mapping[str, Mapping[str, Any]]
) -> bool:
    kind = str(binding.get("binding_kind", ""))
    source_digest = str(binding.get("source_digest", ""))
    if kind == "local_patch_observable":
        patch = patches.get(str(binding.get("patch_id", "")), {})
        allowed = {
            str(patch.get("state_functional_digest", "")),
            str(patch.get("change_generator_digest", "")),
        }
        return bool(source_digest) and source_digest in allowed
    if kind == "qi_flow_observable_projection":
        flow = flows.get(str(binding.get("flow_id", "")), {})
        return bool(source_digest) and source_digest == str(flow.get("flow_observable_digest", ""))
    return False


def _validate_variables(
    variables: Mapping[str, Any],
    patches: Mapping[str, Mapping[str, Any]],
    flows: Mapping[str, Mapping[str, Any]],
    blockers: list[str],
) -> tuple[dict[str, dict[str, Any]], dict[str, dict[str, Any]], int]:
    if not variables:
        blockers.append("projection_variables_missing")
    causal_variables: dict[str, dict[str, Any]] = {}
    bindings: dict[str, dict[str, Any]] = {}
    qi_flow_projection_count = 0
    for name, raw in variables.items():
        variable_name = str(name)
        variable = _m(raw)
        if not valid_name(variable_name):
            blockers.append("projection_variable_name_invalid")
        if variable_name.lower() in RESERVED_VARIABLE_NAMES:
            blockers.append("projection_variable_reifies_indra_qi_structure")
        status = str(variable.get("status", "observed"))
        if status not in {"observed", "derived"}:
            blockers.append(f"projection_variable_{variable_name}_status_invalid")
        uncertainty = variable.get("uncertainty", 0.0)
        if isinstance(uncertainty, bool) or not isinstance(uncertainty, (int, float)) or float(uncertainty) < 0:
            blockers.append(f"projection_variable_{variable_name}_uncertainty_invalid")
        binding = dict(_m(variable.get("source_binding")))
        kind = str(binding.get("binding_kind", ""))
        if kind not in {"local_patch_observable", "qi_flow_observable_projection"}:
            blockers.append(f"projection_variable_{variable_name}_binding_kind_invalid")
        if not _text(binding.get("observable_id")):
            blockers.append(f"projection_variable_{variable_name}_observable_id_missing")
        if kind == "local_patch_observable":
            if str(binding.get("patch_id", "")) not in patches:
                blockers.append(f"projection_variable_{variable_name}_patch_unknown")
        elif kind == "qi_flow_observable_projection":
            qi_flow_projection_count += 1
            if str(binding.get("flow_id", "")) not in flows:
                blockers.append(f"projection_variable_{variable_name}_flow_unknown")
            if binding.get("qi_itself") is not False:
                blockers.append(f"projection_variable_{variable_name}_qi_itself_not_false")
            if binding.get("projection_not_flow_identity") is not True:
                blockers.append(f"projection_variable_{variable_name}_flow_identity_boundary_missing")
        if not _binding_digest_matches(binding, patches, flows):
            blockers.append(f"projection_variable_{variable_name}_source_digest_mismatch")
        bindings[variable_name] = binding
        causal_variables[variable_name] = {
            "value": variable.get("value"),
            "uncertainty": uncertainty,
            "status": status,
            "unit": str(variable.get("unit", "")),
            "provenance": [
                f"indra-qi-projection:{variable_name}",
                f"source-digest:{binding.get('source_digest', '')}",
            ],
        }
    if qi_flow_projection_count <= 0:
        blockers.append("qi_flow_observable_projection_missing")
    return causal_variables, bindings, qi_flow_projection_count


def _expected_edges(mechanisms: Mapping[str, Any]) -> set[str]:
    edges: set[str] = set()
    for target, raw in mechanisms.items():
        mechanism = _m(raw)
        for parent in _items(mechanism.get("parents")):
            edges.add(f"{parent}->{target}")
    return edges


def _validate_edge_annotations(
    mechanisms: Mapping[str, Any], annotations: Mapping[str, Any], blockers: list[str]
) -> None:
    expected = _expected_edges(mechanisms)
    actual = {str(key) for key in annotations}
    if expected != actual:
        blockers.append("projection_edge_annotation_set_mismatch")
    for edge in expected:
        annotation = _m(annotations.get(edge))
        if annotation.get("edge_kind") != "local_causal_projection_only":
            blockers.append(f"projection_edge_{edge}_kind_invalid")
        if annotation.get("not_indra_connection") is not True:
            blockers.append(f"projection_edge_{edge}_not_indra_connection_missing")
        if annotation.get("not_gauge_equivalence_claim") is not True:
            blockers.append(f"projection_edge_{edge}_not_gauge_equivalence_claim_missing")
        if annotation.get("not_qi_flow_identity") is not True:
            blockers.append(f"projection_edge_{edge}_not_qi_flow_identity_missing")


def _aggregate_process_context(source: Mapping[str, Any]) -> tuple[dict[str, str], dict[str, list[str]]]:
    raw_values: dict[str, list[str]] = {key: [] for key in REQUIRED_PROCESS_CONTEXT}
    for raw in _items(source.get("qi_flow_channels")):
        context = _m(_m(raw).get("process_tensor_context"))
        for key in REQUIRED_PROCESS_CONTEXT:
            raw_values[key].append(str(context.get(key, "")))
    normalized = {key: sorted(value for value in values if value) for key, values in raw_values.items()}
    aggregated = {key: _sha({"indra_qi_source_values": values}) for key, values in normalized.items()}
    return aggregated, normalized


def _validate_plan_boundaries(plan: Mapping[str, Any], blockers: list[str]) -> None:
    boundary = _m(plan.get("boundary"))
    for field, expected in PLAN_BOUNDARIES.items():
        if boundary.get(field) is not expected:
            blockers.append(f"projection_boundary_{field}_mismatch")


def build_indra_qi_causal_projection_bridge_v0_2(
    *,
    runtime_context: Mapping[str, Any],
    projection_plan: Mapping[str, Any],
    projection_license: Mapping[str, Any],
) -> IndraQiCausalProjectionBridgeV0_2Result:
    context = _m(runtime_context)
    plan = dict(_m(projection_plan))
    license_value = _m(projection_license)
    blockers: list[str] = []
    warnings: list[str] = []

    root_value = context.get("runtime_root")
    root = pathlib.Path(str(root_value)).expanduser().resolve() if root_value else pathlib.Path(".").resolve()
    if not root_value:
        blockers.append("runtime_root_missing")
    if root == pathlib.Path("/").resolve():
        blockers.append("runtime_root_forbidden")

    source_path = root / "ku_indra_qi_noncommutative_mandala_world_state.json"
    projection_packet_path = root / "indra_qi_causal_projection_packet_v0_2.json"
    activation_record_path = root / "indra_qi_causal_projection_activation_record_v0_2.json"
    projection_ledger_path = root / "indra_qi_causal_projection_ledger_v0_2.jsonl"
    receipt_path = root / "indra_qi_causal_projection_receipt_v0_2.json"
    audit_path = root / "indra_qi_causal_projection_audit_v0_2.jsonl"
    causal_state_path = root / "kuuos_causal_world_model_state_v14_0.json"

    if context.get("indra_qi_causal_projection_bridge_v0_2_enabled") is not True:
        blockers.append("indra_qi_causal_projection_bridge_v0_2_enabled_not_true")
    if context.get("apply_indra_qi_causal_projection_bridge_v0_2") is not True:
        blockers.append("apply_indra_qi_causal_projection_bridge_v0_2_not_true")
    if license_value.get("license_status") != LICENSE_READY:
        blockers.append("indra_qi_causal_projection_bridge_license_not_ready")
    for flag in (
        "indra_qi_world_state_read_allowed",
        "projection_plan_validate_allowed",
        "projection_packet_write_allowed",
        "activation_record_write_allowed",
        "projection_ledger_append_allowed",
        "receipt_write_allowed",
        "audit_append_allowed",
        "v14_initialize_invoke_allowed",
    ):
        if license_value.get(flag) is not True:
            blockers.append(flag.replace("allowed", "not_allowed"))

    source = _read_json(source_path)
    _validate_source(source, blockers)
    source_digest = str(source.get("indra_qi_world_state_digest", ""))
    source_world_model_id = str(source.get("world_model_id", ""))

    projection_id = str(plan.get("projection_id", ""))
    causal_world_id = str(plan.get("causal_world_id", ""))
    transaction_id = str(plan.get("transaction_id", ""))
    if plan.get("version") != PLAN_VERSION:
        blockers.append("projection_plan_version_invalid")
    for value, blocker in (
        (projection_id, "projection_id_invalid"),
        (causal_world_id, "causal_world_id_invalid"),
        (transaction_id, "projection_transaction_id_invalid"),
    ):
        if not value or not valid_name(value):
            blockers.append(blocker)
    if str(plan.get("source_world_model_id", "")) != source_world_model_id:
        blockers.append("projection_source_world_model_id_mismatch")
    if str(plan.get("source_indra_qi_world_state_digest", "")) != source_digest:
        blockers.append("projection_source_indra_state_digest_mismatch")
    _validate_plan_boundaries(plan, blockers)

    prior_records = _records(projection_ledger_path)
    if projection_id and any(str(record.get("projection_id", "")) == projection_id for record in prior_records):
        blockers.append("projection_id_replay")
    if transaction_id and any(str(record.get("transaction_id", "")) == transaction_id for record in prior_records):
        blockers.append("projection_transaction_replay")

    patches, flows = _source_indexes(source)
    variables_raw = _m(plan.get("variables"))
    mechanisms = deepcopy(dict(_m(plan.get("mechanisms"))))
    causal_variables, bindings, qi_flow_projection_count = _validate_variables(
        variables_raw, patches, flows, blockers
    )
    if not mechanisms:
        blockers.append("projection_mechanisms_missing")
    validate_graph(causal_variables, mechanisms, blockers)
    _validate_edge_annotations(mechanisms, _m(plan.get("edge_annotations")), blockers)

    process_context, source_process_context = _aggregate_process_context(source)
    if any(not values for values in source_process_context.values()):
        blockers.append("indra_qi_source_process_context_incomplete")

    variable_names = set(causal_variables)
    v14_template = dict(_m(license_value.get("v14_initialize_license_template")))
    allowed_raw = v14_template.get("allowed_variables", [])
    allowed_variables = {str(value) for value in allowed_raw} if isinstance(allowed_raw, list) else set()
    if allowed_variables != variable_names:
        blockers.append("v14_initialize_allowed_variables_not_exact_projection_set")
    protected_raw = v14_template.get("protected_variables", [])
    protected_variables = {str(value) for value in protected_raw} if isinstance(protected_raw, list) else set()
    if not protected_variables.issubset(variable_names):
        blockers.append("v14_initialize_protected_variables_outside_projection")

    command: dict[str, Any] = {
        "kind": "initialize",
        "transaction_id": transaction_id,
        "world_id": causal_world_id,
        "payload": {
            "variables": causal_variables,
            "mechanisms": mechanisms,
        },
        "process_tensor_context": process_context,
    }
    command["command_digest"] = command_digest(command)
    v14_license = dict(v14_template)
    v14_license["bound_command_digest"] = command["command_digest"]

    projection_packet: dict[str, Any] = {}
    activation_record: dict[str, Any] = {}
    v14_invoked = False
    v14_state_initialized = False
    source_unchanged = False
    causal_world_model_digest = ""
    v14_result: dict[str, Any] = {}

    if not blockers:
        projection_packet = {
            "version": VERSION,
            "projection_status": "projection_packet_ready",
            "projection_id": projection_id,
            "source_world_model_id": source_world_model_id,
            "source_indra_qi_world_state_digest": source_digest,
            "causal_world_id": causal_world_id,
            "transaction_id": transaction_id,
            "variable_bindings": bindings,
            "causal_variables": causal_variables,
            "causal_mechanisms": mechanisms,
            "edge_annotations": deepcopy(dict(_m(plan.get("edge_annotations")))),
            "aggregated_process_tensor_context": process_context,
            "source_process_tensor_context": source_process_context,
            "v14_initialize_command": command,
            "boundary": {
                **PLAN_BOUNDARIES,
                "v14_internal_causal_state_initialization_allowed": True,
                "v14_internal_causal_state_not_truth_authority": True,
                "v14_external_world_actuation_authority": False,
                "projection_lineage_digest_bound": True,
            },
            "epoch": int(time.time()),
        }
        projection_packet["projection_packet_digest"] = _sha(projection_packet)
        if license_value.get("projection_packet_write_allowed") is True:
            _write_json(projection_packet_path, projection_packet)

        v14_result = build_kuuos_causal_world_model_os_v14_0(
            runtime_context={
                "runtime_root": str(root),
                "kuuos_causal_world_model_os_v14_0_enabled": True,
                "apply_kuuos_causal_world_model_os_v14_0": True,
            },
            command=command,
            license_packet=v14_license,
        ).to_dict()
        v14_invoked = True
        if v14_result.get("status") != "KUUOS_CAUSAL_WORLD_MODEL_OS_V14_0_READY":
            blockers.append("v14_causal_world_model_initialize_not_ready")
        if v14_result.get("state_mutated") is not True or int(v14_result.get("revision", 0) or 0) != 1:
            blockers.append("v14_causal_world_model_initialize_state_mismatch")

    causal_state = _read_json(causal_state_path) if v14_invoked else {}
    if v14_invoked and not blockers:
        if not valid_v14_digest(causal_state, "world_model_digest"):
            blockers.append("v14_causal_world_model_state_digest_invalid")
        if str(causal_state.get("world_id", "")) != causal_world_id:
            blockers.append("v14_causal_world_model_world_id_mismatch")
        if set(_m(causal_state.get("variables"))) != variable_names:
            blockers.append("v14_causal_world_model_variable_set_mismatch")
        if dict(_m(causal_state.get("mechanisms"))) != mechanisms:
            blockers.append("v14_causal_world_model_mechanism_set_mismatch")
        boundary = _m(causal_state.get("boundary"))
        if boundary.get("external_world_actuation_authority") is not False:
            blockers.append("v14_causal_world_model_external_actuation_boundary_invalid")
        if boundary.get("world_model_state_not_truth_authority") is not True:
            blockers.append("v14_causal_world_model_truth_boundary_invalid")
        causal_world_model_digest = str(causal_state.get("world_model_digest", ""))

    source_after = _read_json(source_path)
    if source and source_after:
        source_unchanged = (
            str(source_after.get("indra_qi_world_state_digest", "")) == source_digest
            and compute_indra_qi_world_state_digest(source_after) == source_digest
        )
    if v14_invoked and not source_unchanged:
        blockers.append("source_indra_qi_world_state_changed_during_projection")

    projection_status = (
        "causal_projection_initialized"
        if v14_invoked and not blockers
        else "causal_projection_blocked"
    )
    if projection_status == "causal_projection_initialized":
        v14_state_initialized = True
        activation_record = {
            "version": "indra_qi_causal_projection_activation_record_v0_2",
            "activation_status": "causal_projection_initialized",
            "projection_id": projection_id,
            "source_world_model_id": source_world_model_id,
            "source_indra_qi_world_state_digest": source_digest,
            "causal_world_id": causal_world_id,
            "transaction_id": transaction_id,
            "source_projection_packet_digest": str(projection_packet.get("projection_packet_digest", "")),
            "v14_command_digest": str(command.get("command_digest", "")),
            "v14_event_record_digest": str(v14_result.get("event_record_digest", "")),
            "v14_causal_world_model_digest": causal_world_model_digest,
            "source_indra_state_unchanged": source_unchanged,
            "boundary": {
                **PLAN_BOUNDARIES,
                "causal_world_model_initialized": True,
                "causal_initialization_is_internal_model_state_change": True,
                "external_world_not_actuated": True,
                "source_operator_algebras_unchanged": True,
                "source_gauge_connections_unchanged": True,
            },
            "epoch": int(time.time()),
        }
        activation_record["activation_record_digest"] = _sha(activation_record)
        if license_value.get("activation_record_write_allowed") is True:
            _write_json(activation_record_path, activation_record)

        ledger_record = {
            "version": "indra_qi_causal_projection_ledger_record_v0_2",
            "record_type": "indra_qi_causal_projection",
            "projection_id": projection_id,
            "transaction_id": transaction_id,
            "source_world_model_id": source_world_model_id,
            "causal_world_id": causal_world_id,
            "source_indra_qi_world_state_digest": source_digest,
            "source_projection_packet_digest": projection_packet["projection_packet_digest"],
            "source_activation_record_digest": activation_record["activation_record_digest"],
            "v14_causal_world_model_digest": causal_world_model_digest,
            "prev_record_digest": str(prior_records[-1].get("record_digest", "GENESIS")) if prior_records else "GENESIS",
            "boundary": {
                "projection_consumed_once": True,
                "source_indra_state_immutable_during_projection": True,
                "qi_observable_projection_traceable": True,
                "causal_edges_not_gauge_connections": True,
                "non_markov_feedback_preserved": True,
                "replay_protected": True,
            },
            "epoch": int(time.time()),
        }
        ledger_record["record_digest"] = _sha(ledger_record)
        if license_value.get("projection_ledger_append_allowed") is True:
            _append_jsonl(projection_ledger_path, ledger_record)

    status = READY if projection_status == "causal_projection_initialized" else BLOCKED
    receipt = {
        "version": VERSION,
        "status": status,
        "packet_id": "indra-qi-causal-projection-"
        + _sha(
            {
                "projection_id": projection_id,
                "source_digest": source_digest,
                "causal_digest": causal_world_model_digest,
                "blockers": blockers,
            }
        )[:16],
        "projection_id": projection_id,
        "source_world_model_id": source_world_model_id,
        "causal_world_id": causal_world_id,
        "transaction_id": transaction_id,
        "projection_status": projection_status,
        "variable_count": len(causal_variables),
        "mechanism_count": len(mechanisms),
        "qi_flow_projection_count": qi_flow_projection_count,
        "v14_initialize_invoked": v14_invoked,
        "v14_state_initialized": v14_state_initialized,
        "source_indra_state_unchanged": source_unchanged,
        "source_indra_state_digest": source_digest,
        "causal_world_model_digest": causal_world_model_digest,
        "blockers": blockers,
        "warnings": warnings,
        "boundary": {
            **PLAN_BOUNDARIES,
            "v14_internal_causal_state_initialized": v14_state_initialized,
            "external_world_not_actuated": True,
        },
        "epoch": int(time.time()),
    }
    if license_value.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if license_value.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "audit_record_digest": _sha(receipt)})

    return IndraQiCausalProjectionBridgeV0_2Result(
        VERSION,
        status,
        receipt["packet_id"],
        str(root),
        projection_id,
        source_world_model_id,
        causal_world_id,
        transaction_id,
        projection_status,
        len(causal_variables),
        len(mechanisms),
        qi_flow_projection_count,
        v14_invoked,
        v14_state_initialized,
        source_unchanged,
        source_digest,
        causal_world_model_digest,
        str(projection_packet_path),
        str(activation_record_path),
        str(projection_ledger_path),
        str(receipt_path),
        str(audit_path),
        blockers,
        warnings,
    )
