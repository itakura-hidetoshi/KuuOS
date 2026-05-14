#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass, asdict
import importlib.util
import json
import pathlib
import sys
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
ADAPTER_PATH = ROOT / "examples" / "two_truths_mass_gap_runtime_adapter_minimal.py"

spec = importlib.util.spec_from_file_location("two_truths_mass_gap_runtime_adapter_minimal", ADAPTER_PATH)
if spec is None or spec.loader is None:
    raise RuntimeError("failed to load two truths mass gap runtime adapter")
adapter = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = adapter
spec.loader.exec_module(adapter)


@dataclass(frozen=True)
class TwoTruthsClaim:
    ultimate_truth_direct_objectified: bool = False
    conventional_truth_denied: bool = False
    collapses_ultimate_to_conventional: bool = False
    collapses_conventional_to_ultimate: bool = False
    treats_mass_gap_as_final_public_theorem_authority: bool = False
    grants_execution_from_gap: bool = False
    mass_gap_bridge_input: dict[str, Any] | None = None


def _bridge_input(data: dict[str, Any] | None) -> Any:
    if data is None:
        return adapter.MassGapTwoTruthsRuntimeInput()
    return adapter.MassGapTwoTruthsRuntimeInput(**data)


def evaluate_two_truths(c: TwoTruthsClaim) -> dict[str, Any]:
    bridge_input = _bridge_input(c.mass_gap_bridge_input)
    bridge_decision = adapter.evaluate_mass_gap_bridge(bridge_input)
    bridge = asdict(bridge_decision)

    if c.ultimate_truth_direct_objectified:
        status, reason = "REJECT", "ultimate_truth_direct_objectification_forbidden"
    elif c.conventional_truth_denied:
        status, reason = "REJECT", "conventional_truth_denial_forbidden"
    elif c.collapses_ultimate_to_conventional:
        status, reason = "REJECT", "ultimate_to_conventional_collapse_forbidden"
    elif c.collapses_conventional_to_ultimate:
        status, reason = "REJECT", "conventional_to_ultimate_collapse_forbidden"
    elif c.treats_mass_gap_as_final_public_theorem_authority:
        status, reason = "REJECT", "mass_gap_bridge_is_reference_barrier_not_public_final_authority"
    elif c.grants_execution_from_gap:
        status, reason = "REJECT", "mass_gap_bridge_does_not_grant_execution_authority"
    elif bridge_decision.decision_status != "bridge_accepted_as_reference_barrier":
        status, reason = "HOLD", "mass_gap_two_truths_reference_barrier_not_accepted"
    else:
        status, reason = "CANDIDATE", "two_truths_non_collapse_barrier_active"

    return {
        "status": status,
        "reason": reason,
        "principle": "two_truths_mass_gap_runtime",
        "paramartha_objectification_allowed": False,
        "samvrti_denial_allowed": False,
        "ultimate_to_conventional_collapse_allowed": False,
        "conventional_to_ultimate_collapse_allowed": False,
        "mass_gap_bridge_authority": bridge_decision.authority_expansion,
        "mass_gap_reference_barrier_status": bridge_decision.two_truths_non_collapse_barrier,
        "bridge_decision": bridge,
        "execution_authority_granted": False,
        "proof_authority_granted": False,
        "truth_authority_granted": False,
        "essence_authority_granted": False,
        "teni_authority_granted": False,
    }


if __name__ == "__main__":
    out = evaluate_two_truths(TwoTruthsClaim())
    print(json.dumps(out, ensure_ascii=False, indent=2, sort_keys=True))
