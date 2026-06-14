#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy
import hashlib
import json
import pathlib
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_causal_world_model_core_v14_0 import valid_digest as valid_v14_digest
from runtime.kuuos_runtime_daemon_indra_qi_causal_projection_bridge_v0_2 import (
    build_indra_qi_causal_projection_bridge_v0_2,
)
from runtime.kuuos_runtime_daemon_indra_qi_world_model_v0_1 import (
    build_indra_qi_world_model_v0_1,
    compute_indra_qi_world_state_digest,
)

INDRA_EXAMPLE = ROOT / "examples" / "indra_qi_world_model_v0_1.json"
PLAN_EXAMPLE = ROOT / "examples" / "indra_qi_causal_projection_plan_v0_2.json"


def sha(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def without(value: dict[str, Any], field: str) -> dict[str, Any]:
    result = dict(value)
    result.pop(field, None)
    return result


def valid_digest(value: dict[str, Any], field: str) -> bool:
    return bool(value.get(field)) and value[field] == sha(without(value, field))


def read_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def write_json(path: pathlib.Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def records(path: pathlib.Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def latest(path: pathlib.Path) -> dict[str, Any]:
    values = records(path)
    return values[-1] if values else {}


def build_source(root: pathlib.Path) -> dict[str, Any]:
    source_model = json.loads(INDRA_EXAMPLE.read_text(encoding="utf-8"))
    result = build_indra_qi_world_model_v0_1(
        world_model=source_model,
        runtime_context={
            "runtime_root": str(root),
            "indra_qi_world_model_enabled": True,
            "build_indra_qi_world_model": True,
        },
        world_model_license={
            "license_status": "INDRA_QI_WORLD_MODEL_LICENSE_READY",
            "world_model_validate_allowed": True,
            "world_state_write_allowed": True,
            "receipt_write_allowed": True,
            "audit_append_allowed": True,
        },
    ).to_dict()
    assert result["status"] == "INDRA_QI_WORLD_MODEL_READY", result
    return read_json(root / "ku_indra_qi_noncommutative_mandala_world_state.json")


def plan(source: dict[str, Any], suffix: str) -> dict[str, Any]:
    value = json.loads(PLAN_EXAMPLE.read_text(encoding="utf-8"))
    value["projection_id"] = f"indra-qi-projection-{suffix}"
    value["transaction_id"] = f"indra-qi-causal-init-{suffix}"
    value["causal_world_id"] = f"indra-qi-causal-world-{suffix}"
    value["source_indra_qi_world_state_digest"] = source["indra_qi_world_state_digest"]
    return value


def v14_template(variable_names: list[str], **overrides: Any) -> dict[str, Any]:
    value = {
        "license_status": "KUUOS_CAUSAL_WORLD_MODEL_OS_V14_0_LICENSE_READY",
        "state_read_allowed": True,
        "event_ledger_append_allowed": True,
        "result_write_allowed": True,
        "audit_append_allowed": True,
        "allowed_command_kinds": ["initialize"],
        "initialize_allowed": True,
        "state_write_allowed": True,
        "direct_world_model_mutation_allowed": True,
        "allowed_variables": variable_names,
        "protected_variables": [],
        "max_variables": 16,
        "max_mechanisms": 16,
    }
    value.update(overrides)
    return value


def bridge_license(variable_names: list[str], **overrides: Any) -> dict[str, Any]:
    value = {
        "license_status": "INDRA_QI_CAUSAL_PROJECTION_BRIDGE_V0_2_LICENSE_READY",
        "indra_qi_world_state_read_allowed": True,
        "projection_plan_validate_allowed": True,
        "projection_packet_write_allowed": True,
        "activation_record_write_allowed": True,
        "projection_ledger_append_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
        "v14_initialize_invoke_allowed": True,
        "v14_initialize_license_template": v14_template(variable_names),
    }
    value.update(overrides)
    return value


def context(root: pathlib.Path) -> dict[str, Any]:
    return {
        "runtime_root": str(root),
        "indra_qi_causal_projection_bridge_v0_2_enabled": True,
        "apply_indra_qi_causal_projection_bridge_v0_2": True,
    }


def run(root: pathlib.Path, projection_plan: dict[str, Any], license_value: dict[str, Any]) -> dict[str, Any]:
    return build_indra_qi_causal_projection_bridge_v0_2(
        runtime_context=context(root),
        projection_plan=projection_plan,
        projection_license=license_value,
    ).to_dict()


def main() -> int:
    with tempfile.TemporaryDirectory() as directory:
        base = pathlib.Path(directory)

        root = base / "success"
        source = build_source(root)
        projection_plan = plan(source, "success")
        variables = list(projection_plan["variables"])
        result = run(root, projection_plan, bridge_license(variables))
        assert result["status"] == "INDRA_QI_CAUSAL_PROJECTION_BRIDGE_V0_2_READY", result
        assert result["projection_status"] == "causal_projection_initialized"
        assert result["variable_count"] == 3
        assert result["mechanism_count"] == 1
        assert result["qi_flow_projection_count"] == 1
        assert result["v14_initialize_invoked"] is True
        assert result["v14_state_initialized"] is True
        assert result["source_indra_state_unchanged"] is True
        assert result["source_indra_state_digest"] == source["indra_qi_world_state_digest"]

        source_after = read_json(root / "ku_indra_qi_noncommutative_mandala_world_state.json")
        packet = read_json(root / "indra_qi_causal_projection_packet_v0_2.json")
        activation = read_json(root / "indra_qi_causal_projection_activation_record_v0_2.json")
        bridge_record = latest(root / "indra_qi_causal_projection_ledger_v0_2.jsonl")
        causal_state = read_json(root / "kuuos_causal_world_model_state_v14_0.json")
        causal_event = latest(root / "kuuos_causal_world_model_event_ledger_v14_0.jsonl")

        assert source_after["indra_qi_world_state_digest"] == source["indra_qi_world_state_digest"]
        assert compute_indra_qi_world_state_digest(source_after) == source["indra_qi_world_state_digest"]
        assert valid_digest(packet, "projection_packet_digest")
        assert valid_digest(activation, "activation_record_digest")
        assert valid_digest(bridge_record, "record_digest")
        assert valid_v14_digest(causal_state, "world_model_digest")
        assert valid_digest(causal_event, "record_digest")
        assert causal_state["world_id"] == projection_plan["causal_world_id"]
        assert causal_state["revision"] == 1
        assert set(causal_state["variables"]) == set(variables)
        assert causal_state["variables"]["adaptive_response"]["value"] == 0.78
        assert causal_state["boundary"]["external_world_actuation_authority"] is False
        assert causal_state["boundary"]["world_model_state_not_truth_authority"] is True
        assert causal_event["command_kind"] == "initialize"
        assert packet["variable_bindings"]["qi_flow_signal"]["qi_itself"] is False
        assert packet["variable_bindings"]["qi_flow_signal"]["projection_not_flow_identity"] is True
        assert packet["boundary"]["causal_edge_not_gauge_connection"] is True
        assert packet["boundary"]["source_indra_state_not_mutated"] is True
        assert activation["source_projection_packet_digest"] == packet["projection_packet_digest"]
        assert activation["v14_causal_world_model_digest"] == causal_state["world_model_digest"]
        assert bridge_record["source_activation_record_digest"] == activation["activation_record_digest"]
        assert bridge_record["v14_causal_world_model_digest"] == causal_state["world_model_digest"]

        projection_count = len(records(root / "indra_qi_causal_projection_ledger_v0_2.jsonl"))
        event_count = len(records(root / "kuuos_causal_world_model_event_ledger_v14_0.jsonl"))
        replay = run(root, projection_plan, bridge_license(variables))
        assert replay["status"].endswith("BLOCKED")
        assert "projection_id_replay" in replay["blockers"]
        assert "projection_transaction_replay" in replay["blockers"]
        assert replay["v14_initialize_invoked"] is False
        assert len(records(root / "indra_qi_causal_projection_ledger_v0_2.jsonl")) == projection_count
        assert len(records(root / "kuuos_causal_world_model_event_ledger_v14_0.jsonl")) == event_count

        root = base / "source-tamper"
        source = build_source(root)
        source_path = root / "ku_indra_qi_noncommutative_mandala_world_state.json"
        tampered = deepcopy(source)
        tampered["core_statement"]["qi_substance_claim"] = True
        write_json(source_path, tampered)
        projection_plan = plan(source, "source-tamper")
        result = run(root, projection_plan, bridge_license(list(projection_plan["variables"])))
        assert result["status"].endswith("BLOCKED")
        assert "indra_qi_world_state_digest_invalid" in result["blockers"]
        assert "indra_qi_source_qi_substance_claim_not_false" in result["blockers"]
        assert result["v14_initialize_invoked"] is False

        root = base / "qi-variable"
        source = build_source(root)
        projection_plan = plan(source, "qi-variable")
        projection_plan["variables"]["qi"] = projection_plan["variables"].pop("qi_flow_signal")
        mechanism = projection_plan["mechanisms"]["adaptive_response"]
        mechanism["parents"] = ["relational_load", "qi"]
        mechanism["weights"]["qi"] = mechanism["weights"].pop("qi_flow_signal")
        projection_plan["edge_annotations"]["qi->adaptive_response"] = projection_plan[
            "edge_annotations"
        ].pop("qi_flow_signal->adaptive_response")
        result = run(root, projection_plan, bridge_license(list(projection_plan["variables"])))
        assert result["status"].endswith("BLOCKED")
        assert "projection_variable_reifies_indra_qi_structure" in result["blockers"]
        assert result["v14_initialize_invoked"] is False

        root = base / "qi-identity"
        source = build_source(root)
        projection_plan = plan(source, "qi-identity")
        projection_plan["variables"]["qi_flow_signal"]["source_binding"]["qi_itself"] = True
        result = run(root, projection_plan, bridge_license(list(projection_plan["variables"])))
        assert result["status"].endswith("BLOCKED")
        assert "projection_variable_qi_flow_signal_qi_itself_not_false" in result["blockers"]

        root = base / "edge-confusion"
        source = build_source(root)
        projection_plan = plan(source, "edge-confusion")
        projection_plan["edge_annotations"]["qi_flow_signal->adaptive_response"]["not_indra_connection"] = False
        result = run(root, projection_plan, bridge_license(list(projection_plan["variables"])))
        assert result["status"].endswith("BLOCKED")
        assert "projection_edge_qi_flow_signal->adaptive_response_not_indra_connection_missing" in result["blockers"]

        root = base / "memory-loss"
        source = build_source(root)
        source_path = root / "ku_indra_qi_noncommutative_mandala_world_state.json"
        source["qi_flow_channels"][0]["process_tensor_context"]["memory_kernel_digest"] = ""
        source["indra_qi_world_state_digest"] = compute_indra_qi_world_state_digest(source)
        write_json(source_path, source)
        projection_plan = plan(source, "memory-loss")
        result = run(root, projection_plan, bridge_license(list(projection_plan["variables"])))
        assert result["status"].endswith("BLOCKED")
        assert "indra_qi_source_process_context_incomplete" in result["blockers"]
        assert result["v14_initialize_invoked"] is False

        root = base / "nested-license"
        source = build_source(root)
        projection_plan = plan(source, "nested-license")
        variable_names = list(projection_plan["variables"])
        nested = v14_template(variable_names, state_write_allowed=False)
        result = run(
            root,
            projection_plan,
            bridge_license(variable_names, v14_initialize_license_template=nested),
        )
        assert result["status"].endswith("BLOCKED")
        assert result["v14_initialize_invoked"] is True
        assert "v14_causal_world_model_initialize_not_ready" in result["blockers"]
        assert result["v14_state_initialized"] is False
        assert not (root / "kuuos_causal_world_model_state_v14_0.json").is_file()
        assert not (root / "indra_qi_causal_projection_ledger_v0_2.jsonl").is_file()

        root = base / "top-license"
        source = build_source(root)
        projection_plan = plan(source, "top-license")
        result = run(
            root,
            projection_plan,
            bridge_license(list(projection_plan["variables"]), v14_initialize_invoke_allowed=False),
        )
        assert result["status"].endswith("BLOCKED")
        assert "v14_initialize_invoke_not_allowed" in result["blockers"]
        assert result["v14_initialize_invoked"] is False
        assert not (root / "kuuos_causal_world_model_state_v14_0.json").is_file()

    print("indra_qi_causal_projection_bridge_v0_2 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
