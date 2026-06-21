from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

from runtime.kuuos_belief_os_types_v0_1 import sha
from runtime.kuuos_qi_diagnostic_candidate_ledger_v0_28 import (
    DiagnosticLedgerError,
    QiDiagnosticCandidateLedger,
)
from runtime.kuuos_qi_healing_potential_diagnostic_kernel_v0_28 import (
    build_diagnostic_packet,
    evaluate_diagnostic_packet,
)


def _event(
    time_index: int,
    *,
    recoverability: float,
    coherence: float,
    distortion: float,
    residue: float,
    memory_gain: float,
    response_delta: float,
    stability: float,
    burden: float,
    label: str,
) -> dict[str, Any]:
    return {
        "time_index": time_index,
        "observation_id": f"observation-{label}-{time_index}",
        "qi_recoverability_margin": recoverability,
        "qi_coherence_margin": coherence,
        "qi_transport_distortion": distortion,
        "qi_tail_residue": residue,
        "qi_memory_gain": memory_gain,
        "response_delta": response_delta,
        "adaptive_stability": stability,
        "intervention_burden": burden,
        "bounded_intervention": True,
        "backaction_visible": True,
        "source_trace": f"trace:{label}:{time_index}",
    }


def _hypotheses(label: str, *, severity: float) -> list[dict[str, Any]]:
    return [
        {
            "hypothesis_id": f"{label}-h1",
            "label": "primary-pattern-candidate",
            "support": 0.72,
            "counterevidence": 0.18,
            "uncertainty": 0.24,
            "severity": severity,
            "candidate_only": True,
            "source_traces": [f"trace:{label}:1", f"trace:{label}:2"],
        },
        {
            "hypothesis_id": f"{label}-h2",
            "label": "alternative-pattern-candidate",
            "support": 0.46,
            "counterevidence": 0.30,
            "uncertainty": 0.42,
            "severity": max(0.0, severity - 0.15),
            "candidate_only": True,
            "source_traces": [f"trace:{label}:2", f"trace:{label}:3"],
        },
    ]


def _packet(
    label: str,
    history: list[dict[str, Any]],
    *,
    red_flags: list[str] | None = None,
    process_tensor_visible: bool = True,
    severity: float = 0.8,
    source_coverage: float = 0.95,
    temporal_coverage: float = 0.90,
    contradiction_visibility: float = 0.90,
) -> dict[str, Any]:
    return build_diagnostic_packet(
        packet_id=f"diagnostic-{label}",
        context_digest=sha(f"context:{label}"),
        source_v027_state_digest=sha(f"v027-state:{label}"),
        qi_process_tensor_receipt_digest=sha(f"process-tensor:{label}"),
        qi_observation_candidate_digest=sha(f"observation-candidate:{label}"),
        process_tensor_visible=process_tensor_visible,
        process_history=history,
        diagnostic_hypotheses=_hypotheses(label, severity=severity),
        red_flags=list(red_flags or []),
        source_coverage=source_coverage,
        temporal_coverage=temporal_coverage,
        contradiction_visibility=contradiction_visibility,
        created_at_ms=100_000,
    )


def run_qi_healing_potential_diagnostic_scenarios() -> dict[str, Any]:
    visible_history = [
        _event(
            1,
            recoverability=0.75,
            coherence=0.70,
            distortion=0.14,
            residue=0.16,
            memory_gain=0.72,
            response_delta=0.00,
            stability=0.78,
            burden=0.14,
            label="visible",
        ),
        _event(
            2,
            recoverability=0.82,
            coherence=0.76,
            distortion=0.11,
            residue=0.12,
            memory_gain=0.78,
            response_delta=0.24,
            stability=0.84,
            burden=0.11,
            label="visible",
        ),
        _event(
            3,
            recoverability=0.87,
            coherence=0.82,
            distortion=0.09,
            residue=0.10,
            memory_gain=0.81,
            response_delta=0.31,
            stability=0.88,
            burden=0.09,
            label="visible",
        ),
        _event(
            4,
            recoverability=0.90,
            coherence=0.85,
            distortion=0.08,
            residue=0.08,
            memory_gain=0.84,
            response_delta=0.28,
            stability=0.90,
            burden=0.08,
            label="visible",
        ),
    ]
    visible_packet = _packet("visible", visible_history, severity=0.92)
    visible_report = evaluate_diagnostic_packet(visible_packet)
    assert visible_report["healing_potential"]["classification"] == (
        "HEALING_POTENTIAL_VISIBLE"
    )
    assert visible_report["healing_potential"]["severity_used_in_score"] is False
    assert visible_report["diagnostic_hypothesis_summary"][
        "single_winner_forced"
    ] is False

    constrained_history = [
        _event(
            1,
            recoverability=0.18,
            coherence=0.22,
            distortion=0.78,
            residue=0.82,
            memory_gain=0.18,
            response_delta=-0.24,
            stability=0.20,
            burden=0.82,
            label="constrained",
        ),
        _event(
            2,
            recoverability=0.16,
            coherence=0.20,
            distortion=0.82,
            residue=0.86,
            memory_gain=0.16,
            response_delta=-0.28,
            stability=0.18,
            burden=0.86,
            label="constrained",
        ),
        _event(
            3,
            recoverability=0.14,
            coherence=0.18,
            distortion=0.86,
            residue=0.88,
            memory_gain=0.14,
            response_delta=-0.22,
            stability=0.16,
            burden=0.88,
            label="constrained",
        ),
        _event(
            4,
            recoverability=0.15,
            coherence=0.18,
            distortion=0.84,
            residue=0.87,
            memory_gain=0.15,
            response_delta=-0.18,
            stability=0.17,
            burden=0.87,
            label="constrained",
        ),
    ]
    constrained_packet = _packet(
        "constrained", constrained_history, severity=0.88
    )
    constrained_report = evaluate_diagnostic_packet(constrained_packet)
    assert constrained_report["healing_potential"]["classification"] == (
        "HEALING_POTENTIAL_CONSTRAINED"
    )
    assert constrained_report["healing_potential"]["irreversibility_claimed"] is False

    red_flag_packet = _packet(
        "red-flag",
        visible_history,
        red_flags=["declared-red-flag-review-surface"],
        severity=0.95,
    )
    red_flag_report = evaluate_diagnostic_packet(red_flag_packet)
    assert red_flag_report["healing_potential"]["classification"] == (
        "CLINICIAN_REVIEW_REQUIRED"
    )
    assert red_flag_report["route"] == "CLINICIAN_REVIEW_HANDOFF"
    assert red_flag_report["route_is_clinical_instruction"] is False

    insufficient_packet = _packet(
        "insufficient",
        visible_history[:2],
        process_tensor_visible=False,
        source_coverage=0.30,
        temporal_coverage=0.20,
        contradiction_visibility=0.40,
    )
    insufficient_report = evaluate_diagnostic_packet(insufficient_packet)
    assert insufficient_report["healing_potential"]["classification"] == (
        "INSUFFICIENT_EVIDENCE"
    )
    assert insufficient_report["route"] == "REOBSERVE"

    with TemporaryDirectory(prefix="kuuos-diagnostic-v028-") as temporary:
        ledger = QiDiagnosticCandidateLedger(Path(temporary))
        first = ledger.append(visible_report)
        replay = ledger.append(visible_report)
        second = ledger.append(constrained_report)
        assert first["status"] == "APPENDED"
        assert replay["status"] == "REPLAYED"
        assert second["ledger_count"] == 2
        tampered = deepcopy(red_flag_report)
        tampered["healing_potential"]["healing_guaranteed"] = True
        try:
            ledger.append(tampered)
        except DiagnosticLedgerError:
            tamper_rejected = True
        else:
            tamper_rejected = False
        assert tamper_rejected is True

    return {
        "status": "KUUOS_QI_HEALING_POTENTIAL_DIAGNOSTIC_V0_28_OK",
        "visible_class": visible_report["healing_potential"]["classification"],
        "visible_interval": [
            visible_report["healing_potential"]["interval_lower"],
            visible_report["healing_potential"]["interval_upper"],
        ],
        "constrained_class": constrained_report["healing_potential"][
            "classification"
        ],
        "red_flag_class": red_flag_report["healing_potential"]["classification"],
        "insufficient_class": insufficient_report["healing_potential"][
            "classification"
        ],
        "severity_separate_from_healing_score": True,
        "healing_guaranteed": False,
        "plural_hypotheses_preserved": True,
        "clinician_review_required": True,
        "ledger_replay_status": replay["status"],
        "tamper_rejected": tamper_rejected,
    }


__all__ = ["run_qi_healing_potential_diagnostic_scenarios"]
