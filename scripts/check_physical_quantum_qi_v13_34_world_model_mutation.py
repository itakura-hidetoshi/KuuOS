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

from runtime.kuuos_runtime_daemon_physical_quantum_qi_v13_34_world_model_mutation import (
    build_physical_quantum_qi_v13_34_world_model_mutation,
    compute_world_model_digest,
    compute_world_model_mutation_plan_digest,
)
from scripts.check_physical_quantum_qi_v13_33_guarded_intent_activation import (
    activation_license as v13_33_license,
    prepare_v13_32,
    run as run_v13_33,
)


def read_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def write_json(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def latest_jsonl(path: pathlib.Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    lines = [line for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    return json.loads(lines[-1]) if lines else {}


def prepare_v13_33(root: pathlib.Path, kind: str) -> None:
    prepare_v13_32(root, kind)
    result = run_v13_33(root, v13_33_license())
    assert result["status"] == "PHYSICAL_QUANTUM_QI_V13_33_GUARDED_INTENT_ACTIVATION_READY", result


def initial_world_state(root: pathlib.Path) -> dict[str, Any]:
    state = {
        "version": "physical_quantum_qi_world_model_state_v13_34",
        "revision": 0,
        "state": {
            "clinical": {"status": "baseline", "confidence": 0.5},
            "network": {"harmony_score": 0.4},
            "events": [],
            "system": {"immutable_root": True},
        },
        "boundary": {"world_model_state_only": True},
    }
    state["world_model_digest"] = compute_world_model_digest(state)
    write_json(root / "physical_quantum_qi_world_model_state.json", state)
    return state


def intent_digest(root: pathlib.Path) -> str:
    packet = read_json(root / "physical_quantum_qi_guarded_execution_intent_packet.json")
    intents = packet.get("guarded_execution_intents", [])
    return str(intents[0].get("guarded_execution_intent_digest", "")) if isinstance(intents, list) and intents else ""


def mutation_plan(
    root: pathlib.Path,
    mutation_id: str,
    operations: list[dict[str, Any]],
    *,
    expected_digest: str | None = None,
    source_intent_digest: str | None = None,
) -> dict[str, Any]:
    state = read_json(root / "physical_quantum_qi_world_model_state.json")
    plan = {
        "version": "physical_quantum_qi_world_model_mutation_plan_v13_34",
        "mutation_id": mutation_id,
        "reason": "licensed direct WORLD model update",
        "rollback_required": True,
        "expected_world_model_digest": expected_digest if expected_digest is not None else compute_world_model_digest(state),
        "source_guarded_execution_intent_digest": source_intent_digest if source_intent_digest is not None else intent_digest(root),
        "operations": operations,
    }
    plan["mutation_plan_digest"] = compute_world_model_mutation_plan_digest(plan)
    return plan


def license_packet(plan: dict[str, Any], **overrides: Any) -> dict[str, Any]:
    value = {
        "license_status": "PHYSICAL_QUANTUM_QI_V13_34_WORLD_MODEL_MUTATION_LICENSE_READY",
        "v13_33_activation_record_read_allowed": True,
        "guarded_execution_intent_packet_read_allowed": True,
        "world_model_state_read_allowed": True,
        "world_model_state_write_allowed": True,
        "rollback_snapshot_write_allowed": True,
        "mutation_ledger_append_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
        "direct_world_model_mutation_allowed": True,
        "allowed_path_prefixes": ["/state"],
        "protected_paths": ["/state/system", "/governance", "/licenses", "/audit"],
        "max_operations": 16,
        "bound_mutation_plan_digest": plan["mutation_plan_digest"],
    }
    value.update(overrides)
    return value


def context(root: pathlib.Path, plan: dict[str, Any]) -> dict[str, Any]:
    return {
        "physical_quantum_qi_v13_34_world_model_mutation_enabled": True,
        "apply_physical_quantum_qi_v13_34_world_model_mutation": True,
        "runtime_root": str(root),
        "world_model_mutation_plan": plan,
    }


def run(root: pathlib.Path, plan: dict[str, Any], license_value: dict[str, Any]) -> dict[str, Any]:
    return build_physical_quantum_qi_v13_34_world_model_mutation(
        runtime_context=context(root, plan),
        v13_34_world_model_mutation_license=license_value,
    ).to_dict()


def assert_unchanged(root: pathlib.Path, original: dict[str, Any]) -> None:
    current = read_json(root / "physical_quantum_qi_world_model_state.json")
    assert current == original, (current, original)


def main() -> int:
    with tempfile.TemporaryDirectory() as directory:
        base = pathlib.Path(directory)

        root = base / "success"
        prepare_v13_33(root, "reinforce")
        original = initial_world_state(root)
        plan = mutation_plan(
            root,
            "mutation-success-001",
            [
                {"op": "set", "path": "/state/clinical/status", "value": "updated"},
                {"op": "increment", "path": "/state/network/harmony_score", "value": 0.2},
                {"op": "append", "path": "/state/events", "value": {"kind": "direct_world_update"}},
                {"op": "merge", "path": "/state/clinical", "value": {"confidence": 0.9}},
            ],
        )
        result = run(root, plan, license_packet(plan))
        assert result["status"] == "PHYSICAL_QUANTUM_QI_V13_34_WORLD_MODEL_MUTATION_READY", result
        assert result["mutation_status"] == "world_model_direct_mutation_applied"
        assert result["world_model_mutated"] is True
        assert result["rollback_snapshot_written"] is True
        assert result["mutation_ledger_appended"] is True
        assert result["operations_applied"] == 4
        updated = read_json(root / "physical_quantum_qi_world_model_state.json")
        assert updated["revision"] == 1
        assert updated["state"]["clinical"] == {"status": "updated", "confidence": 0.9}
        assert updated["state"]["network"]["harmony_score"] == 0.6000000000000001
        assert updated["state"]["events"] == [{"kind": "direct_world_update"}]
        assert updated["previous_world_model_digest"] == original["world_model_digest"]
        assert updated["world_model_digest"] == result["after_world_model_digest"]
        snapshot = read_json(root / "physical_quantum_qi_world_model_rollback_snapshot_mutation-success-001.json")
        assert snapshot["world_model_state"] == original
        ledger = latest_jsonl(root / "physical_quantum_qi_world_model_mutation_ledger.jsonl")
        assert ledger["before_world_model_digest"] == original["world_model_digest"]
        assert ledger["after_world_model_digest"] == updated["world_model_digest"]
        assert ledger["rollback_snapshot_digest"] == snapshot["rollback_snapshot_digest"]

        replay = run(root, plan, license_packet(plan))
        assert replay["status"].endswith("BLOCKED")
        assert "world_model_mutation_id_replay" in replay["blockers"]
        assert read_json(root / "physical_quantum_qi_world_model_state.json") == updated

        root = base / "digest_mismatch"
        prepare_v13_33(root, "reinforce")
        original = initial_world_state(root)
        plan = mutation_plan(
            root,
            "mutation-digest-mismatch",
            [{"op": "set", "path": "/state/clinical/status", "value": "should-not-apply"}],
            expected_digest="wrong-world-model-digest",
        )
        result = run(root, plan, license_packet(plan))
        assert result["status"].endswith("BLOCKED")
        assert "world_model_expected_digest_mismatch" in result["blockers"]
        assert_unchanged(root, original)

        root = base / "protected_path"
        prepare_v13_33(root, "reinforce")
        original = initial_world_state(root)
        plan = mutation_plan(
            root,
            "mutation-protected-path",
            [{"op": "set", "path": "/state/system/immutable_root", "value": False}],
        )
        result = run(root, plan, license_packet(plan))
        assert result["status"].endswith("BLOCKED")
        assert "world_model_mutation_protected_path" in result["blockers"]
        assert_unchanged(root, original)

        root = base / "invalid_operation_atomic"
        prepare_v13_33(root, "reinforce")
        original = initial_world_state(root)
        plan = mutation_plan(
            root,
            "mutation-invalid-operation",
            [{"op": "increment", "path": "/state/clinical/status", "value": 1}],
        )
        result = run(root, plan, license_packet(plan))
        assert result["status"].endswith("BLOCKED")
        assert "world_model_mutation_increment_target_not_number" in result["blockers"]
        assert result["rollback_snapshot_written"] is False
        assert_unchanged(root, original)

        root = base / "hold_intent"
        prepare_v13_33(root, "probe")
        original = initial_world_state(root)
        plan = mutation_plan(
            root,
            "mutation-hold-intent",
            [{"op": "set", "path": "/state/clinical/status", "value": "should-not-apply"}],
            source_intent_digest="",
        )
        result = run(root, plan, license_packet(plan))
        assert result["status"].endswith("BLOCKED")
        assert "v13_33_guarded_intent_not_ready_for_world_mutation" in result["blockers"]
        assert_unchanged(root, original)

        root = base / "license_block"
        prepare_v13_33(root, "reinforce")
        original = initial_world_state(root)
        plan = mutation_plan(
            root,
            "mutation-license-block",
            [{"op": "set", "path": "/state/clinical/status", "value": "should-not-apply"}],
        )
        result = run(root, plan, license_packet(plan, direct_world_model_mutation_allowed=False))
        assert result["status"].endswith("BLOCKED")
        assert "direct_world_model_mutation_not_allowed" in result["blockers"]
        assert_unchanged(root, original)

        root = base / "unbound_plan"
        prepare_v13_33(root, "reinforce")
        original = initial_world_state(root)
        plan = mutation_plan(
            root,
            "mutation-unbound-plan",
            [{"op": "delete", "path": "/state/clinical/confidence"}],
        )
        result = run(root, plan, license_packet(plan, bound_mutation_plan_digest="different-plan-digest"))
        assert result["status"].endswith("BLOCKED")
        assert "world_model_mutation_plan_not_bound_to_license" in result["blockers"]
        assert_unchanged(root, original)

    print("physical_quantum_qi_v13_34_world_model_mutation checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
