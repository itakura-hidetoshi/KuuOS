#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import argparse
import json
from typing import Any


@dataclass(frozen=True)
class KuuOSQiReentryChainControllerDecision:
    controller_version: str
    controller_status: str
    requested_max_cycles: int
    allowed_max_cycles: int
    controller_decision: str
    controller_reason: str
    health_projection_path: str | None
    daemon_health_status: str | None
    next_operator_action: str | None
    recoverability_status: str | None
    recoverability_score: float | None
    recovery_unsafe: bool | None
    local_recovery_allowed: bool | None
    chain_invocation_allowed: bool
    runtime_hot_path_tier: str
    validation_tier: str
    grants_execution_authority: bool = False
    grants_truth_authority: bool = False
    grants_final_commitment_authority: bool = False
    grants_memory_overwrite_authority: bool = False
    grants_clinical_authority: bool = False
    grants_theorem_authority: bool = False
    grants_completed_identity_authority: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _read_json(path: Path) -> dict[str, Any] | None:
    if not path.is_file():
        return None
    value = json.loads(path.read_text(encoding="utf-8"))
    return value if isinstance(value, dict) else None


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _clamp_requested(value: int) -> int:
    return max(0, min(int(value), 5))


def _score(value: Any) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def decide_qi_reentry_chain_controller(
    *,
    health_projection: dict[str, Any] | None,
    requested_max_cycles: int = 2,
    health_projection_path: Path | None = None,
) -> KuuOSQiReentryChainControllerDecision:
    requested = _clamp_requested(requested_max_cycles)
    if health_projection is None:
        return KuuOSQiReentryChainControllerDecision(
            controller_version="kuuos_runtime_daemon_qi_reentry_chain_controller_v0_1",
            controller_status="QI_REENTRY_CHAIN_CONTROLLER_DECIDED",
            requested_max_cycles=requested,
            allowed_max_cycles=0,
            controller_decision="CHAIN_NOT_ALLOWED",
            controller_reason="health_projection_missing",
            health_projection_path=str(health_projection_path) if health_projection_path else None,
            daemon_health_status=None,
            next_operator_action=None,
            recoverability_status=None,
            recoverability_score=None,
            recovery_unsafe=None,
            local_recovery_allowed=None,
            chain_invocation_allowed=False,
            runtime_hot_path_tier="T0_hot_path_controller",
            validation_tier="T3_runtime_full_check",
        )

    daemon_health = health_projection.get("daemon_health_status")
    action = health_projection.get("next_operator_action")
    recoverability = health_projection.get("recoverability_status")
    score = _score(health_projection.get("recoverability_score"))
    unsafe = bool(health_projection.get("recovery_unsafe"))
    local_allowed = health_projection.get("local_recovery_allowed") is True

    allowed_cycles = 0
    decision = "CHAIN_NOT_ALLOWED"
    reason = "health_does_not_allow_chain"
    if unsafe:
        reason = "recovery_unsafe"
    elif action != "invoke_manual_runner":
        reason = "next_operator_action_not_invoke_manual_runner"
    elif recoverability != "RECOVERABLE_BY_MANUAL_RUNNER":
        reason = "not_recoverable_by_manual_runner"
    elif not local_allowed:
        reason = "local_recovery_not_allowed"
    else:
        effective_score = score if score is not None else 0.0
        if effective_score >= 0.9:
            allowed_cycles = min(requested, 3)
            decision = "CHAIN_ALLOWED_STABLE"
            reason = "manual_runner_recovery_stable"
        elif effective_score >= 0.7:
            allowed_cycles = min(requested, 2)
            decision = "CHAIN_ALLOWED_BOUNDED"
            reason = "manual_runner_recovery_bounded"
        else:
            allowed_cycles = min(requested, 1)
            decision = "CHAIN_ALLOWED_SINGLE_STEP"
            reason = "manual_runner_recovery_fragile_single_step"

    return KuuOSQiReentryChainControllerDecision(
        controller_version="kuuos_runtime_daemon_qi_reentry_chain_controller_v0_1",
        controller_status="QI_REENTRY_CHAIN_CONTROLLER_DECIDED",
        requested_max_cycles=requested,
        allowed_max_cycles=allowed_cycles,
        controller_decision=decision,
        controller_reason=reason,
        health_projection_path=str(health_projection_path) if health_projection_path else None,
        daemon_health_status=str(daemon_health) if daemon_health is not None else None,
        next_operator_action=str(action) if action is not None else None,
        recoverability_status=str(recoverability) if recoverability is not None else None,
        recoverability_score=score,
        recovery_unsafe=unsafe,
        local_recovery_allowed=local_allowed,
        chain_invocation_allowed=allowed_cycles > 0,
        runtime_hot_path_tier="T0_hot_path_controller",
        validation_tier="T3_runtime_full_check",
    )


def read_and_decide_qi_reentry_chain_controller(
    *,
    daemon_dir: Path,
    requested_max_cycles: int = 2,
) -> KuuOSQiReentryChainControllerDecision:
    health_path = Path(daemon_dir) / "daemon_qi_process_tensor_health_projection_v0_1.json"
    return decide_qi_reentry_chain_controller(
        health_projection=_read_json(health_path),
        requested_max_cycles=requested_max_cycles,
        health_projection_path=health_path,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Decide KuuOS Qi reentry handoff chain controller v0.1")
    parser.add_argument("--daemon-dir", type=Path, required=True)
    parser.add_argument("--requested-max-cycles", type=int, default=2)
    parser.add_argument("--write", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    decision = read_and_decide_qi_reentry_chain_controller(
        daemon_dir=args.daemon_dir,
        requested_max_cycles=args.requested_max_cycles,
    )
    if args.write:
        _write_json(args.daemon_dir / "daemon_qi_reentry_chain_controller_decision_v0_1.json", decision.to_dict())
    print(json.dumps(decision.to_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
