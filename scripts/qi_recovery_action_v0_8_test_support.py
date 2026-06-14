#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import sys
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_indra_qi_recovery_action_core_v0_8 import (
    ALLOWED_ACTION_KINDS,
    action_plan_digest,
    valid_digest,
)
from runtime.kuuos_runtime_daemon_qi_recoverability_action_envelope_v0_8 import (
    build_indra_qi_recoverability_action_envelope_v0_8,
)
from scripts.check_indra_qi_process_tensor_world_assimilation_v0_6 import (
    read_json,
    records,
)
from scripts.world_reentry_v0_7_test_support import (
    build_plan as reentry_plan,
    prepare_assimilated,
    run_reentry,
)

EXAMPLE = ROOT / "examples" / "indra_qi_recoverability_action_envelope_plan_v0_8.json"


def latest(path: pathlib.Path) -> dict[str, Any]:
    values = records(path)
    return values[-1] if values else {}


def prepare_reentry(
    root: pathlib.Path,
    suffix: str,
) -> tuple[
    dict[str, Any],
    dict[str, Any],
    dict[str, Any],
    pathlib.Path,
    dict[str, Any],
    dict[str, Any],
]:
    world, assimilation, seed = prepare_assimilated(root, f"action-{suffix}")
    plan = reentry_plan(world, assimilation, seed, suffix=f"action-{suffix}")
    result = run_reentry(root, plan)
    assert result["status"] == "INDRA_QI_POST_ASSIMILATION_CAUSAL_REENTRY_V0_7_READY", result
    reentry = read_json(root / "indra_qi_post_assimilation_causal_reentry_record_v0_7.json")
    assert valid_digest(reentry, "reentry_record_digest")
    child = pathlib.Path(reentry["child_runtime_root"])
    generated = read_json(child / "indra_qi_generated_causal_projection_plan_v0_7.json")
    causal = read_json(child / "kuuos_causal_world_model_state_v14_0.json")
    return world, assimilation, reentry, child, generated, causal


def build_plan(
    world: dict[str, Any],
    reentry: dict[str, Any],
    *,
    suffix: str,
) -> dict[str, Any]:
    plan = json.loads(EXAMPLE.read_text(encoding="utf-8"))
    plan.update(
        {
            "action_envelope_id": f"indra-qi-recovery-action-{suffix}",
            "source_reentry_id": reentry["reentry_id"],
            "source_reentry_record_digest": reentry["reentry_record_digest"],
            "source_world_state_digest": world["indra_qi_world_state_digest"],
            "source_dynamic_world_state_digest": world[
                "process_tensor_dynamic_world_state_digest"
            ],
            "source_v14_world_model_digest": reentry["v14_world_model_digest"],
        }
    )
    plan["action_plan_digest"] = action_plan_digest(plan)
    return plan


def action_license(plan: dict[str, Any], **overrides: Any) -> dict[str, Any]:
    value = {
        "license_status": "INDRA_QI_RECOVERABILITY_ACTION_ENVELOPE_V0_8_LICENSE_READY",
        "bound_action_plan_digest": plan["action_plan_digest"],
        "world_state_read_allowed": True,
        "assimilation_record_read_allowed": True,
        "post_assimilation_seed_read_allowed": True,
        "assimilation_ledger_read_allowed": True,
        "reentry_record_read_allowed": True,
        "reentry_ledger_read_allowed": True,
        "child_runtime_read_allowed": True,
        "action_plan_validate_allowed": True,
        "action_envelope_write_allowed": True,
        "activation_record_write_allowed": True,
        "action_ledger_append_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
        "allowed_action_kinds": sorted(ALLOWED_ACTION_KINDS),
    }
    value.update(overrides)
    return value


def run_action(
    root: pathlib.Path,
    plan: dict[str, Any],
    license_value: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return build_indra_qi_recoverability_action_envelope_v0_8(
        runtime_context={
            "runtime_root": str(root),
            "indra_qi_recoverability_action_envelope_v0_8_enabled": True,
            "build_indra_qi_recoverability_action_envelope_v0_8": True,
        },
        action_plan=plan,
        action_license=license_value or action_license(plan),
    ).to_dict()
