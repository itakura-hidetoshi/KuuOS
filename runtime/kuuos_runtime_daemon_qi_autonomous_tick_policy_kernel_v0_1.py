#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
from typing import Any, Mapping

A_ADVANCE = "advance_tick"
A_HOLD = "hold"
A_OBSERVE = "observe"
A_NOTIFY = "notify"
A_TICKET = "ticket"
A_HANDOVER = "handover"
A_FREEZE = "freeze"
ACTIONS = [A_ADVANCE, A_HOLD, A_OBSERVE, A_NOTIFY, A_TICKET, A_HANDOVER, A_FREEZE]
RANK = {name: index for index, name in enumerate(ACTIONS)}


@dataclass(frozen=True)
class QiAutonomousTickPolicyKernel:
    kernel_version: str
    policy_status: str
    policy_packet_id: str
    selected_action: str
    decisionos_action: str | None
    cbf_action: str | None
    token_ledger_action: str | None
    process_tensor_action: str | None
    same_root: bool
    next_tick_number: int | None
    advance_tick_allowed: bool
    hold_selected: bool
    observe_selected: bool
    notify_selected: bool
    ticket_selected: bool
    handover_selected: bool
    freeze_selected: bool
    reason_codes: list[str]
    blockers: list[str]
    source_decision_id: str | None
    source_cbf_id: str | None
    source_token_ledger_id: str | None
    source_process_tensor_id: str | None
    read_only_policy_surface: bool

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _m(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _sha(value: Mapping[str, Any]) -> str:
    payload = json.dumps(dict(value), ensure_ascii=False, sort_keys=True).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _action(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip().lower()
    aliases = {
        "proceed": A_ADVANCE,
        "advance": A_ADVANCE,
        "next_tick": A_ADVANCE,
        "reobserve": A_OBSERVE,
        "open_ticket": A_TICKET,
        "external_ticket": A_TICKET,
        "do_not_run": A_FREEZE,
        "do_not_execute": A_FREEZE,
        "hard_freeze": A_FREEZE,
    }
    return aliases.get(text, text)


def _truthy(value: Any) -> bool:
    return value is True or str(value).strip().lower() in {"true", "yes", "1"}


def _int(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _rank(action: str | None) -> int:
    return RANK.get(action or A_HOLD, RANK[A_HOLD])


def _max_action(actions: list[str | None]) -> str:
    valid = [a for a in actions if a in RANK]
    if not valid:
        return A_HOLD
    return sorted(valid, key=_rank, reverse=True)[0]


def build_qi_autonomous_tick_policy_kernel(
    *,
    decisionos_packet: Mapping[str, Any],
    cbf_packet: Mapping[str, Any],
    token_ledger_packet: Mapping[str, Any],
    process_tensor_packet: Mapping[str, Any],
    policy_context: Mapping[str, Any] | None = None,
) -> QiAutonomousTickPolicyKernel:
    decision = _m(decisionos_packet)
    cbf = _m(cbf_packet)
    token = _m(token_ledger_packet)
    pt = _m(process_tensor_packet)
    ctx = _m(policy_context)

    blockers: list[str] = []
    reasons: list[str] = []

    if ctx.get("tick_policy_enabled") is not True:
        blockers.append("tick_policy_enabled_not_true")
    if ctx.get("read_only_policy_surface") is not True:
        blockers.append("read_only_policy_surface_not_true")

    roots = [decision.get("root_id"), cbf.get("root_id"), token.get("root_id"), pt.get("root_id")]
    same_root = bool(roots[0]) and all(item == roots[0] for item in roots)
    if not same_root:
        blockers.append("same_root_failed")
        reasons.append("same_root_failed")

    ids = {
        "decision": decision.get("decision_id") or decision.get("packet_id"),
        "cbf": cbf.get("cbf_id") or cbf.get("packet_id"),
        "token": token.get("token_ledger_id") or token.get("packet_id"),
        "pt": pt.get("process_tensor_id") or pt.get("packet_id"),
    }
    for key, value in ids.items():
        if not value:
            blockers.append(f"{key}_id_missing")

    da = _action(decision.get("decision_action") or decision.get("selected_action"))
    ca = _action(cbf.get("cbf_action") or cbf.get("recommended_action"))
    ta = _action(token.get("token_ledger_action") or token.get("recommended_action"))
    pa = _action(pt.get("process_tensor_action") or pt.get("recommended_action"))

    for label, action in (("decision", da), ("cbf", ca), ("token", ta), ("process_tensor", pa)):
        if action not in RANK:
            blockers.append(f"{label}_action_unknown")
            reasons.append("unknown_action")

    if cbf.get("cbf_ok") is not True:
        blockers.append("cbf_not_ok")
        reasons.append("cbf_not_ok")
    if _truthy(cbf.get("barrier_closed")):
        ca = A_FREEZE
        reasons.append("cbf_barrier_closed")

    remaining = _int(token.get("remaining_tokens"), 0)
    minimum = _int(token.get("minimum_required_tokens"), 1)
    if token.get("token_ledger_ok") is not True:
        blockers.append("token_ledger_not_ok")
        reasons.append("token_ledger_not_ok")
    if remaining < minimum and _rank(ta) < _rank(A_HOLD):
        ta = A_HOLD
        reasons.append("token_floor")

    if pt.get("process_tensor_ok") is not True:
        blockers.append("process_tensor_not_ok")
        reasons.append("process_tensor_not_ok")
    if _truthy(pt.get("non_markov_unresolved")) and _rank(pa) < _rank(A_OBSERVE):
        pa = A_OBSERVE
        reasons.append("non_markov_observe")
    if _truthy(pt.get("recovery_witness_missing")) and _rank(pa) < _rank(A_HOLD):
        pa = A_HOLD
        reasons.append("recovery_witness_missing")

    uncertainty = _float(decision.get("uncertainty"), 0.0)
    if uncertainty >= _float(ctx.get("handover_uncertainty_threshold"), 0.85):
        da = A_HANDOVER if _rank(da) < _rank(A_HANDOVER) else da
        reasons.append("uncertainty_handover")
    elif uncertainty >= _float(ctx.get("ticket_uncertainty_threshold"), 0.65):
        da = A_TICKET if _rank(da) < _rank(A_TICKET) else da
        reasons.append("uncertainty_ticket")
    elif uncertainty >= _float(ctx.get("notify_uncertainty_threshold"), 0.45):
        da = A_NOTIFY if _rank(da) < _rank(A_NOTIFY) else da
        reasons.append("uncertainty_notify")

    for flag, action, reason in (
        ("observe_required", A_OBSERVE, "decision_observe"),
        ("ticket_required", A_TICKET, "decision_ticket"),
        ("handover_required", A_HANDOVER, "decision_handover"),
        ("freeze_required", A_FREEZE, "decision_freeze"),
    ):
        if _truthy(decision.get(flag)) and _rank(da) < _rank(action):
            da = action
            reasons.append(reason)

    if any(_truthy(src.get("write_performed")) or _truthy(src.get("control_granted")) for src in (decision, cbf, token, pt, ctx)):
        blockers.append("write_or_control_present")
        reasons.append("read_only_boundary")

    selected = _max_action([da, ca, ta, pa])
    if blockers and selected == A_ADVANCE:
        selected = A_HOLD
        reasons.append("advance_downgraded")
    if A_FREEZE in {da, ca, ta, pa}:
        selected = A_FREEZE

    current_tick = _int(ctx.get("current_tick"), _int(token.get("current_tick"), 0))
    next_tick = current_tick + 1 if selected == A_ADVANCE and not blockers and same_root else None

    material = {
        "root": roots[0] if same_root else None,
        "selected": selected,
        "decision": da,
        "cbf": ca,
        "token": ta,
        "process_tensor": pa,
        "ids": ids,
    }
    packet_id = "qi-tick-policy-" + _sha(material)[:16]
    status = "QI_AUTONOMOUS_TICK_POLICY_READY" if not blockers else "QI_AUTONOMOUS_TICK_POLICY_BLOCKED"

    return QiAutonomousTickPolicyKernel(
        kernel_version="kuuos_runtime_daemon_qi_autonomous_tick_policy_kernel_v0_1",
        policy_status=status,
        policy_packet_id=packet_id,
        selected_action=selected,
        decisionos_action=da,
        cbf_action=ca,
        token_ledger_action=ta,
        process_tensor_action=pa,
        same_root=same_root,
        next_tick_number=next_tick,
        advance_tick_allowed=selected == A_ADVANCE and not blockers and same_root,
        hold_selected=selected == A_HOLD,
        observe_selected=selected == A_OBSERVE,
        notify_selected=selected == A_NOTIFY,
        ticket_selected=selected == A_TICKET,
        handover_selected=selected == A_HANDOVER,
        freeze_selected=selected == A_FREEZE,
        reason_codes=sorted(set(reasons)),
        blockers=blockers,
        source_decision_id=str(ids["decision"]) if ids["decision"] else None,
        source_cbf_id=str(ids["cbf"]) if ids["cbf"] else None,
        source_token_ledger_id=str(ids["token"]) if ids["token"] else None,
        source_process_tensor_id=str(ids["pt"]) if ids["pt"] else None,
        read_only_policy_surface=ctx.get("read_only_policy_surface") is True,
    )
