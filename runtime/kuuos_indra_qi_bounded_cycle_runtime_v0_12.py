#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import pathlib
import shutil
import time
from typing import Any, Mapping

from runtime.kuuos_causal_world_model_core_v14_0 import valid_digest as valid_v14_digest
from runtime.kuuos_indra_qi_bounded_cycle_child_stage_v0_12 import run_child_stages
from runtime.kuuos_indra_qi_bounded_cycle_core_v0_12 import (
    REQUIRED_BOUNDARY,
    STATE_VERSION,
    mapping,
    runner_state_digest,
    sha,
    valid_digest,
    validate_plan,
)
from runtime.kuuos_indra_qi_bounded_cycle_plans_v0_12 import (
    convergence_reached,
    dynamic_metrics,
)
from runtime.kuuos_indra_qi_bounded_cycle_runtime_support_v0_12 import (
    append_jsonl,
    latest_matching,
    read_json,
    records,
    restore_root_files,
    restore_tree,
    safe_id,
    snapshot_root_files,
    snapshot_tree,
    validate_license_templates,
    validate_runner_state,
    validate_source_v0_11,
    write_json,
)
from runtime.kuuos_indra_qi_bounded_cycle_tail_v0_12 import build_tail
from runtime.kuuos_indra_qi_bounded_cycle_v0_10_stage_v0_12 import run_v0_10_stage
from runtime.kuuos_indra_qi_world_assimilation_core_v0_6 import dynamic_world_state_digest
from runtime.kuuos_runtime_daemon_indra_qi_world_model_v0_1 import (
    compute_indra_qi_world_state_digest,
)

VERSION = "indra_qi_bounded_generational_cycle_v0_12"
READY = "INDRA_QI_BOUNDED_GENERATIONAL_CYCLE_V0_12_READY"
BLOCKED = "INDRA_QI_BOUNDED_GENERATIONAL_CYCLE_V0_12_BLOCKED"


@dataclass(frozen=True)
class IndraQiBoundedCycleV0_12Result:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    runner_id: str
    generation_run_id: str
    generation_index: int
    completed_generations: int
    max_generations: int
    runner_status: str
    stop_reason: str
    selected_candidate_id: str
    v0_8_ready: bool
    v0_9_ready: bool
    v0_10_ready: bool
    v0_11_ready: bool
    transaction_committed: bool
    transaction_rolled_back: bool
    before_world_state_digest: str
    after_world_state_digest: str
    source_child_runtime_root: str
    target_child_runtime_root: str
    source_v0_11_handoff_digest: str
    target_v0_11_handoff_digest: str
    runner_state_digest: str
    blockers: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _target_artifacts(
    root: pathlib.Path,
    run_id: str,
    child_root: str,
    blockers: list[str],
) -> dict[str, Any]:
    handoff = read_json(
        root / "indra_qi_parent_cycle_assimilation_reentry_handoff_v0_11.json"
    )
    record = read_json(
        root / "indra_qi_parent_cycle_assimilation_reentry_record_v0_11.json"
    )
    ledger = latest_matching(
        records(root / "indra_qi_parent_cycle_assimilation_reentry_ledger_v0_11.jsonl"),
        "loop_id",
        run_id,
    )
    reentry = read_json(root / "indra_qi_post_assimilation_causal_reentry_record_v0_7.json")
    world = read_json(root / "ku_indra_qi_noncommutative_mandala_world_state.json")
    child = pathlib.Path(child_root).expanduser().resolve()
    causal = read_json(child / "kuuos_causal_world_model_state_v14_0.json")
    checks = (
        (valid_digest(handoff, "loop_handoff_packet_digest"), "bounded_cycle_target_handoff_digest_invalid"),
        (valid_digest(record, "loop_record_digest"), "bounded_cycle_target_record_digest_invalid"),
        (valid_digest(ledger, "record_digest"), "bounded_cycle_target_ledger_digest_invalid"),
        (valid_digest(reentry, "reentry_record_digest"), "bounded_cycle_target_reentry_digest_invalid"),
        (valid_v14_digest(causal, "world_model_digest"), "bounded_cycle_target_v14_digest_invalid"),
    )
    for condition, blocker in checks:
        if not condition:
            blockers.append(blocker)
    world_digest = str(world.get("indra_qi_world_state_digest", ""))
    dynamic_digest = str(world.get("process_tensor_dynamic_world_state_digest", ""))
    if compute_indra_qi_world_state_digest(world) != world_digest:
        blockers.append("bounded_cycle_target_world_digest_invalid")
    if dynamic_world_state_digest(world) != dynamic_digest:
        blockers.append("bounded_cycle_target_dynamic_digest_invalid")
    if str(handoff.get("reentry_record_digest", "")) != str(
        reentry.get("reentry_record_digest", "")
    ):
        blockers.append("bounded_cycle_target_handoff_reentry_mismatch")
    if str(reentry.get("v14_world_model_digest", "")) != str(
        causal.get("world_model_digest", "")
    ):
        blockers.append("bounded_cycle_target_reentry_v14_mismatch")
    return {
        "handoff": handoff,
        "record": record,
        "ledger": ledger,
        "reentry": reentry,
        "world": world,
        "causal": causal,
        "world_digest": world_digest,
        "dynamic_digest": dynamic_digest,
        "handoff_digest": str(handoff.get("loop_handoff_packet_digest", "")),
        "reentry_digest": str(reentry.get("reentry_record_digest", "")),
        "v14_digest": str(causal.get("world_model_digest", "")),
        "metrics": dynamic_metrics(world),
    }


def _write_success(
    *,
    root: pathlib.Path,
    plan: Mapping[str, Any],
    source: Mapping[str, Any],
    child_output: Mapping[str, Any],
    v10_output: Mapping[str, Any],
    target: Mapping[str, Any],
    previous_state: Mapping[str, Any],
    prior_ledger: list[dict[str, Any]],
    source_child: pathlib.Path,
    target_child: str,
    stop_reason: str,
) -> str:
    runner_id = str(plan.get("runner_id", ""))
    run_id = str(plan.get("generation_run_id", ""))
    generation = int(plan.get("generation_index", 0) or 0)
    completed = generation + 1
    maximum = int(plan.get("max_generations", 0) or 0)
    status = "bounded_cycle_stopped" if stop_reason else "bounded_cycle_ready_for_next_generation"
    source_handoff = mapping(source.get("handoff"))
    handoff = {
        "version": "indra_qi_bounded_cycle_handoff_packet_v0_12",
        "runner_id": runner_id,
        "generation_run_id": run_id,
        "generation_index": generation,
        "completed_generations": completed,
        "max_generations": maximum,
        "runner_status": status,
        "stop_reason": stop_reason,
        "source_v0_11_loop_id": str(source_handoff.get("loop_id", "")),
        "source_v0_11_handoff_packet_digest": str(
            source_handoff.get("loop_handoff_packet_digest", "")
        ),
        "selected_action_kind": str(plan.get("selected_action_kind", "")),
        "selected_candidate_id": str(child_output.get("selected_candidate_id", "")),
        "action_envelope_digest": str(child_output.get("action_envelope_digest", "")),
        "execution_record_digest": str(child_output.get("execution_record_digest", "")),
        "feedback_packet_digest": str(child_output.get("feedback_packet_digest", "")),
        "process_tensor_cycle_state_digest": str(
            v10_output.get("process_tensor_cycle_state_digest", "")
        ),
        "target_v0_11_handoff_packet_digest": str(target.get("handoff_digest", "")),
        "target_reentry_record_digest": str(target.get("reentry_digest", "")),
        "target_v14_world_model_digest": str(target.get("v14_digest", "")),
        "before_parent_world_state_digest": str(
            mapping(source.get("world")).get("indra_qi_world_state_digest", "")
        ),
        "after_parent_world_state_digest": str(target.get("world_digest", "")),
        "before_dynamic_world_state_digest": str(
            mapping(source.get("world")).get("process_tensor_dynamic_world_state_digest", "")
        ),
        "after_dynamic_world_state_digest": str(target.get("dynamic_digest", "")),
        "source_child_runtime_root": str(source_child),
        "target_child_runtime_root": target_child,
        "dynamic_metrics": dict(mapping(target.get("metrics"))),
        "boundary": {
            **REQUIRED_BOUNDARY,
            "v0_8_completed": True,
            "v0_9_completed": True,
            "v0_10_completed": True,
            "v0_11_completed": True,
            "generation_transaction_committed": True,
        },
        "epoch": int(time.time()),
    }
    handoff["generation_handoff_digest"] = sha(handoff)
    write_json(root / "indra_qi_bounded_cycle_handoff_v0_12.json", handoff)
    record = {
        "version": "indra_qi_bounded_cycle_record_v0_12",
        "runner_id": runner_id,
        "generation_run_id": run_id,
        "generation_index": generation,
        "source_v0_11_handoff_packet_digest": handoff[
            "source_v0_11_handoff_packet_digest"
        ],
        "source_generation_handoff_digest": handoff["generation_handoff_digest"],
        "target_v0_11_handoff_packet_digest": handoff[
            "target_v0_11_handoff_packet_digest"
        ],
        "runner_status": status,
        "stop_reason": stop_reason,
        "boundary": {
            "append_only_generation_record": True,
            "generation_index_monotone": True,
            "non_markov_feedback_preserved": True,
        },
        "epoch": int(time.time()),
    }
    record["generation_record_digest"] = sha(record)
    write_json(root / "indra_qi_bounded_cycle_record_v0_12.json", record)
    ledger = {
        "version": "indra_qi_bounded_cycle_ledger_record_v0_12",
        "record_type": "bounded_generational_cycle",
        "runner_id": runner_id,
        "generation_run_id": run_id,
        "generation_index": generation,
        "source_v0_11_handoff_packet_digest": handoff[
            "source_v0_11_handoff_packet_digest"
        ],
        "source_generation_handoff_digest": handoff["generation_handoff_digest"],
        "source_generation_record_digest": record["generation_record_digest"],
        "target_v0_11_handoff_packet_digest": handoff[
            "target_v0_11_handoff_packet_digest"
        ],
        "target_reentry_record_digest": handoff["target_reentry_record_digest"],
        "target_v14_world_model_digest": handoff["target_v14_world_model_digest"],
        "runner_status": status,
        "stop_reason": stop_reason,
        "prev_record_digest": str(prior_ledger[-1].get("record_digest", "GENESIS"))
        if prior_ledger
        else "GENESIS",
        "boundary": {
            "append_only_generation_lineage": True,
            "source_v0_11_handoff_consumed_once": True,
            "one_generation_committed": True,
            "non_markov_feedback_preserved": True,
        },
        "epoch": int(time.time()),
    }
    ledger["record_digest"] = sha(ledger)
    append_jsonl(root / "indra_qi_bounded_cycle_ledger_v0_12.jsonl", ledger)
    state = {
        "version": STATE_VERSION,
        "runner_id": runner_id,
        "runner_status": status,
        "stop_reason": stop_reason,
        "completed_generations": completed,
        "max_generations": maximum,
        "last_generation_run_id": run_id,
        "last_generation_record_digest": record["generation_record_digest"],
        "latest_v0_11_handoff_packet_digest": handoff[
            "target_v0_11_handoff_packet_digest"
        ],
        "latest_reentry_id": str(mapping(target.get("reentry")).get("reentry_id", "")),
        "latest_reentry_record_digest": handoff["target_reentry_record_digest"],
        "latest_parent_world_state_digest": handoff[
            "after_parent_world_state_digest"
        ],
        "latest_dynamic_world_state_digest": handoff[
            "after_dynamic_world_state_digest"
        ],
        "latest_child_runtime_root": target_child,
        "latest_v14_world_model_digest": handoff["target_v14_world_model_digest"],
        "dynamic_metrics": handoff["dynamic_metrics"],
        "prev_runner_state_digest": str(
            previous_state.get("runner_state_digest", "GENESIS")
        )
        if previous_state
        else "GENESIS",
        "boundary": {
            "bounded_generation_state_only": True,
            "not_truth_authority": True,
            "not_external_world_actuation_authority": True,
            "non_markov_feedback_preserved": True,
            "candidate_weighting_not_truth": True,
        },
        "epoch": int(time.time()),
    }
    state["runner_state_digest"] = runner_state_digest(state)
    write_json(root / "indra_qi_bounded_cycle_state_v0_12.json", state)
    return str(state["runner_state_digest"])


def build_cycle(
    *,
    runtime_context: Mapping[str, Any],
    cycle_plan: Mapping[str, Any],
    cycle_license: Mapping[str, Any],
) -> IndraQiBoundedCycleV0_12Result:
    context = mapping(runtime_context)
    plan = dict(mapping(cycle_plan))
    license_value = mapping(cycle_license)
    blockers: list[str] = []
    root_value = context.get("runtime_root")
    root = pathlib.Path(str(root_value)).expanduser().resolve() if root_value else pathlib.Path(".").resolve()
    if not root_value:
        blockers.append("runtime_root_missing")
    if root == pathlib.Path("/").resolve():
        blockers.append("runtime_root_forbidden")
    if context.get("indra_qi_bounded_generational_cycle_v0_12_enabled") is not True:
        blockers.append("bounded_cycle_enabled_not_true")
    if context.get("apply_indra_qi_bounded_generation_v0_12") is not True:
        blockers.append("bounded_cycle_apply_not_true")
    validate_plan(plan, blockers)
    source = validate_source_v0_11(root, plan, blockers)
    source_handoff_digest = str(
        mapping(source.get("handoff")).get("loop_handoff_packet_digest", "")
    )
    previous_state, prior_ledger = validate_runner_state(
        root, plan, source_handoff_digest, blockers
    )
    validate_license_templates(
        license_value, plan, mapping(source.get("causal")), blockers
    )
    runner_id = str(plan.get("runner_id", ""))
    run_id = str(plan.get("generation_run_id", ""))
    generation = int(plan.get("generation_index", 0) or 0)
    maximum = int(plan.get("max_generations", 0) or 0)
    source_world = mapping(source.get("world"))
    before_world = str(source_world.get("indra_qi_world_state_digest", ""))
    source_child = source.get("child")
    if not isinstance(source_child, pathlib.Path):
        source_child = root
    target_child = (
        root
        / "indra_qi_causal_reentry_cycles_v0_7"
        / safe_id(str(plan.get("reentry_id", "")))
    ).resolve()
    if target_child.exists():
        blockers.append("bounded_cycle_target_child_already_exists")
    if target_child == source_child.resolve():
        blockers.append("bounded_cycle_target_child_equals_source_child")

    root_snapshot: dict[str, bytes] = {}
    child_snapshot: dict[str, bytes] = {}
    if not blockers:
        root_snapshot = snapshot_root_files(root)
        child_snapshot = snapshot_tree(source_child)
    child_output = run_child_stages(
        root=root,
        plan=plan,
        license_value=license_value,
        world=source_world,
        reentry=mapping(source.get("reentry")),
        causal=mapping(source.get("causal")),
        child=source_child,
        blockers=blockers,
    )
    v10_output = run_v0_10_stage(
        root=root,
        plan=plan,
        license_value=license_value,
        source_reentry=mapping(source.get("reentry")),
        child_output=child_output,
        blockers=blockers,
    )
    tail_output = build_tail(
        root=root,
        plan=plan,
        license_value=license_value,
        source=v10_output,
        blockers=blockers,
    )
    target_child_root = str(tail_output.get("target_child_runtime_root", target_child))
    target: dict[str, Any] = {}
    if bool(tail_output.get("ready")) and not blockers:
        target = _target_artifacts(root, run_id, target_child_root, blockers)

    rolled_back = False
    if blockers and root_snapshot:
        restore_root_files(root, root_snapshot)
        restore_tree(source_child, child_snapshot)
        if target_child.exists() and target_child != source_child.resolve():
            shutil.rmtree(target_child)
        rolled_back = True
        target_child_root = str(target_child)
        target = {}

    committed = not blockers and bool(tail_output.get("ready"))
    completed = generation + 1 if committed else generation
    stop_reason = ""
    state_digest = str(previous_state.get("runner_state_digest", ""))
    runner_status = "bounded_cycle_blocked"
    after_world = before_world
    target_handoff_digest = ""
    if committed:
        if completed >= maximum:
            stop_reason = "maximum_generations_reached"
        elif convergence_reached(
            mapping(target.get("metrics")), mapping(plan.get("convergence_policy"))
        ):
            stop_reason = "dynamic_world_convergence_reached"
        runner_status = (
            "bounded_cycle_stopped"
            if stop_reason
            else "bounded_cycle_ready_for_next_generation"
        )
        after_world = str(target.get("world_digest", ""))
        target_handoff_digest = str(target.get("handoff_digest", ""))
        state_digest = _write_success(
            root=root,
            plan=plan,
            source=source,
            child_output=child_output,
            v10_output=v10_output,
            target=target,
            previous_state=previous_state,
            prior_ledger=prior_ledger,
            source_child=source_child,
            target_child=target_child_root,
            stop_reason=stop_reason,
        )
    status = READY if committed else BLOCKED
    receipt = {
        "version": VERSION,
        "status": status,
        "runner_id": runner_id,
        "generation_run_id": run_id,
        "generation_index": generation,
        "completed_generations": completed,
        "max_generations": maximum,
        "runner_status": runner_status,
        "stop_reason": stop_reason,
        "transaction_committed": committed,
        "transaction_rolled_back": rolled_back,
        "source_v0_11_handoff_packet_digest": source_handoff_digest,
        "target_v0_11_handoff_packet_digest": target_handoff_digest,
        "before_parent_world_state_digest": before_world,
        "after_parent_world_state_digest": after_world,
        "source_child_runtime_root": str(source_child),
        "target_child_runtime_root": target_child_root,
        "runner_state_digest": state_digest,
        "v0_8_ready": bool(child_output.get("v0_8_ready")),
        "v0_9_ready": bool(child_output.get("v0_9_ready")),
        "v0_10_ready": bool(v10_output.get("v0_10_ready")),
        "v0_11_ready": bool(tail_output.get("ready")),
        "blockers": blockers,
        "boundary": {
            **REQUIRED_BOUNDARY,
            "generation_committed": committed,
            "rollback_completed_on_failure": rolled_back,
        },
        "epoch": int(time.time()),
    }
    receipt["packet_id"] = "indra-qi-bounded-cycle-" + sha(receipt)[:16]
    if license_value.get("receipt_write_allowed") is True:
        write_json(root / "indra_qi_bounded_cycle_receipt_v0_12.json", receipt)
    if license_value.get("audit_append_allowed") is True:
        append_jsonl(
            root / "indra_qi_bounded_cycle_audit_v0_12.jsonl",
            {**receipt, "audit_record_digest": sha(receipt)},
        )
    return IndraQiBoundedCycleV0_12Result(
        VERSION,
        status,
        receipt["packet_id"],
        str(root),
        runner_id,
        run_id,
        generation,
        completed,
        maximum,
        runner_status,
        stop_reason,
        str(child_output.get("selected_candidate_id", "")),
        bool(child_output.get("v0_8_ready")),
        bool(child_output.get("v0_9_ready")),
        bool(v10_output.get("v0_10_ready")),
        bool(tail_output.get("ready")),
        committed,
        rolled_back,
        before_world,
        after_world,
        str(source_child),
        target_child_root,
        source_handoff_digest,
        target_handoff_digest,
        state_digest,
        blockers,
    )
