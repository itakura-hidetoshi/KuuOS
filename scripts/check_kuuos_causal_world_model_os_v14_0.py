#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_causal_world_model_core_v14_0 import command_digest, valid_digest
from runtime.kuuos_causal_world_model_os_v14_0 import build_kuuos_causal_world_model_os_v14_0

WORLD_ID = "ResearchWorld"
PROCESS_CONTEXT = {
    "process_tensor_digest": "process-v14-digest",
    "memory_kernel_digest": "memory-v14-digest",
    "history_window_digest": "history-v14-digest",
    "instrument_trace_digest": "instrument-v14-digest",
    "non_markov_context_digest": "non-markov-v14-digest",
}


def read_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def records(path: pathlib.Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def command(kind: str, transaction_id: str, payload: dict[str, Any], *, process: bool = True) -> dict[str, Any]:
    value: dict[str, Any] = {
        "version": "kuuos_causal_world_model_command_v14_0",
        "kind": kind,
        "transaction_id": transaction_id,
        "world_id": WORLD_ID,
        "payload": payload,
        "process_tensor_context": dict(PROCESS_CONTEXT) if process else {},
    }
    value["command_digest"] = command_digest(value)
    return value


def license_packet(cmd: dict[str, Any], **overrides: Any) -> dict[str, Any]:
    value = {
        "license_status": "KUUOS_CAUSAL_WORLD_MODEL_OS_V14_0_LICENSE_READY",
        "bound_command_digest": cmd["command_digest"],
        "allowed_command_kinds": ["initialize", "observe", "intervene", "undo", "counterfactual", "inspect"],
        "allowed_variables": ["X", "Y", "Z", "Guard"],
        "protected_variables": ["Guard"],
        "max_variables": 64,
        "max_mechanisms": 64,
        "state_read_allowed": True,
        "state_write_allowed": True,
        "event_ledger_append_allowed": True,
        "result_write_allowed": True,
        "audit_append_allowed": True,
        "snapshot_write_allowed": True,
        "snapshot_read_allowed": True,
        "direct_world_model_mutation_allowed": True,
        "initialize_allowed": True,
        "observation_update_allowed": True,
        "intervention_allowed": True,
        "undo_allowed": True,
        "counterfactual_allowed": True,
        "inspect_allowed": True,
    }
    value.update(overrides)
    return value


def context(root: pathlib.Path) -> dict[str, Any]:
    return {
        "kuuos_causal_world_model_os_v14_0_enabled": True,
        "apply_kuuos_causal_world_model_os_v14_0": True,
        "runtime_root": str(root),
    }


def run(root: pathlib.Path, cmd: dict[str, Any], lic: dict[str, Any] | None = None) -> dict[str, Any]:
    return build_kuuos_causal_world_model_os_v14_0(
        runtime_context=context(root),
        command=cmd,
        license_packet=lic if lic is not None else license_packet(cmd),
    ).to_dict()


def initialize_command() -> dict[str, Any]:
    return command(
        "initialize",
        "txInit",
        {
            "variables": {
                "X": {"value": 1.0, "uncertainty": 0.1, "unit": "u"},
                "Y": {"value": 0.0, "uncertainty": 0.0, "unit": "u"},
                "Z": {"value": 0.0, "uncertainty": 0.0, "unit": "u"},
                "Guard": {"value": 1.0, "uncertainty": 0.0, "unit": "flag"},
            },
            "mechanisms": {
                "Y": {
                    "type": "affine",
                    "parents": ["X"],
                    "weights": {"X": 2.0},
                    "bias": 1.0,
                    "noise": 0.1,
                },
                "Z": {
                    "type": "affine",
                    "parents": ["Y", "X"],
                    "weights": {"Y": 1.0, "X": -1.0},
                    "bias": 0.0,
                    "noise": 0.2,
                },
            },
        },
    )


def main() -> int:
    with tempfile.TemporaryDirectory() as directory:
        root = pathlib.Path(directory) / "world"
        state_path = root / "kuuos_causal_world_model_state_v14_0.json"
        ledger_path = root / "kuuos_causal_world_model_event_ledger_v14_0.jsonl"

        init = initialize_command()
        result = run(root, init)
        assert result["status"] == "KUUOS_CAUSAL_WORLD_MODEL_OS_V14_0_READY", result
        assert result["state_mutated"] is True
        assert result["revision"] == 1
        state = read_json(state_path)
        assert valid_digest(state, "world_model_digest")
        assert state["variables"]["X"]["value"] == 1.0
        assert state["variables"]["Y"]["value"] == 3.0
        assert state["variables"]["Z"]["value"] == 2.0
        assert state["boundary"]["direct_world_model_mutation_enabled"] is True
        assert state["boundary"]["external_world_actuation_authority"] is False
        init_digest = state["world_model_digest"]

        observe = command(
            "observe",
            "txObserve",
            {"values": {"X": 3.0}, "uncertainties": {"X": 0.2}, "release_interventions": []},
        )
        result = run(root, observe)
        assert result["status"] == "KUUOS_CAUSAL_WORLD_MODEL_OS_V14_0_READY", result
        assert result["before_world_model_digest"] == init_digest
        assert result["revision"] == 2
        state = read_json(state_path)
        assert state["variables"]["X"]["value"] == 3.0
        assert state["variables"]["Y"]["value"] == 7.0
        assert state["variables"]["Z"]["value"] == 4.0
        observed_digest = state["world_model_digest"]
        assert read_json(root / "kuuos_causal_world_model_snapshots_v14_0" / "txObserve.json")[
            "world_model_digest"
        ] == init_digest

        intervene = command(
            "intervene",
            "txDo",
            {"set": {"X": 5.0}, "uncertainties": {"X": 0.0}, "release": []},
        )
        result = run(root, intervene)
        assert result["status"] == "KUUOS_CAUSAL_WORLD_MODEL_OS_V14_0_READY", result
        assert result["revision"] == 3
        state = read_json(state_path)
        assert state["variables"]["X"]["status"] == "intervened"
        assert state["variables"]["X"]["value"] == 5.0
        assert state["variables"]["Y"]["value"] == 11.0
        assert state["variables"]["Z"]["value"] == 6.0
        assert state["active_interventions"]["X"]["transaction_id"] == "txDo"
        intervened_digest = state["world_model_digest"]
        assert read_json(root / "kuuos_causal_world_model_snapshots_v14_0" / "txDo.json")[
            "world_model_digest"
        ] == observed_digest

        counterfactual = command(
            "counterfactual",
            "txCounterfactual",
            {"do": {"X": 2.0}, "uncertainties": {"X": 0.0}, "release": []},
        )
        result = run(root, counterfactual)
        assert result["status"] == "KUUOS_CAUSAL_WORLD_MODEL_OS_V14_0_READY", result
        assert result["state_mutated"] is False
        assert result["counterfactual_generated"] is True
        assert result["before_world_model_digest"] == intervened_digest
        assert result["after_world_model_digest"] == intervened_digest
        assert read_json(state_path)["world_model_digest"] == intervened_digest
        counterfactual_result = read_json(
            root / "kuuos_causal_world_model_results_v14_0" / "txCounterfactual.json"
        )
        projected = counterfactual_result["operation_result"]["projected_variables"]
        assert projected["X"]["value"] == 2.0
        assert projected["Y"]["value"] == 5.0
        assert projected["Z"]["value"] == 3.0
        assert counterfactual_result["boundary"]["counterfactual_projection_not_fact"] is True
        assert counterfactual_result["operation_result"]["boundary"]["persistent_world_model_not_mutated"] is True

        undo = command("undo", "txUndo", {"target_transaction_id": "txDo"})
        result = run(root, undo)
        assert result["status"] == "KUUOS_CAUSAL_WORLD_MODEL_OS_V14_0_READY", result
        assert result["state_mutated"] is True
        assert result["undo_applied"] is True
        assert result["revision"] == 4
        state = read_json(state_path)
        assert state["restored_from_transaction_id"] == "txDo"
        assert state["variables"]["X"]["value"] == 3.0
        assert state["variables"]["Y"]["value"] == 7.0
        assert state["variables"]["Z"]["value"] == 4.0
        assert state["active_interventions"] == {}
        assert valid_digest(state, "world_model_digest")

        inspect = command("inspect", "txInspect", {})
        result = run(root, inspect)
        assert result["status"] == "KUUOS_CAUSAL_WORLD_MODEL_OS_V14_0_READY", result
        assert result["state_mutated"] is False
        inspect_result = read_json(root / "kuuos_causal_world_model_results_v14_0" / "txInspect.json")
        assert inspect_result["operation_result"]["revision"] == 4
        assert inspect_result["operation_result"]["variables"]["X"]["value"] == 3.0

        event_records = records(ledger_path)
        assert [record["command_kind"] for record in event_records] == [
            "initialize",
            "observe",
            "intervene",
            "counterfactual",
            "undo",
            "inspect",
        ]
        previous = "GENESIS"
        for record in event_records:
            assert valid_digest(record, "record_digest")
            assert record["prev_record_digest"] == previous
            assert record["boundary"]["single_os_kernel_event"] is True
            assert record["boundary"]["non_markov_memory_lineage_preserved"] is True
            previous = record["record_digest"]

        before_count = len(event_records)
        replay = run(root, inspect)
        assert replay["status"].endswith("BLOCKED")
        assert "causal_world_model_transaction_replay" in replay["blockers"]
        assert len(records(ledger_path)) == before_count

        protected = command("observe", "txProtected", {"values": {"Guard": 0.0}})
        protected_result = run(root, protected)
        assert protected_result["status"].endswith("BLOCKED")
        assert "causal_world_model_protected_variable_mutation" in protected_result["blockers"]
        assert len(records(ledger_path)) == before_count

        no_context = command("inspect", "txNoContext", {}, process=False)
        no_context_result = run(root, no_context)
        assert no_context_result["status"].endswith("BLOCKED")
        assert "process_tensor_context_process_tensor_digest_missing" in no_context_result["blockers"]

        license_block = command("observe", "txLicenseBlock", {"values": {"X": 9.0}})
        license_block_result = run(
            root,
            license_block,
            license_packet(license_block, direct_world_model_mutation_allowed=False),
        )
        assert license_block_result["status"].endswith("BLOCKED")
        assert "direct_world_model_mutation_not_allowed" in license_block_result["blockers"]
        assert read_json(state_path)["variables"]["X"]["value"] == 3.0

        tampered = command("observe", "txTampered", {"values": {"X": 8.0}})
        tampered_license = license_packet(tampered)
        tampered["payload"]["values"]["X"] = 10.0
        tampered_result = run(root, tampered, tampered_license)
        assert tampered_result["status"].endswith("BLOCKED")
        assert "causal_world_model_command_digest_invalid" in tampered_result["blockers"]
        assert "causal_world_model_command_not_bound_to_license" in tampered_result["blockers"]

        cycle_root = pathlib.Path(directory) / "cycle"
        cycle = command(
            "initialize",
            "txCycle",
            {
                "variables": {"X": {"value": 1.0}, "Y": {"value": 1.0}},
                "mechanisms": {
                    "X": {"type": "affine", "parents": ["Y"], "weights": {"Y": 1.0}},
                    "Y": {"type": "affine", "parents": ["X"], "weights": {"X": 1.0}},
                },
            },
        )
        cycle_result = run(cycle_root, cycle)
        assert cycle_result["status"].endswith("BLOCKED")
        assert "causal_graph_cycle_detected" in cycle_result["blockers"]
        assert not (cycle_root / "kuuos_causal_world_model_state_v14_0.json").exists()

    print("KuuOS causal world model OS v14.0 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
