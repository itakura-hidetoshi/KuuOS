from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

from runtime.kuuos_belief_os_types_v0_1 import sha
from runtime.kuuos_qi_window_trajectory_kernel_v0_29 import (
    build_trajectory_packet,
    evaluate_trajectory_packet,
)
from runtime.kuuos_qi_window_trajectory_ledger_v0_29 import (
    QiWindowTrajectoryLedger,
    TrajectoryLedgerError,
)


def _report(
    label: str,
    index: int,
    *,
    classification: str,
    lower: float,
    center: float,
    upper: float,
    support: float,
    burden: float,
    quality: float = 0.90,
    red_flags: bool = False,
) -> dict[str, Any]:
    return {
        "report_id": f"{label}-report-{index}",
        "observed_at_ms": index * 1000,
        "source_v028_report_digest": sha(f"{label}:v028:{index}"),
        "classification": classification,
        "interval_lower": lower,
        "interval_center": center,
        "interval_upper": upper,
        "support_score": support,
        "burden_score": burden,
        "evidence_quality": quality,
        "red_flags_visible": red_flags,
        "candidate_only": True,
        "source_trace": f"trace:{label}:{index}",
    }


def _packet(label: str, reports: list[dict[str, Any]]) -> dict[str, Any]:
    return build_trajectory_packet(
        packet_id=f"trajectory-{label}",
        context_digest=sha(f"context:{label}"),
        source_v028_kernel_digest=sha("v028-kernel"),
        process_tensor_lineage_digest=sha(f"process-lineage:{label}"),
        reports=reports,
        created_at_ms=100_000,
    )


def run_qi_window_trajectory_scenarios() -> dict[str, Any]:
    opening = evaluate_trajectory_packet(
        _packet(
            "opening",
            [
                _report("opening", 1, classification="HEALING_POTENTIAL_UNCERTAIN", lower=0.20, center=0.35, upper=0.50, support=0.52, burden=0.38),
                _report("opening", 2, classification="HEALING_POTENTIAL_UNCERTAIN", lower=0.30, center=0.45, upper=0.60, support=0.62, burden=0.30),
                _report("opening", 3, classification="HEALING_POTENTIAL_VISIBLE", lower=0.42, center=0.58, upper=0.72, support=0.74, burden=0.22),
            ],
        )
    )
    assert opening["trajectory_classification"] == "WINDOW_OPENING"

    stable = evaluate_trajectory_packet(
        _packet(
            "stable",
            [
                _report("stable", 1, classification="HEALING_POTENTIAL_VISIBLE", lower=0.46, center=0.60, upper=0.74, support=0.74, burden=0.20),
                _report("stable", 2, classification="HEALING_POTENTIAL_VISIBLE", lower=0.47, center=0.61, upper=0.75, support=0.75, burden=0.19),
                _report("stable", 3, classification="HEALING_POTENTIAL_VISIBLE", lower=0.46, center=0.60, upper=0.74, support=0.74, burden=0.20),
            ],
        )
    )
    assert stable["trajectory_classification"] == "WINDOW_STABLE_VISIBLE"

    oscillating = evaluate_trajectory_packet(
        _packet(
            "oscillating",
            [
                _report("oscillating", 1, classification="HEALING_POTENTIAL_VISIBLE", lower=0.42, center=0.55, upper=0.68, support=0.70, burden=0.22),
                _report("oscillating", 2, classification="HEALING_POTENTIAL_UNCERTAIN", lower=0.22, center=0.35, upper=0.48, support=0.50, burden=0.42),
                _report("oscillating", 3, classification="HEALING_POTENTIAL_VISIBLE", lower=0.44, center=0.58, upper=0.72, support=0.72, burden=0.20),
                _report("oscillating", 4, classification="HEALING_POTENTIAL_UNCERTAIN", lower=0.20, center=0.33, upper=0.46, support=0.48, burden=0.45),
            ],
        )
    )
    assert oscillating["trajectory_classification"] == "WINDOW_OSCILLATING"

    dormant = evaluate_trajectory_packet(
        _packet(
            "dormant",
            [
                _report("dormant", 1, classification="HEALING_POTENTIAL_VISIBLE", lower=0.50, center=0.65, upper=0.80, support=0.80, burden=0.16),
                _report("dormant", 2, classification="HEALING_POTENTIAL_VISIBLE", lower=0.40, center=0.55, upper=0.70, support=0.68, burden=0.26),
                _report("dormant", 3, classification="HEALING_POTENTIAL_CONSTRAINED", lower=0.18, center=0.25, upper=0.30, support=0.30, burden=0.72),
            ],
        )
    )
    assert dormant["trajectory_classification"] == "WINDOW_DORMANT_REOPENABLE"
    assert dormant["metrics"]["reopening_memory"] > 0.0
    assert dormant["prior_visible_window_erased"] is False

    constricting = evaluate_trajectory_packet(
        _packet(
            "constricting",
            [
                _report("constricting", 1, classification="HEALING_POTENTIAL_UNCERTAIN", lower=0.18, center=0.32, upper=0.46, support=0.42, burden=0.50),
                _report("constricting", 2, classification="HEALING_POTENTIAL_CONSTRAINED", lower=0.12, center=0.24, upper=0.32, support=0.30, burden=0.68),
                _report("constricting", 3, classification="HEALING_POTENTIAL_CONSTRAINED", lower=0.08, center=0.18, upper=0.26, support=0.24, burden=0.76),
            ],
        )
    )
    assert constricting["trajectory_classification"] == "WINDOW_CONSTRICTING"
    assert constricting["relapse_claimed_irreversible"] is False

    review = evaluate_trajectory_packet(
        _packet(
            "review",
            [
                _report("review", 1, classification="HEALING_POTENTIAL_VISIBLE", lower=0.45, center=0.60, upper=0.75, support=0.75, burden=0.20),
                _report("review", 2, classification="HEALING_POTENTIAL_VISIBLE", lower=0.47, center=0.62, upper=0.77, support=0.77, burden=0.18),
                _report("review", 3, classification="CLINICIAN_REVIEW_REQUIRED", lower=0.40, center=0.55, upper=0.70, support=0.65, burden=0.30, red_flags=True),
            ],
        )
    )
    assert review["trajectory_classification"] == "REVIEW_HANDOFF"

    insufficient = evaluate_trajectory_packet(
        _packet(
            "insufficient",
            [
                _report("insufficient", 1, classification="HEALING_POTENTIAL_UNCERTAIN", lower=0.25, center=0.40, upper=0.55, support=0.50, burden=0.40),
                _report("insufficient", 2, classification="HEALING_POTENTIAL_VISIBLE", lower=0.40, center=0.55, upper=0.70, support=0.68, burden=0.25),
            ],
        )
    )
    assert insufficient["trajectory_classification"] == "INSUFFICIENT_HISTORY"

    with TemporaryDirectory(prefix="kuuos-v029-") as temporary:
        ledger = QiWindowTrajectoryLedger(Path(temporary))
        first = ledger.append(opening)
        replay = ledger.append(opening)
        second = ledger.append(dormant)
        assert first["status"] == "APPENDED"
        assert replay["status"] == "REPLAYED"
        assert second["ledger_count"] == 2
        tampered = deepcopy(dormant)
        tampered["prior_visible_window_erased"] = True
        try:
            ledger.append(tampered)
        except TrajectoryLedgerError:
            tamper_rejected = True
        else:
            tamper_rejected = False
        assert tamper_rejected

    return {
        "status": "KUUOS_QI_WINDOW_TRAJECTORY_V0_29_OK",
        "opening": opening["trajectory_classification"],
        "stable": stable["trajectory_classification"],
        "oscillating": oscillating["trajectory_classification"],
        "dormant": dormant["trajectory_classification"],
        "constricting": constricting["trajectory_classification"],
        "review": review["trajectory_classification"],
        "insufficient": insufficient["trajectory_classification"],
        "reopening_memory": dormant["metrics"]["reopening_memory"],
        "single_decline_closure": False,
        "irreversibility_claimed": False,
        "prognosis_claimed": False,
        "ledger_replay": replay["status"],
        "tamper_rejected": tamper_rejected,
    }


__all__ = ["run_qi_window_trajectory_scenarios"]
