from __future__ import annotations

import json
import tempfile
from copy import deepcopy
from pathlib import Path

from runtime.kuuos_belief_os_types_v0_1 import sha
from runtime.kuuos_plan_os_closed_loop_fixture_v0_4 import (
    closed_loop_learning_source,
)
from runtime.kuuos_plan_os_closed_loop_intake_kernel_v0_4 import (
    build_bound_replan_state,
    build_closed_loop_bind_receipt,
    build_closed_loop_intake_receipt,
)
from runtime.kuuos_plan_os_closed_loop_intake_store_v0_4 import (
    ClosedLoopIntakeStore,
    ClosedLoopIntakeStoreError,
    build_initial_closed_loop_intake_store_state,
)
from runtime.kuuos_plan_os_closed_loop_intake_types_v0_4 import (
    STAGE_BIND,
    STAGE_INTAKE,
    intake_receipt_digest,
)


def _build_intake(
    plan: dict,
    compiler: dict,
    learn_state: dict,
    learn_handoff: dict,
    learn_completion: dict,
    *,
    cycle: int,
    now_ms: int,
) -> dict:
    return build_closed_loop_intake_receipt(
        current_plan_state=plan,
        next_cycle_compiler_receipt=compiler,
        committed_learn_state=learn_state,
        learn_lineage_handoff_receipt=learn_handoff,
        learn_lineage_completion_receipt=learn_completion,
        current_cycle_index=cycle,
        plan_budget=2.0,
        maximum_candidate_risk=0.5,
        base_switch_threshold=0.1,
        mission_cycle_state_digest=sha({"closed-loop-cycle": cycle}),
        replan_phase_event_digest=sha({"closed-loop-event": cycle}),
        now_ms=now_ms,
    )


def _negative_cases(
    plan: dict,
    compiler: dict,
    learn_state: dict,
    learn_handoff: dict,
    learn_completion: dict,
) -> None:
    cycle = compiler["mission_cycle_cycle_index"]
    try:
        _build_intake(
            plan,
            compiler,
            learn_state,
            learn_handoff,
            learn_completion,
            cycle=cycle + 1,
            now_ms=550_001,
        )
    except ValueError as exc:
        assert str(exc) == "closed_loop_cycle_mismatch"
    else:
        raise AssertionError("wrong closed-loop cycle accepted")

    substituted = deepcopy(compiler)
    substituted["compiled_plan_state_digest"] = sha("substituted-plan")
    try:
        _build_intake(
            plan,
            substituted,
            learn_state,
            learn_handoff,
            learn_completion,
            cycle=cycle,
            now_ms=550_002,
        )
    except ValueError as exc:
        assert str(exc) == "closed_loop_compiler_receipt_digest_invalid"
    else:
        raise AssertionError("substituted compiler receipt accepted")

    substituted_completion = deepcopy(learn_completion)
    substituted_completion["planos_replan_input_digest"] = sha(
        "substituted-replan-input"
    )
    try:
        _build_intake(
            plan,
            compiler,
            learn_state,
            learn_handoff,
            substituted_completion,
            cycle=cycle,
            now_ms=550_003,
        )
    except ValueError as exc:
        assert str(exc).startswith("closed_loop_learn_completion_invalid:")
    else:
        raise AssertionError("substituted Learn completion accepted")


def run_kernel() -> dict:
    with tempfile.TemporaryDirectory(prefix="kuuos-plan-os-v04-") as temporary:
        root = Path(temporary)
        plan, compiler, learn_state, learn_handoff, learn_completion = (
            closed_loop_learning_source(root / "source")
        )
        _negative_cases(
            plan, compiler, learn_state, learn_handoff, learn_completion
        )
        cycle = compiler["mission_cycle_cycle_index"]
        intake = _build_intake(
            plan,
            compiler,
            learn_state,
            learn_handoff,
            learn_completion,
            cycle=cycle,
            now_ms=550_000,
        )
        assert intake["current_plan_state_digest"] == plan["plan_state_digest"]
        assert intake["committed_learn_state_digest"] == learn_state[
            "learn_state_digest"
        ]
        assert intake["planos_replan_input_digest"] == learn_completion[
            "planos_replan_input_digest"
        ]
        assert intake["active_from_cycle"] == cycle + 1
        assert intake["future_only"] is True
        assert intake["active_now"] is False

        store = ClosedLoopIntakeStore(root / "intake-store")
        store.initialize(
            build_initial_closed_loop_intake_store_state(
                store_id="plan-v04-intake-store", now_ms=549_900
            )
        )
        assert store.commit(
            stage=STAGE_INTAKE, receipt=intake, now_ms=550_010
        )["status"] == "COMMITTED"
        before_intake_replay = store.ledger_commit_count()
        assert store.commit(
            stage=STAGE_INTAKE, receipt=intake, now_ms=550_011
        )["status"] == "REPLAYED"
        assert store.ledger_commit_count() == before_intake_replay

        conflicting = deepcopy(intake)
        conflicting["mission_cycle_state_digest"] = sha("conflicting-intake")
        conflicting["closed_loop_intake_receipt_digest"] = ""
        conflicting["closed_loop_intake_receipt_digest"] = intake_receipt_digest(
            conflicting
        )
        try:
            store.commit(
                stage=STAGE_INTAKE, receipt=conflicting, now_ms=550_012
            )
        except ClosedLoopIntakeStoreError as exc:
            assert str(exc) == "closed_loop_intake_already_committed"
        else:
            raise AssertionError("conflicting closed-loop intake accepted")

        replan_state = build_bound_replan_state(
            intake_receipt=intake,
            replan_id="plan-v04-second-generation-replan",
            current_plan_state=plan,
            committed_learn_state=learn_state,
            now_ms=560_000,
        )
        assert replan_state["current_phase"] == "bind"
        assert replan_state["event_index"] == 0
        assert replan_state["current_cycle_index"] == cycle
        assert replan_state["active_from_cycle"] == cycle + 1
        assert replan_state["active_now"] is False

        bind_receipt = build_closed_loop_bind_receipt(
            intake_receipt=intake,
            bound_replan_state=replan_state,
            now_ms=560_010,
        )
        assert bind_receipt["next_phase"] == "history"
        assert bind_receipt["history_phase_required"] is True
        assert bind_receipt["replan_active_now"] is False
        assert bind_receipt["plan_active_now"] is False
        assert bind_receipt["execution_permission"] is False

        assert store.commit(
            stage=STAGE_BIND, receipt=bind_receipt, now_ms=560_011
        )["status"] == "COMMITTED"
        before_bind_replay = store.ledger_commit_count()
        assert store.commit(
            stage=STAGE_BIND, receipt=bind_receipt, now_ms=560_012
        )["status"] == "REPLAYED"
        assert store.ledger_commit_count() == before_bind_replay

        snapshot = root / "intake-store" / "closed-loop-intake-snapshot.json"
        snapshot.write_text(json.dumps({"corrupt": True}), encoding="utf-8")
        try:
            store.recover(require_snapshot_match=True)
        except ClosedLoopIntakeStoreError as exc:
            assert str(exc) == "closed_loop_snapshot_ledger_mismatch"
        else:
            raise AssertionError("corrupt closed-loop snapshot accepted")
        repaired = store.repair_snapshot()
        recovered = store.recover(require_snapshot_match=True)
        assert repaired["closed_loop_intake_store_state_digest"] == recovered[
            "closed_loop_intake_store_state_digest"
        ]

        return {
            "status": "PLAN_OS_CLOSED_LOOP_REPLAN_INTAKE_ADAPTER_V0_4_OK",
            "intake_receipt_digest": intake[
                "closed_loop_intake_receipt_digest"
            ],
            "bind_receipt_digest": bind_receipt[
                "closed_loop_bind_receipt_digest"
            ],
            "planos_replan_input_digest": intake[
                "planos_replan_input_digest"
            ],
            "current_cycle_index": cycle,
            "active_from_cycle": cycle + 1,
            "bound_replan_phase": replan_state["current_phase"],
            "next_phase": bind_receipt["next_phase"],
            "history_phase_required": bind_receipt[
                "history_phase_required"
            ],
            "future_only": intake["future_only"],
            "ledger_commits": store.ledger_commit_count(),
            "recovered_state_digest": recovered[
                "closed_loop_intake_store_state_digest"
            ],
        }


if __name__ == "__main__":
    print(json.dumps(run_kernel(), ensure_ascii=False, sort_keys=True))
