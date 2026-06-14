#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import sys
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_indra_qi_post_assimilation_reentry_core_v0_7 import (
    reentry_plan_digest,
    sha,
    valid_digest,
    without,
)
from runtime.kuuos_indra_qi_world_assimilation_core_v0_6 import (
    dynamic_world_state_digest,
)
from runtime.kuuos_runtime_daemon_indra_qi_post_assimilation_reentry_v0_7 import (
    build_indra_qi_post_assimilation_causal_reentry_v0_7,
)
from runtime.kuuos_runtime_daemon_indra_qi_world_model_v0_1 import (
    compute_indra_qi_world_state_digest,
)
from scripts.check_indra_qi_process_tensor_world_assimilation_v0_6 import (
    build_plan as assimilation_plan,
    prepare_cycle,
    read_json,
    records,
    run_assimilation,
    write_json,
)

EXAMPLE = ROOT / "examples" / "indra_qi_world_reentry_plan_v0_7.json"


def latest(path: pathlib.Path) -> dict[str, Any]:
    values = records(path)
    return values[-1] if values else {}


def prepare_assimilated(
    root: pathlib.Path, suffix: str
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    world, cycle, seed = prepare_cycle(root, f"reentry-{suffix}")
    plan = assimilation_plan(world, cycle, seed, suffix=f"reentry-{suffix}")
    result = run_assimilation(root, plan)
    assert result["status"] == "INDRA_QI_PROCESS_TENSOR_WORLD_ASSIMILATION_V0_6_READY", result
    assimilated = read_json(root / "ku_indra_qi_noncommutative_mandala_world_state.json")
    record = read_json(root / "indra_qi_process_tensor_world_assimilation_record_v0_6.json")
    post_seed = read_json(root / "indra_qi_post_assimilation_projection_seed_v0_6.json")
    assert compute_indra_qi_world_state_digest(assimilated) == assimilated[
        "indra_qi_world_state_digest"
    ]
    assert dynamic_world_state_digest(assimilated) == assimilated[
        "process_tensor_dynamic_world_state_digest"
    ]
    assert valid_digest(record, "assimilation_record_digest")
    assert valid_digest(post_seed, "post_assimilation_seed_packet_digest")
    return assimilated, record, post_seed


def build_plan(
    world: dict[str, Any],
    record: dict[str, Any],
    seed: dict[str, Any],
    *,
    suffix: str,
) -> dict[str, Any]:
    plan = json.loads(EXAMPLE.read_text(encoding="utf-8"))
    plan.update(
        {
            "reentry_id": f"indra-qi-world-reentry-{suffix}",
            "source_assimilation_id": record["assimilation_id"],
            "source_assimilation_record_digest": record["assimilation_record_digest"],
            "source_post_assimilation_seed_packet_digest": seed[
                "post_assimilation_seed_packet_digest"
            ],
            "source_world_state_digest": world["indra_qi_world_state_digest"],
            "projection_id": f"indra-qi-reentry-projection-{suffix}",
            "causal_world_id": f"indra-qi-reentry-causal-world-{suffix}",
            "transaction_id": f"indra-qi-reentry-init-{suffix}",
        }
    )
    plan["reentry_plan_digest"] = reentry_plan_digest(plan)
    return plan


def v14_template(**overrides: Any) -> dict[str, Any]:
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
        "allowed_variables": [],
        "protected_variables": [],
        "max_variables": 16,
        "max_mechanisms": 16,
    }
    value.update(overrides)
    return value


def projection_template(**overrides: Any) -> dict[str, Any]:
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
        "v14_initialize_license_template": v14_template(),
    }
    value.update(overrides)
    return value


def reentry_license(plan: dict[str, Any], **overrides: Any) -> dict[str, Any]:
    value = {
        "license_status": "INDRA_QI_POST_ASSIMILATION_CAUSAL_REENTRY_V0_7_LICENSE_READY",
        "bound_reentry_plan_digest": plan["reentry_plan_digest"],
        "world_state_read_allowed": True,
        "assimilation_record_read_allowed": True,
        "post_assimilation_seed_read_allowed": True,
        "assimilation_ledger_read_allowed": True,
        "reentry_plan_validate_allowed": True,
        "child_runtime_create_allowed": True,
        "child_world_state_copy_allowed": True,
        "generated_projection_plan_write_allowed": True,
        "v0_2_projection_invoke_allowed": True,
        "reentry_record_write_allowed": True,
        "reentry_ledger_append_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
        "v0_2_projection_license_template": projection_template(),
    }
    value.update(overrides)
    return value


def run_reentry(
    root: pathlib.Path,
    plan: dict[str, Any],
    license_value: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return build_indra_qi_post_assimilation_causal_reentry_v0_7(
        runtime_context={
            "runtime_root": str(root),
            "indra_qi_post_assimilation_causal_reentry_v0_7_enabled": True,
            "invoke_indra_qi_post_assimilation_causal_reentry_v0_7": True,
        },
        reentry_plan=plan,
        reentry_license=license_value or reentry_license(plan),
    ).to_dict()


def rewrite_seed_chain(
    root: pathlib.Path,
    seed: dict[str, Any],
    record: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    seed["post_assimilation_seed_packet_digest"] = sha(
        without(seed, "post_assimilation_seed_packet_digest")
    )
    write_json(root / "indra_qi_post_assimilation_projection_seed_v0_6.json", seed)
    record["post_assimilation_seed_packet_digest"] = seed[
        "post_assimilation_seed_packet_digest"
    ]
    record["assimilation_record_digest"] = sha(
        without(record, "assimilation_record_digest")
    )
    write_json(
        root / "indra_qi_process_tensor_world_assimilation_record_v0_6.json",
        record,
    )
    ledger_path = root / "indra_qi_process_tensor_world_assimilation_ledger_v0_6.jsonl"
    values = records(ledger_path)
    ledger = values[-1]
    ledger["post_assimilation_seed_packet_digest"] = seed[
        "post_assimilation_seed_packet_digest"
    ]
    ledger["source_assimilation_record_digest"] = record[
        "assimilation_record_digest"
    ]
    ledger["record_digest"] = sha(without(ledger, "record_digest"))
    ledger_path.write_text(
        "\n".join(
            json.dumps(value, ensure_ascii=False, sort_keys=True)
            for value in values[:-1] + [ledger]
        )
        + "\n",
        encoding="utf-8",
    )
    return seed, record


def assert_parent_unchanged(root: pathlib.Path, digest: str) -> None:
    state = read_json(root / "ku_indra_qi_noncommutative_mandala_world_state.json")
    assert state["indra_qi_world_state_digest"] == digest
    assert compute_indra_qi_world_state_digest(state) == digest
