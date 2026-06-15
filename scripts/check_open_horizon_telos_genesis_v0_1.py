#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
import pathlib
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_open_horizon_telos_genesis_core_v0_1 import (  # noqa: E402
    BLOCKED,
    LICENSE_VERSION,
    OBSERVATION_VERSION,
    PLAN_VERSION,
    READY,
    REQUIRED_BOUNDARY,
    ROOT_VERSION,
    build_open_horizon_telos_genesis,
    observation_digest,
    plan_digest,
    root_digest,
)


def root_packet() -> dict:
    packet = {
        "version": ROOT_VERSION,
        "root_id": "kuuos-root-001",
        "principles": [
            "emptiness",
            "dependent_origination",
            "harmony",
            "contemplation",
            "repairability",
            "benefit_others",
        ],
        "protected": True,
        "self_rewrite_allowed": False,
    }
    packet["root_principles_digest"] = root_digest(packet)
    return packet


def observation(observation_id: str, signals: list[dict]) -> dict:
    packet = {
        "version": OBSERVATION_VERSION,
        "observation_id": observation_id,
        "world_context_digest": "world-" + observation_id,
        "process_tensor_context_digest": "process-" + observation_id,
        "non_markov_context_digest": "memory-" + observation_id,
        "signals": signals,
    }
    packet["observation_digest"] = observation_digest(packet)
    return packet


def plan(run_id: str, root: dict, obs: dict, previous: str = "") -> dict:
    packet = {
        "version": PLAN_VERSION,
        "telos_run_id": run_id,
        "agent_id": "kuuos-agent-alpha",
        "expected_root_principles_digest": root["root_principles_digest"],
        "expected_observation_digest": obs["observation_digest"],
        "expected_previous_state_digest": previous,
        "max_generated_goals": 8,
        "max_selected_goals": 4,
        "min_goal_score": 0.35,
        "min_action_scale": 0.12,
        "renewal_window_steps": 3,
        "boundary": dict(REQUIRED_BOUNDARY),
    }
    packet["telos_plan_digest"] = plan_digest(packet)
    return packet


def license_packet(root: dict, obs: dict, plan_packet: dict) -> dict:
    return {
        "version": LICENSE_VERSION,
        "bound_plan_digest": plan_packet["telos_plan_digest"],
        "bound_observation_digest": obs["observation_digest"],
        "bound_root_principles_digest": root["root_principles_digest"],
        "goal_generation_allowed": True,
        "subgoal_synthesis_allowed": True,
        "goal_selection_allowed": True,
        "commitment_seed_write_allowed": True,
        "state_write_allowed": True,
        "ledger_append_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
        "domain_action_preparation_allowed": True,
        "root_principles_rewrite_allowed": False,
    }


def context(root: pathlib.Path) -> dict:
    return {
        "runtime_root": str(root),
        "open_horizon_telos_genesis_enabled": True,
        "apply_open_horizon_telos_genesis": True,
    }


def read(path: pathlib.Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def assert_good_first_generation(runtime_root: pathlib.Path) -> tuple[dict, dict]:
    root = root_packet()
    obs = observation(
        "obs-001",
        [
            {
                "signal_id": "sig-deficit",
                "kind": "deficit",
                "target": "unresolved observation debt",
                "magnitude": 0.75,
                "urgency": 0.85,
                "evidence": 0.8,
                "uncertainty": 0.25,
                "irreversibility": 0.1,
                "recoverability": 0.9,
                "relational_benefit": 0.85,
                "autonomy_gain": 0.75,
            },
            {
                "signal_id": "sig-opportunity",
                "kind": "opportunity",
                "target": "autonomous tool synthesis",
                "magnitude": 0.8,
                "urgency": 0.65,
                "evidence": 0.7,
                "uncertainty": 0.35,
                "irreversibility": 0.2,
                "recoverability": 0.85,
                "relational_benefit": 0.8,
                "autonomy_gain": 0.95,
            },
            {
                "signal_id": "sig-relationship",
                "kind": "relationship",
                "target": "human agent collaboration",
                "magnitude": 0.65,
                "urgency": 0.55,
                "evidence": 0.85,
                "uncertainty": 0.2,
                "irreversibility": 0.1,
                "recoverability": 0.95,
                "relational_benefit": 0.95,
                "autonomy_gain": 0.6,
            },
        ],
    )
    root_before = copy.deepcopy(root)
    obs_before = copy.deepcopy(obs)
    p = plan("telos-run-001", root, obs)
    lic = license_packet(root, obs, p)
    result = build_open_horizon_telos_genesis(
        runtime_context=context(runtime_root),
        observation_packet=obs,
        root_principles_packet=root,
        telos_plan=p,
        telos_license=lic,
    )
    assert result.status == READY, result.blockers
    assert result.generation_index == 1
    assert result.generated_goal_count == 3
    assert result.selected_goal_count == 3
    assert result.action_ready_count >= 2
    assert result.execution_posture == "commitment_seed_ready"
    assert result.stop_reason == "local_generation_complete_horizon_renewable"
    assert root == root_before and obs == obs_before

    state = read(runtime_root / "kuuos_open_horizon_telos_state_v0_1.json")
    goals = read(runtime_root / "kuuos_open_horizon_goal_set_v0_1.json")
    commitment = read(runtime_root / "kuuos_open_horizon_commitment_seed_v0_1.json")
    assert state["open_horizon"] is True
    assert state["global_generation_cap_declared"] is False
    assert state["root_principles_unchanged"] is True
    assert commitment["next_wake"]["global_horizon_fixed"] is False
    assert commitment["domain_action_prepared"] is True
    assert {g["kind"] for g in goals["selected_goals"]} == {
        "deficit",
        "opportunity",
        "relationship",
    }
    return root, state


def assert_continuation_and_uncertainty_scaling(runtime_root: pathlib.Path, root: dict, previous_state: dict) -> None:
    obs = observation(
        "obs-002",
        [
            {
                "signal_id": "sig-unknown",
                "kind": "unknown",
                "target": "new external environment",
                "magnitude": 0.6,
                "urgency": 0.45,
                "evidence": 0.2,
                "uncertainty": 0.95,
                "irreversibility": 0.8,
                "recoverability": 0.75,
                "relational_benefit": 0.65,
                "autonomy_gain": 0.8,
            }
        ],
    )
    p = plan("telos-run-002", root, obs, previous_state["telos_state_digest"])
    lic = license_packet(root, obs, p)
    result = build_open_horizon_telos_genesis(
        runtime_context=context(runtime_root),
        observation_packet=obs,
        root_principles_packet=root,
        telos_plan=p,
        telos_license=lic,
    )
    assert result.status == READY, result.blockers
    assert result.generation_index == 2
    assert result.selected_goal_count == 1
    goals = read(runtime_root / "kuuos_open_horizon_goal_set_v0_1.json")
    goal = goals["selected_goals"][0]
    assert goal["progress_posture"] == "explore"
    assert goal["action_scale"] > 0.0
    assert goal["goal_statement"].startswith("clarify_")

    replay = build_open_horizon_telos_genesis(
        runtime_context=context(runtime_root),
        observation_packet=obs,
        root_principles_packet=root,
        telos_plan=p,
        telos_license=lic,
    )
    assert replay.status == BLOCKED
    assert "telos_run_replay_detected" in replay.blockers
    assert "observation_replay_detected" in replay.blockers


def assert_boundary_failures() -> None:
    with tempfile.TemporaryDirectory() as directory:
        runtime_root = pathlib.Path(directory)
        root = root_packet()
        obs = observation(
            "obs-invalid",
            [
                {
                    "signal_id": "sig-1",
                    "kind": "opportunity",
                    "target": "test",
                    "magnitude": 0.5,
                    "urgency": 0.5,
                    "evidence": 0.5,
                    "uncertainty": 0.5,
                    "irreversibility": 0.5,
                    "recoverability": 0.5,
                    "relational_benefit": 0.5,
                    "autonomy_gain": 0.5,
                }
            ],
        )
        p = plan("telos-run-invalid", root, obs)
        bad_root = dict(root)
        bad_root["self_rewrite_allowed"] = True
        bad_root["root_principles_digest"] = root_digest(bad_root)
        bad_plan = plan("telos-run-invalid-root", bad_root, obs)
        bad_license = license_packet(bad_root, obs, bad_plan)
        result = build_open_horizon_telos_genesis(
            runtime_context=context(runtime_root),
            observation_packet=obs,
            root_principles_packet=bad_root,
            telos_plan=bad_plan,
            telos_license=bad_license,
        )
        assert result.status == BLOCKED
        assert "root_principles_self_rewrite_not_denied" in result.blockers

        no_generation_license = license_packet(root, obs, p)
        no_generation_license["goal_generation_allowed"] = False
        result = build_open_horizon_telos_genesis(
            runtime_context=context(runtime_root),
            observation_packet=obs,
            root_principles_packet=root,
            telos_plan=p,
            telos_license=no_generation_license,
        )
        assert result.status == BLOCKED
        assert "goal_generation_not_allowed" in result.blockers


def assert_manifest() -> None:
    manifest = json.loads(
        (ROOT / "manifests/kuuos_open_horizon_telos_genesis_v0_1.json").read_text(encoding="utf-8")
    )
    for group in ("runtime", "scripts", "docs", "examples", "workflows"):
        for relative in manifest[group]:
            assert (ROOT / relative).is_file(), relative


def main() -> int:
    with tempfile.TemporaryDirectory() as directory:
        runtime_root = pathlib.Path(directory)
        root, state = assert_good_first_generation(runtime_root)
        assert_continuation_and_uncertainty_scaling(runtime_root, root, state)
        ledger_lines = (runtime_root / "kuuos_open_horizon_telos_ledger_v0_1.jsonl").read_text(
            encoding="utf-8"
        ).splitlines()
        assert len(ledger_lines) == 2
    assert_boundary_failures()
    assert_manifest()
    print("PASS: KuuOS open-horizon telos genesis v0.1 checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
