#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import pathlib
import sys
import tempfile
from typing import Any, Mapping

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_indra_qi_world_self_adjoint_lean_receipt_bridge_core_v0_28 import *


def save(path: pathlib.Path, value: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(dict(value), ensure_ascii=False, sort_keys=True), encoding="utf-8")


def source_v026() -> dict[str, Any]:
    state = {
        "version": SOURCE_V026_VERSION,
        "world_model_id": "world-example",
        "carrier": {"scalar_field": "real", "space_kind": "ell2_countable_real", "complete_real_hilbert_space_declared": True},
        "representation_boundary": {"world_not_identified_with_hilbert_vector": True, "multi_world_noncollapse_preserved": True, "two_truths_gap_preserved": True},
        "operator_template": {"generator_kind": "positive_diagonal_dense_core_template", "dense_core_declared": True, "symmetric_core_declared": True, "self_adjointness_status": "not_asserted_by_runtime", "unbounded_operator_execution_enabled": False},
        "analytic_observables": {"coercivity_lower_bound": 1.0, "rayleigh_lower_bound_verified": True},
        "decision": "world_l2_analytic_spine_ready",
    }
    state["world_l2_spine_state_digest"] = digest(state)
    return state


def source_v027(v026: Mapping[str, Any]) -> dict[str, Any]:
    state = {
        "version": SOURCE_V027_VERSION,
        "world_model_id": v026["world_model_id"],
        "source_state_digest": v026["world_l2_spine_state_digest"],
        "formal_module_sha256": "d" * 64,
        "runtime_concrete_proof_claimed": False,
        "operator_executed": False,
        "decision": "world_dense_operator_proof_bridge_ready",
        "realization_status": "formal_realization_obligation_bound_not_runtime_proved",
    }
    state["proof_bridge_state_digest"] = digest(state)
    return state


def packet(root: pathlib.Path, *, omit_stage: str | None = None, build_status: str = "success", bad_commit: bool = False):
    v026 = source_v026()
    v027 = source_v027(v026)
    save(root / "indra_qi_world_real_hilbert_l2_analytic_spine_state_v0_26.json", v026)
    save(root / "indra_qi_world_dense_operator_proof_bridge_state_v0_27.json", v027)
    formal_source = (ROOT / FORMAL_MODULE).read_text(encoding="utf-8")
    formal_path = root / FORMAL_MODULE
    formal_path.parent.mkdir(parents=True, exist_ok=True)
    formal_path.write_text(formal_source, encoding="utf-8")
    module_sha = hashlib.sha256(formal_path.read_bytes()).hexdigest()
    plan = {
        "version": PLAN_VERSION,
        "bridge_id": "self-adjoint-bridge",
        "proof_run_id": f"proof-{omit_stage or build_status}{'-bad' if bad_commit else ''}",
        "world_model_id": "world-example",
        "expected_v027_bridge_state_digest": v027["proof_bridge_state_digest"],
        "expected_v026_analytic_state_digest": v026["world_l2_spine_state_digest"],
        "expected_formal_module_sha256": module_sha,
        "canonical_repository": CANONICAL_REPOSITORY,
        "required_proof_stages": sorted(REQUIRED_STAGES),
        "minimum_rayleigh_lower_bound": 1.0,
        "boundary": dict(REQUIRED_BOUNDARY),
    }
    plan["self_adjoint_bridge_plan_digest"] = plan_digest(plan)
    source = validate_sources(root, plan, [])
    declarations = {
        "dense_linear_pmap": "concreteL2R2DenseDiagonalDomainLinearPMap",
        "graph_adjoint_fixed_point": "concrete_l2_r2_dense_diagonal_domain_linear_pmap_graph_adjoint_eq_graph",
        "actual_adjoint_eq_self": "concrete_l2_r2_dense_diagonal_domain_linear_pmap_actual_adjoint_eq_self",
        "mathlib_is_self_adjoint": "concrete_l2_r2_dense_diagonal_domain_linear_pmap_isSelfAdjoint",
        "global_rayleigh_lower_bound": "concrete_l2_r2_self_adjoint_diagonal_global_rayleigh_lower_edge_one",
    }
    stages = [
        {"stage_id": stage, "status": "proved", "declaration": declarations[stage], "source_file_sha256": digest({"stage": stage})}
        for stage in sorted(REQUIRED_STAGES) if stage != omit_stage
    ]
    proof = {
        "version": PROOF_VERSION,
        "canonical_repository": CANONICAL_REPOSITORY,
        "canonical_commit": "main" if bad_commit else "0" * 40,
        "lean_version": "4.x",
        "mathlib_revision": "immutable-mathlib-revision",
        "workflow_name": "Lean Fast Check",
        "workflow_run_id": "example-run",
        "build_status": build_status,
        "source_v027_bridge_state_digest": source["v027"],
        "source_v026_analytic_state_digest": source["v026"],
        "dense_operator_identity_digest": source["identity"],
        "bridge_schema_sha256": module_sha,
        "proof_stages": stages,
        "theorem_bundle": {
            "energy_lower_bound_theorem": "concrete_l2_r2_actual_energy_ge_norm_sq",
            "self_adjoint_theorem": "concrete_l2_r2_dense_diagonal_domain_linear_pmap_isSelfAdjoint",
            "global_rayleigh_theorem": "concrete_l2_r2_self_adjoint_diagonal_global_rayleigh_lower_edge_one",
            "rayleigh_lower_bound": 1.0,
            "actual_mathlib_is_self_adjoint": True,
            "whole_domain_rayleigh_lower_bound": True,
        },
        "source_audit": {"no_sorry": True, "no_admit": True, "no_axiom_placeholders": True, "no_unsafe_bridge": True},
        "runtime_self_adjointness_claimed": False,
        "unbounded_operator_execution_enabled": False,
    }
    proof["lean_proof_receipt_digest"] = proof_digest(proof)
    license_value = {
        "version": LICENSE_VERSION,
        "bound_plan_digest": plan["self_adjoint_bridge_plan_digest"],
        "bound_lean_proof_receipt_digest": proof["lean_proof_receipt_digest"],
        "bound_dense_operator_identity_digest": source["identity"],
        "bound_bridge_schema_sha256": module_sha,
        "state_write_allowed": True,
        "recommendation_write_allowed": True,
        "ledger_append_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
        "runtime_theorem_claim_authority_granted": False,
        "operator_execution_authority_granted": False,
        "world_update_authority_granted": False,
        "external_actuation_authority_granted": False,
        "truth_authority_granted": False,
    }
    context = {"runtime_root": str(root), "indra_qi_world_self_adjoint_lean_receipt_bridge_v0_28_enabled": True, "apply_indra_qi_world_self_adjoint_lean_receipt_bridge_v0_28": True}
    return context, plan, license_value, proof


def run_case(**kwargs):
    with tempfile.TemporaryDirectory() as directory:
        root = pathlib.Path(directory)
        context, plan, license_value, proof = packet(root, **kwargs)
        return build_world_self_adjoint_lean_receipt_bridge(runtime_context=context, self_adjoint_bridge_plan=plan, self_adjoint_bridge_license=license_value, lean_proof_receipt=proof)


def main() -> int:
    lean = (ROOT / FORMAL_MODULE).read_text(encoding="utf-8")
    for token in ("CanonicalSelfAdjointProofReceipt", "canonical_self_adjoint_claim", "source_global_rayleigh_bound_preserved", "runtime_self_adjoint_receipt_grants_no_authority"):
        assert token in lean
    ready = run_case()
    assert ready.status == READY and ready.decision == "world_self_adjoint_lean_receipt_bridge_ready"
    assert ready.proof_stage_count == len(REQUIRED_STAGES) and ready.rayleigh_lower_bound == 1.0
    awaiting = run_case(omit_stage="mathlib_is_self_adjoint")
    assert awaiting.status == READY and awaiting.decision == "awaiting_external_lean_proof"
    failed = run_case(build_status="failure")
    assert failed.status == READY and failed.decision == "awaiting_external_lean_proof"
    blocked = run_case(bad_commit=True)
    assert blocked.status == BLOCKED and "v028_proof_commit_not_immutable_hex40" in blocked.blockers
    manifest = json.loads((ROOT / "manifests/qi_world_self_adjoint_lean_receipt_bridge_v0_28.json").read_text())
    for group in ("runtime", "scripts", "docs", "formal", "example"):
        for relative in manifest[group]:
            assert (ROOT / relative).is_file(), relative
    print("qi_world_self_adjoint_lean_receipt_bridge_v0_28 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
