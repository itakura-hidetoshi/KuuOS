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

from runtime.kuuos_runtime_daemon_indra_qi_world_model_v0_1 import (
    build_indra_qi_world_model_v0_1,
    compute_indra_qi_world_state_digest,
)

EXAMPLE = ROOT / "examples" / "indra_qi_world_model_v0_1.json"


def load_example() -> dict[str, Any]:
    return json.loads(EXAMPLE.read_text(encoding="utf-8"))


def runtime_context(root: pathlib.Path) -> dict[str, Any]:
    return {
        "runtime_root": str(root),
        "indra_qi_world_model_enabled": True,
        "build_indra_qi_world_model": True,
    }


def license_packet(**overrides: Any) -> dict[str, Any]:
    value = {
        "license_status": "INDRA_QI_WORLD_MODEL_LICENSE_READY",
        "world_model_validate_allowed": True,
        "world_state_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }
    value.update(overrides)
    return value


def run(root: pathlib.Path, model: dict[str, Any], license_value: dict[str, Any] | None = None) -> dict[str, Any]:
    return build_indra_qi_world_model_v0_1(
        world_model=model,
        runtime_context=runtime_context(root),
        world_model_license=license_value or license_packet(),
    ).to_dict()


def read_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def assert_blocked(root: pathlib.Path, model: dict[str, Any], blocker: str) -> None:
    result = run(root, model)
    assert result["status"] == "INDRA_QI_WORLD_MODEL_BLOCKED", result
    assert blocker in result["blockers"], result
    assert not (root / "ku_indra_qi_noncommutative_mandala_world_state.json").is_file()


def main() -> int:
    with tempfile.TemporaryDirectory() as directory:
        base = pathlib.Path(directory)

        success_root = base / "success"
        result = run(success_root, load_example())
        assert result["status"] == "INDRA_QI_WORLD_MODEL_READY", result
        assert result["local_patch_count"] == 2
        assert result["connection_count"] == 2
        assert result["qi_flow_count"] == 2
        assert result["holonomy_cycle_count"] == 1
        assert result["string_correspondence_count"] == 2
        assert result["m_brane_surface_count"] == 2
        state = read_json(success_root / "ku_indra_qi_noncommutative_mandala_world_state.json")
        receipt = read_json(success_root / "ku_indra_qi_noncommutative_mandala_world_receipt.json")
        assert state["core_statement"]["indra_net"] == "gauge_structured_relational_substrate"
        assert state["core_statement"]["qi"] == "gauge_covariant_relational_effective_flow"
        assert state["core_statement"]["qi_substance_claim"] is False
        assert state["indra_qi_world_state_digest"] == compute_indra_qi_world_state_digest(state)
        assert receipt["state_digest"] == state["indra_qi_world_state_digest"]
        bridge = state["causal_world_model_bridge"]
        assert bridge["target"] == "kuuos_causal_world_model_os_v14_0"
        assert bridge["causal_dag_not_complete_world_ontology"] is True
        assert bridge["causal_edge_not_gauge_connection"] is True
        assert bridge["variable_value_not_qi_itself"] is True
        assert bridge["internal_causal_mutation_not_external_actuation"] is True

        candidate = load_example()
        candidate["qi_flow_channels"][0]["substance_claim"] = True
        assert_blocked(base / "qi-substance", candidate, "qi_flow_0_substance_claim_not_false")

        candidate = load_example()
        candidate["qi_flow_channels"][0]["target_patch"] = "world-a"
        assert_blocked(base / "endpoint", candidate, "qi_flow_0_connection_endpoint_mismatch")

        candidate = load_example()
        candidate["local_world_patches"][0]["operator_algebra"]["noncommutative_ordering_required"] = False
        assert_blocked(base / "ordering", candidate, "local_patch_0_noncommutative_ordering_not_required")

        candidate = load_example()
        candidate["holonomy_cycles"][0]["holonomy_preserved"] = False
        assert_blocked(base / "holonomy", candidate, "holonomy_cycle_0_not_preserved")

        candidate = load_example()
        candidate["mandala_inclusion"]["single_ontology_forced"] = True
        assert_blocked(base / "collapse", candidate, "mandala_single_ontology_forced_not_false")

        candidate = load_example()
        candidate["two_truths_boundary"]["two_truths_gap_preserved"] = False
        assert_blocked(base / "two-truths", candidate, "two_truths_two_truths_gap_preserved_not_true")

        candidate = load_example()
        candidate["qi_flow_channels"][0]["process_tensor_context"]["memory_kernel_digest"] = ""
        assert_blocked(base / "memory", candidate, "qi_flow_0_memory_kernel_digest_missing")

        candidate = load_example()
        candidate["governance_boundary"]["direct_world_update_authority"] = True
        assert_blocked(base / "authority", candidate, "direct_world_update_authority_not_false")

        candidate = load_example()
        candidate["governance_boundary"]["structural_bridge_not_physical_theorem_authority"] = False
        assert_blocked(
            base / "reification",
            candidate,
            "governance_boundary_structural_bridge_not_physical_theorem_authority_mismatch",
        )

        blocked_root = base / "license"
        result = run(blocked_root, load_example(), license_packet(world_state_write_allowed=False))
        assert result["status"] == "INDRA_QI_WORLD_MODEL_BLOCKED", result
        assert "world_state_write_not_allowed" in result["blockers"]
        assert not (blocked_root / "ku_indra_qi_noncommutative_mandala_world_state.json").is_file()

    print("indra_qi_world_model_v0_1 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
