#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_world_quantum_log_sobolev_contractivity_mixing_core_v0_48 import (
    BLOCKED,
    READY,
    REQUIRED_BOUNDARY,
    REQUIRED_COMPONENTS,
    VERSION,
    build_world_quantum_log_sobolev_contractivity_mixing,
    plan_digest,
)


def sha(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    formal = ROOT / "formal/KUOS/WORLD/QuantumLogSobolevContractivityMixingBridgeV0_48.lean"
    source = ROOT / "formal/KUOS/WORLD/QuantumGradientJKOEntropyProductionBridgeV0_47.lean"
    text = formal.read_text(encoding="utf-8")

    for token in (
        "WorldQuantumLogSobolevContractivityMixingBridge",
        "logSobolevRate",
        "logSobolevInequality",
        "contractionFactor",
        "oneStepRelativeEntropyContraction",
        "oneStepLyapunovContraction",
        "mixingDistance",
        "relativeEntropyToEquilibrium",
        "iteratedGradientFlow",
        "finite_log_sobolev_inequality",
        "relative_entropy_iterate_contracts",
        "lyapunov_iterate_contracts",
        "mixing_distance_iterate_bound",
        "relative_entropy_gauge_invariant",
        "log_sobolev_contractivity_package",
        "analytic_mixing_receipts_complete",
        "runtime_grants_no_mixing_authority",
        "mixing_representation_boundary_preserved",
    ):
        assert token in text, token

    plan = {
        "version": VERSION,
        "world_model_id": "world-v0-48-example",
        "source_v047_sha256": sha(source),
        "formal_module_sha256": sha(formal),
        "components": sorted(REQUIRED_COMPONENTS),
        "boundary": dict(REQUIRED_BOUNDARY),
        "physical_log_sobolev_constant_computed_by_runtime": False,
        "quantum_markov_semigroup_executed_by_runtime": False,
        "physical_mixing_declared_by_runtime": False,
        "ergodicity_inferred_from_finite_certificate": False,
        "worlds_collapsed_at_equilibrium": False,
        "world_state_optimized_by_runtime": False,
        "world_updated": False,
    }
    plan["plan_digest"] = plan_digest(plan)
    ready = build_world_quantum_log_sobolev_contractivity_mixing(plan)
    assert ready.status == READY
    assert ready.decision == "ready"
    assert ready.bridge_state_digest

    denied = dict(plan)
    denied["quantum_markov_semigroup_executed_by_runtime"] = True
    denied["plan_digest"] = plan_digest(denied)
    blocked = build_world_quantum_log_sobolev_contractivity_mixing(denied)
    assert blocked.status == BLOCKED
    assert "quantum_markov_semigroup_executed_by_runtime_forbidden" in blocked.blockers

    denied_boundary = dict(plan)
    denied_boundary["boundary"] = dict(REQUIRED_BOUNDARY)
    denied_boundary["boundary"]["finite_contraction_not_physical_mixing"] = False
    denied_boundary["plan_digest"] = plan_digest(denied_boundary)
    blocked_boundary = build_world_quantum_log_sobolev_contractivity_mixing(
        denied_boundary
    )
    assert blocked_boundary.status == BLOCKED
    assert "boundary_finite_contraction_not_physical_mixing_invalid" in blocked_boundary.blockers

    manifest = json.loads(
        (
            ROOT
            / "manifests/world_quantum_log_sobolev_contractivity_mixing_v0_48.json"
        ).read_text(encoding="utf-8")
    )
    for values in manifest["files"].values():
        for relative in values:
            assert (ROOT / relative).is_file(), relative

    print("world_quantum_log_sobolev_contractivity_mixing_v0_48 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
