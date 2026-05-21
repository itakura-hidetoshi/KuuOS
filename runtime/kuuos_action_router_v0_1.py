#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
import hashlib
import json
import sys
from typing import Any, Mapping

TASK_QUEUES = [
    "quarantine_tasks",
    "boundary_recheck_tasks",
    "lineage_recheck_tasks",
    "delivery_recheck_tasks",
    "reobserve_tasks",
    "hold_review_tasks",
    "candidate_next_tasks",
]

TASK_QUEUE_BY_ACTION = {
    "open_quarantine_review_packet": "quarantine_tasks",
    "open_boundary_recheck_packet": "boundary_recheck_tasks",
    "open_lineage_recheck_packet": "lineage_recheck_tasks",
    "open_delivery_recheck_packet": "delivery_recheck_tasks",
    "open_reobserve_packet": "reobserve_tasks",
    "open_hold_review_packet": "hold_review_tasks",
    "open_next_nonfinal_candidate_packet": "candidate_next_tasks",
}

NON_AUTHORITY_FLAGS = {
    "grants_execution_authority": False,
    "grants_truth_authority": False,
    "grants_final_commitment_authority": False,
    "grants_memory_overwrite_authority": False,
    "grants_clinical_authority": False,
    "grants_theorem_authority": False,
    "grants_completed_identity_authority": False,
}

@dataclass(frozen=True)
class KuuOSActionRouterResult:
    router_status: str
    selected_action_hash: str | None
    target_task_queue: str | None
    task_packet: dict[str, Any] | None
    updated_task_board: dict[str, Any]
    grants_execution_authority: bool = False
    grants_truth_authority: bool = False
    grants_final_commitment_authority: bool = False
    grants_memory_overwrite_authority: bool = False
    grants_clinical_authority: bool = False
    grants_theorem_authority: bool = False
    grants_completed_identity_authority: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def empty_task_board() -> dict[str, Any]:
    return {
        "version": "task_board_v0_1",
        "routed_action_hashes": [],
        "task_queues": {name: [] for name in TASK_QUEUES},
        "router_log": [],
        **NON_AUTHORITY_FLAGS,
    }


def _normalize_task_board(task_board: Mapping[str, Any] | None) -> dict[str, Any]:
    if task_board is None:
        return empty_task_board()
    board = deepcopy(dict(task_board))
    board.setdefault("version", "task_board_v0_1")
    board.setdefault("routed_action_hashes", [])
    task_queues = board.setdefault("task_queues", {})
    for name in TASK_QUEUES:
        task_queues.setdefault(name, [])
    board.setdefault("router_log", [])
    for key, value in NON_AUTHORITY_FLAGS.items():
        board[key] = value
    return board


def _canonical_hash(payload: Mapping[str, Any]) -> str:
    data = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


def _action_hash(action_packet: Mapping[str, Any]) -> str:
    if action_packet.get("action_hash"):
        return str(action_packet["action_hash"])
    return _canonical_hash(action_packet)


def _make_task_packet(action_packet: Mapping[str, Any], action_hash: str, target_queue: str, routed_at: str) -> dict[str, Any]:
    return {
        "packet_version": "task_packet_v0_1",
        "task_queue": target_queue,
        "task_type": action_packet.get("action_type", "open_hold_review_packet"),
        "source_action_hash": action_hash,
        "source_receipt_hash": action_packet.get("receipt_hash"),
        "previous_receipt_hash": action_packet.get("previous_receipt_hash"),
        "cycle_id": action_packet.get("cycle_id"),
        "qi_signal": action_packet.get("qi_signal"),
        "qi_reason": action_packet.get("qi_reason"),
        "required_next_action": action_packet.get("required_next_action"),
        "opened_notices": list(action_packet.get("opened_notices", [])),
        "blocked_boundaries": list(action_packet.get("blocked_boundaries", [])),
        "missing_inputs": list(action_packet.get("missing_inputs", [])),
        "qi_process_tensor_receipt": dict(action_packet.get("qi_process_tensor_receipt", {})),
        "routed_at_utc": routed_at,
        "task_status": "OPEN_NON_AUTHORITATIVE",
        "allowed_projection": ["task_packet", "router_log_entry"],
        **NON_AUTHORITY_FLAGS,
    }


def route_next_action(worker_state: Mapping[str, Any], task_board: Mapping[str, Any] | None = None) -> KuuOSActionRouterResult:
    board = _normalize_task_board(task_board)
    routed = set(str(item) for item in board.get("routed_action_hashes", []))
    outbox = worker_state.get("action_outbox", [])
    routed_at = datetime.now(timezone.utc).isoformat()
    for action in outbox:
        if not isinstance(action, Mapping):
            continue
        action_hash = _action_hash(action)
        if action_hash in routed:
            continue
        action_type = str(action.get("action_type", "open_hold_review_packet"))
        target_queue = TASK_QUEUE_BY_ACTION.get(action_type, "hold_review_tasks")
        task_packet = _make_task_packet(action, action_hash, target_queue, routed_at)
        board["routed_action_hashes"].append(action_hash)
        board["task_queues"][target_queue].append(task_packet)
        board["router_log"].append({
            "routed_at_utc": routed_at,
            "action_hash": action_hash,
            "action_type": action_type,
            "target_task_queue": target_queue,
            "source_receipt_hash": action.get("receipt_hash"),
            "qi_process_tensor_receipt": task_packet["qi_process_tensor_receipt"],
            **NON_AUTHORITY_FLAGS,
        })
        return KuuOSActionRouterResult(
            router_status="ROUTED_ONE_APPEND_ONLY",
            selected_action_hash=action_hash,
            target_task_queue=target_queue,
            task_packet=task_packet,
            updated_task_board=board,
        )
    return KuuOSActionRouterResult(
        router_status="NO_UNROUTED_ACTION_PACKET",
        selected_action_hash=None,
        target_task_queue=None,
        task_packet=None,
        updated_task_board=board,
    )


def main(argv: list[str]) -> int:
    if len(argv) not in {2, 3}:
        print("usage: kuuos_action_router_v0_1.py WORKER_STATE.json [TASK_BOARD.json]", file=sys.stderr)
        return 2
    with open(argv[1], "r", encoding="utf-8") as f:
        worker_state = json.load(f)
    task_board = None
    if len(argv) == 3:
        with open(argv[2], "r", encoding="utf-8") as f:
            task_board = json.load(f)
    result = route_next_action(worker_state, task_board)
    print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0

if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
