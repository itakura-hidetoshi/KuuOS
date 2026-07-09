from __future__ import annotations

from dataclasses import asdict, dataclass
import json
import sys
from typing import Any, Mapping, Sequence

from runtime.kuuos_belief_os_types_v0_1 import sha

VERSION = "kuuos_planos_path_integral_candidate_weighting_v0_25"

REENTRY_MODE_DELTA = {
    "reinforce_path_weight": 3.0,
    "open_probe_potential": 1.0,
    "add_barrier_potential": -4.0,
}

NON_AUTHORITY_BOUNDARY = {
    "candidate_weighting_advisory_only": True,
    "selection_authority_granted": False,
    "activation_authorization_granted": False,
    "actos_invoked": False,
    "execution_granted": False,
    "truth_authority_granted": False,
    "memory_overwrite_granted": False,
    "blocker_release_granted": False,
    "external_commit_granted": False,
}


@dataclass(frozen=True)
class CandidateWeightReceipt:
    candidate_id: str
    candidate_digest: str
    source_candidate_type: str
    reentry_mode: str
    path_weight_delta: float
    process_tensor_bonus: float
    blocker_penalty: float
    advisory_score: float
    recommended_replan_route: str
    probe_required: bool
    barrier_required: bool
    execution_ready: bool
    advisory_only: bool = True

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class PlanOSPathIntegralCandidateWeightingReceipt:
    version: str
    status: str
    source_gate_digest: str
    path_integral_digest: str
    qi_process_tensor_digest: str
    blocker_digest: str
    dominant_reentry_mode: str
    candidate_weight_receipts: list[dict[str, Any]]
    retained_candidate_ids: list[str]
    probe_candidate_ids: list[str]
    barrier_candidate_ids: list[str]
    blockers: list[str]
    boundary: dict[str, bool]
    receipt_digest: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _m(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _seq(value: Any) -> list[Mapping[str, Any]]:
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return [item for item in value if isinstance(item, Mapping)]
    return []


def _truthy(value: Any) -> bool:
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "y", "present", "ok", "pass"}
    return bool(value)


def _digest(value: Any) -> str:
    return sha(value)


def _mode(path_integral: Mapping[str, Any]) -> str:
    direct = str(path_integral.get("dominant_reentry_mode", path_integral.get("reentry_mode", "")))
    if direct in REENTRY_MODE_DELTA:
        return direct
    hints = _m(path_integral.get("path_integral_hints"))
    hinted = str(hints.get("dominant_reentry_mode", ""))
    if hinted in REENTRY_MODE_DELTA:
        return hinted
    return "open_probe_potential"


def _candidate_digest(candidate: Mapping[str, Any]) -> str:
    supplied = candidate.get("candidate_digest")
    if isinstance(supplied, str) and supplied:
        return supplied
    return _digest(dict(candidate))


def _candidate_id(candidate: Mapping[str, Any], index: int) -> str:
    value = candidate.get("candidate_id", candidate.get("id", f"candidate-{index}"))
    return str(value)


def _boundary_ok(path_integral: Mapping[str, Any], qi: Mapping[str, Any], blocker: Mapping[str, Any]) -> list[str]:
    blockers: list[str] = []
    p_boundary = _m(path_integral.get("boundary"))
    if not (
        _truthy(path_integral.get("physical_quantum_qi_path_integral_reentry_considered"))
        or _truthy(path_integral.get("path_integral_considered"))
        or _truthy(path_integral.get("physical_quantum_qi_path_integral_rerouted"))
    ):
        blockers.append("path_integral_not_considered")
    if not (
        _truthy(path_integral.get("path_integral_candidate_weighting_only"))
        or _truthy(p_boundary.get("path_integral_candidate_weighting_only"))
        or _truthy(p_boundary.get("candidate_weighting_not_truth"))
        or _truthy(p_boundary.get("path_integral_is_candidate_weighting_not_truth"))
    ):
        blockers.append("path_integral_candidate_weighting_boundary_missing")
    if _truthy(path_integral.get("path_integral_truth_authority")):
        blockers.append("path_integral_truth_authority_forbidden")
    if _truthy(path_integral.get("path_integral_execution_authority")):
        blockers.append("path_integral_execution_authority_forbidden")
    if not (
        _truthy(qi.get("process_tensor_visible"))
        or _truthy(qi.get("processTensorVisible"))
        or _truthy(qi.get("nonmarkov_memory_visible"))
    ):
        blockers.append("qi_process_tensor_evidence_missing")
    if _truthy(qi.get("grants_execution_authority")) or _truthy(qi.get("qi_grants_execution_authority")):
        blockers.append("qi_execution_authority_forbidden")
    if _truthy(blocker.get("blocker_release_granted")) or _truthy(blocker.get("blockerReleaseGranted")):
        blockers.append("blocker_release_forbidden")
    if _truthy(blocker.get("blocker_bypass_granted")) or _truthy(blocker.get("blockerBypassGranted")):
        blockers.append("blocker_bypass_forbidden")
    return blockers


def _recommended_route(mode: str, candidate_type: str, blocker_penalty: float) -> str:
    if blocker_penalty < 0 or mode == "add_barrier_potential":
        return "hold_or_reobserve"
    if mode == "open_probe_potential":
        return "reobserve_before_selection"
    if candidate_type in {"repair", "reroute"}:
        return "retain_for_deliberation"
    return "reinforce_for_next_deliberation"


def build_path_integral_candidate_weighting_receipt(
    *,
    source_gate: Mapping[str, Any],
    path_integral: Mapping[str, Any],
    qi_process_tensor: Mapping[str, Any],
    blocker: Mapping[str, Any],
    candidates: Sequence[Mapping[str, Any]],
) -> PlanOSPathIntegralCandidateWeightingReceipt:
    src = _m(source_gate)
    path = _m(path_integral)
    qi = _m(qi_process_tensor)
    blk = _m(blocker)
    items = _seq(candidates)

    blockers = _boundary_ok(path, qi, blk)
    if not items:
        blockers.append("candidate_list_empty")
    if _truthy(src.get("activation_authorization_granted")) or _truthy(src.get("execution_granted")):
        blockers.append("source_gate_authority_escalation")

    mode = _mode(path)
    path_delta = REENTRY_MODE_DELTA[mode]
    process_bonus = 0.0
    if _truthy(qi.get("process_tensor_visible")) or _truthy(qi.get("processTensorVisible")):
        process_bonus += 0.5
    if _truthy(qi.get("transition_continuity_visible")) or _truthy(qi.get("transitionContinuityVisible")):
        process_bonus += 0.25
    if _truthy(qi.get("memory_continuity_visible")) or _truthy(qi.get("memoryContinuityVisible")):
        process_bonus += 0.25

    blocker_penalty = -2.0 if (
        _truthy(blk.get("missing_evidence_held"))
        or _truthy(blk.get("missingEvidenceHeld"))
        or mode == "add_barrier_potential"
    ) else 0.0

    receipts: list[CandidateWeightReceipt] = []
    for index, candidate in enumerate(items):
        candidate_type = str(candidate.get("candidate_type", candidate.get("type", "unknown")))
        cid = _candidate_id(candidate, index)
        risk = candidate.get("estimated_risk", candidate.get("risk", 0.0))
        try:
            risk_penalty = min(max(float(risk), 0.0), 1.0)
        except (TypeError, ValueError):
            risk_penalty = 0.0
        score = path_delta + process_bonus + blocker_penalty - risk_penalty
        route = _recommended_route(mode, candidate_type, blocker_penalty)
        receipts.append(
            CandidateWeightReceipt(
                candidate_id=cid,
                candidate_digest=_candidate_digest(candidate),
                source_candidate_type=candidate_type,
                reentry_mode=mode,
                path_weight_delta=path_delta,
                process_tensor_bonus=process_bonus,
                blocker_penalty=blocker_penalty,
                advisory_score=score,
                recommended_replan_route=route,
                probe_required=mode == "open_probe_potential",
                barrier_required=mode == "add_barrier_potential" or blocker_penalty < 0,
                execution_ready=False,
            )
        )

    retained = [r.candidate_id for r in receipts if r.recommended_replan_route.startswith("reinforce") or r.recommended_replan_route == "retain_for_deliberation"]
    probe = [r.candidate_id for r in receipts if r.probe_required]
    barrier = [r.candidate_id for r in receipts if r.barrier_required]

    status = "PLANOS_PATH_INTEGRAL_CANDIDATE_WEIGHTING_READY" if not blockers else "PLANOS_PATH_INTEGRAL_CANDIDATE_WEIGHTING_BLOCKED"
    partial = {
        "version": VERSION,
        "status": status,
        "source_gate_digest": _digest(dict(src)),
        "path_integral_digest": _digest(dict(path)),
        "qi_process_tensor_digest": _digest(dict(qi)),
        "blocker_digest": _digest(dict(blk)),
        "dominant_reentry_mode": mode,
        "candidate_weight_receipts": [r.to_dict() for r in receipts],
        "retained_candidate_ids": retained,
        "probe_candidate_ids": probe,
        "barrier_candidate_ids": barrier,
        "blockers": list(blockers),
        "boundary": dict(NON_AUTHORITY_BOUNDARY),
    }
    return PlanOSPathIntegralCandidateWeightingReceipt(
        receipt_digest=_digest(partial),
        **partial,
    )


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: kuuos_planos_path_integral_candidate_weighting_v0_25.py INPUT.json", file=sys.stderr)
        return 2
    with open(argv[1], "r", encoding="utf-8") as handle:
        payload = json.load(handle)
    receipt = build_path_integral_candidate_weighting_receipt(
        source_gate=_m(payload.get("source_gate")),
        path_integral=_m(payload.get("path_integral")),
        qi_process_tensor=_m(payload.get("qi_process_tensor")),
        blocker=_m(payload.get("blocker")),
        candidates=_seq(payload.get("candidates")),
    )
    print(json.dumps(receipt.to_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if receipt.status.endswith("READY") else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
