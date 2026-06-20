#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_world_quantum_gradient_jko_entropy_production_core_v0_47 import (
    BLOCKED,
    READY,
    REQUIRED_BOUNDARY,
    REQUIRED_COMPONENTS,
    VERSION,
    build_world_quantum_gradient_jko_entropy_production,
    plan_digest,
)


def sha(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    formal = ROOT / "formal/KUOS/WORLD/QuantumGradientJKOEntropyProductionBridgeV0_47.lean"
    source = ROOT / "formal/KUOS/WORLD/QuantumGeodesicMirrorDescentFreeEnergyBridgeV0_46.lean"
    text = formal.read_text(encoding="utf-8")

    for token in (
        "WorldQuantumGradientJKOEntropyProductionBridge",
        "gradientFlowStep",
        "entropyProduction",
        "energyDissipation",
        "jkoProximalCost",
        "jkoOptimality",
        "equilibrium",
        "lyapunovGap",
        "freeEnergyDrop",
        "free_energy_nonincreasing",
        "free_energy_drop_nonnegative",
        "entropy_production_controlled_by_drop",
        "jko_step_is_minimal",
        "equilibrium_has_zero_entropy_production",
        "lyapunov_gap_nonnegative",
        "lyapunov_gap_nonincreasing",
        "free_energy_drop_gauge_invariant",
        "gradient_entropy_lyapunov_package",
        "analytic_gradient_flow_receipts_complete",
        "runtime_grants_no_gradient_flow_authority",
        "gradient_flow_representation_boundary_preserved",
    ):
        assert token in text, token

    plan = {
        "version": VERSION,
        "world_model_id": "world-v0-47-example",
        "source_v046_sha256": sha(source),
        "formal_module_sha256": sha(formal),
        "components": sorted(REQUIRED_COMPONENTS),
        "boundary": dict(REQUIRED_BOUNDARY),
        "gradient_flow_executed_by_runtime": False,
        "physical_entropy_production_computed_by_runtime": False,
        "jko_optimization_executed_by_runtime": False,
        "physical_equilibrium_declared_by_runtime": False,
        "truth_inferred_from_stationarity": False,
        "world_state_optimized_by_runtime": False,
        "world_updated": False,
    }
    plan["plan_digest"] = plan_digest(plan)
    ready = build_world_quantum_gradient_jko_entropy_production(plan)
    assert ready.status == READY
    assert ready.decision == "ready"
    assert ready.bridge_state_digest

    denied = dict(plan)
    denied["jko_optimization_executed_by_runtime"] = True
    denied["plan_digest"] = plan_digest(denied)
    blocked = build_world_quantum_gradient_jko_entropy_production(denied)
    assert blocked.status == BLOCKED
    assert "jko_optimization_executed_by_runtime_forbidden" in blocked.blockers

    denied_boundary = dict(plan)
    denied_boundary["boundary"] = dict(REQUIRED_BOUNDARY)
    denied_boundary["boundary"]["stationary_not_truth_authority"] = False
    denied_boundary["plan_digest"] = plan_digest(denied_boundary)
    blocked_boundary = build_world_quantum_gradient_jko_entropy_production(
        denied_boundary
    )
    assert blocked_boundary.status == BLOCKED
    assert "boundary_stationary_not_truth_authority_invalid" in blocked_boundary.blockers

    manifest = json.loads(
        (
            ROOT
            / "manifests/world_quantum_gradient_jko_entropy_production_v0_47.json"
        ).read_text(encoding="utf-8")
    )
    for values in manifest["files"].values():
        for relative in values:
            assert (ROOT / relative).is_file(), relative

    print("world_quantum_gradient_jko_entropy_production_v0_47 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
