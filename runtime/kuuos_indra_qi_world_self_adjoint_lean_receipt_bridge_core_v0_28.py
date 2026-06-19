#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import math
import os
import pathlib
import re
import time
from typing import Any, Mapping

PLAN_VERSION = "indra_qi_world_self_adjoint_lean_receipt_bridge_plan_v0_28"
PROOF_VERSION = "mgap4d_world_self_adjoint_lean_proof_receipt_v0_28"
LICENSE_VERSION = "indra_qi_world_self_adjoint_lean_receipt_bridge_license_v0_28"
STATE_VERSION = "indra_qi_world_self_adjoint_lean_receipt_bridge_state_v0_28"
RECOMMENDATION_VERSION = "indra_qi_world_self_adjoint_lean_receipt_bridge_recommendation_v0_28"
LEDGER_VERSION = "indra_qi_world_self_adjoint_lean_receipt_bridge_ledger_record_v0_28"
VERSION = "indra_qi_world_self_adjoint_lean_receipt_bridge_v0_28"
READY = "INDRA_QI_WORLD_SELF_ADJOINT_LEAN_RECEIPT_BRIDGE_V0_28_READY"
BLOCKED = "INDRA_QI_WORLD_SELF_ADJOINT_LEAN_RECEIPT_BRIDGE_V0_28_BLOCKED"
SOURCE_V027_VERSION = "indra_qi_world_dense_operator_proof_bridge_state_v0_27"
SOURCE_V026_VERSION = "indra_qi_world_real_hilbert_l2_analytic_spine_state_v0_26"
FORMAL_MODULE = "formal/KUOS/WORLD/RealHilbertL2SelfAdjointProofReceiptBridgeV0_28.lean"
CANONICAL_REPOSITORY = "itakura-hidetoshi/4d-mass-gap"
REQUIRED_STAGES = {
    "dense_linear_pmap",
    "graph_adjoint_fixed_point",
    "actual_adjoint_eq_self",
    "mathlib_is_self_adjoint",
    "global_rayleigh_lower_bound",
}
REQUIRED_DECLARATIONS = {
    "dense_linear_pmap": "concreteL2R2DenseDiagonalDomainLinearPMap",
    "graph_adjoint_fixed_point": "concrete_l2_r2_dense_diagonal_domain_linear_pmap_graph_adjoint_eq_graph",
    "actual_adjoint_eq_self": "concrete_l2_r2_dense_diagonal_domain_linear_pmap_actual_adjoint_eq_self",
    "mathlib_is_self_adjoint": "concrete_l2_r2_dense_diagonal_domain_linear_pmap_isSelfAdjoint",
    "global_rayleigh_lower_bound": "concrete_l2_r2_self_adjoint_diagonal_global_rayleigh_lower_edge_one",
}
REQUIRED_THEOREM_BUNDLE = {
    "energy_lower_bound_theorem": "concrete_l2_r2_actual_energy_ge_norm_sq",
    "self_adjoint_theorem": "concrete_l2_r2_dense_diagonal_domain_linear_pmap_isSelfAdjoint",
    "global_rayleigh_theorem": "concrete_l2_r2_self_adjoint_diagonal_global_rayleigh_lower_edge_one",
}
REQUIRED_BOUNDARY = {
    "source_v0_27_bridge_exact": True,
    "source_v0_26_analytic_state_exact": True,
    "immutable_canonical_commit_required": True,
    "exact_declaration_binding_required": True,
    "lean_ci_success_required": True,
    "source_audit_attestation_required": True,
    "runtime_receipt_not_proof_term": True,
    "runtime_cannot_assert_self_adjointness": True,
    "runtime_cannot_execute_unbounded_operator": True,
    "world_not_identified_with_hilbert_vector": True,
    "multi_world_noncollapse_preserved": True,
    "two_truths_gap_preserved": True,
    "recommendation_only": True,
    "not_truth_authority": True,
    "not_world_update_authority": True,
    "not_operator_execution_authority": True,
    "not_mathematical_theorem_authority": True,
    "fail_closed_on_integrity_loss": True,
}
HEX40 = re.compile(r"^[0-9a-f]{40}$")
HEX64 = re.compile(r"^[0-9a-f]{64}$")


def M(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def L(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def number(value: Any, default: float = 0.0) -> float:
    return float(value) if not isinstance(value, bool) and isinstance(value, (int, float)) and math.isfinite(float(value)) else default


def digest(value: Any) -> str:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def without(value: Mapping[str, Any], field: str) -> dict[str, Any]:
    out = dict(value)
    out.pop(field, None)
    return out


def valid_digest(value: Mapping[str, Any], field: str) -> bool:
    return bool(value.get(field)) and value.get(field) == digest(without(value, field))


def plan_digest(value: Mapping[str, Any]) -> str:
    return digest(without(value, "self_adjoint_bridge_plan_digest"))


def proof_digest(value: Mapping[str, Any]) -> str:
    return digest(without(value, "lean_proof_receipt_digest"))


def state_digest(value: Mapping[str, Any]) -> str:
    return digest(without(value, "self_adjoint_bridge_state_digest"))


def read(path: pathlib.Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return dict(value) if isinstance(value, Mapping) else {}


def read_jsonl(path: pathlib.Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        try:
            value = json.loads(line)
        except json.JSONDecodeError:
            value = {"_invalid": True}
        rows.append(dict(value) if isinstance(value, Mapping) else {"_invalid": True})
    return rows


def write(path: pathlib.Path, value: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(dict(value), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(tmp, path)


def append(path: pathlib.Path, value: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(dict(value), ensure_ascii=False, sort_keys=True) + "\n")


def validate_plan(plan: Mapping[str, Any], blockers: list[str]) -> None:
    if plan.get("version") != PLAN_VERSION:
        blockers.append("v028_plan_version_invalid")
    if plan.get("self_adjoint_bridge_plan_digest") != plan_digest(plan):
        blockers.append("v028_plan_digest_invalid")
    for field in ("bridge_id", "proof_run_id", "world_model_id", "expected_v027_bridge_state_digest", "expected_v026_analytic_state_digest", "expected_formal_module_sha256"):
        if not str(plan.get(field, "")).strip():
            blockers.append(f"v028_plan_{field}_missing")
    if plan.get("canonical_repository") != CANONICAL_REPOSITORY:
        blockers.append("v028_canonical_repository_invalid")
    stages = L(plan.get("required_proof_stages"))
    if set(stages) != REQUIRED_STAGES or len(stages) != len(REQUIRED_STAGES):
        blockers.append("v028_required_proof_stages_invalid")
    if number(plan.get("minimum_rayleigh_lower_bound")) <= 0:
        blockers.append("v028_minimum_rayleigh_lower_bound_invalid")
    for field, expected in REQUIRED_BOUNDARY.items():
        if M(plan.get("boundary")).get(field) is not expected:
            blockers.append(f"v028_boundary_{field}_mismatch")


def validate_sources(root: pathlib.Path, plan: Mapping[str, Any], blockers: list[str]) -> dict[str, str]:
    v027 = read(root / "indra_qi_world_dense_operator_proof_bridge_state_v0_27.json")
    v026 = read(root / "indra_qi_world_real_hilbert_l2_analytic_spine_state_v0_26.json")
    if v027.get("version") != SOURCE_V027_VERSION or not valid_digest(v027, "proof_bridge_state_digest"):
        blockers.append("v028_source_v027_state_invalid")
    if v026.get("version") != SOURCE_V026_VERSION or not valid_digest(v026, "world_l2_spine_state_digest"):
        blockers.append("v028_source_v026_state_invalid")
    v027_sha = str(v027.get("proof_bridge_state_digest", ""))
    v026_sha = str(v026.get("world_l2_spine_state_digest", ""))
    if plan.get("expected_v027_bridge_state_digest") != v027_sha:
        blockers.append("v028_expected_v027_state_digest_mismatch")
    if plan.get("expected_v026_analytic_state_digest") != v026_sha:
        blockers.append("v028_expected_v026_state_digest_mismatch")
    if v027.get("source_state_digest") != v026_sha:
        blockers.append("v028_v027_to_v026_chain_mismatch")
    if v027.get("decision") != "world_dense_operator_proof_bridge_ready" or v027.get("realization_status") != "formal_realization_obligation_bound_not_runtime_proved":
        blockers.append("v028_source_v027_not_ready")
    if v027.get("runtime_concrete_proof_claimed") is not False or v027.get("operator_executed") is not False:
        blockers.append("v028_source_v027_authority_boundary_invalid")
    if v027.get("world_model_id") != plan.get("world_model_id") or v026.get("world_model_id") != plan.get("world_model_id"):
        blockers.append("v028_world_model_id_mismatch")
    carrier, operator = M(v026.get("carrier")), M(v026.get("operator_template"))
    representation, observables = M(v026.get("representation_boundary")), M(v026.get("analytic_observables"))
    if not (carrier.get("scalar_field") == "real" and carrier.get("space_kind") == "ell2_countable_real" and carrier.get("complete_real_hilbert_space_declared") is True):
        blockers.append("v028_source_real_hilbert_carrier_invalid")
    if not (operator.get("generator_kind") == "positive_diagonal_dense_core_template" and operator.get("dense_core_declared") is True and operator.get("symmetric_core_declared") is True and operator.get("self_adjointness_status") == "not_asserted_by_runtime" and operator.get("unbounded_operator_execution_enabled") is False):
        blockers.append("v028_source_operator_template_invalid")
    if not (representation.get("world_not_identified_with_hilbert_vector") is True and representation.get("multi_world_noncollapse_preserved") is True and representation.get("two_truths_gap_preserved") is True):
        blockers.append("v028_source_representation_boundary_invalid")
    if number(observables.get("coercivity_lower_bound")) <= 0 or observables.get("rayleigh_lower_bound_verified") is not True:
        blockers.append("v028_source_rayleigh_gate_invalid")
    identity = digest({
        "world_model_id": plan.get("world_model_id"),
        "v027": v027_sha,
        "v026": v026_sha,
        "formal_module_sha256": v027.get("formal_module_sha256"),
        "operator_template": operator,
    })
    return {"v027": v027_sha, "v026": v026_sha, "identity": identity}


def validate_formal_module(root: pathlib.Path, plan: Mapping[str, Any], blockers: list[str]) -> str:
    path = root / FORMAL_MODULE
    actual = hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else ""
    if not actual:
        blockers.append("v028_formal_module_missing")
    if plan.get("expected_formal_module_sha256") != actual:
        blockers.append("v028_formal_module_digest_mismatch")
    return actual


def validate_proof(proof: Mapping[str, Any], plan: Mapping[str, Any], source: Mapping[str, str], module_sha: str, blockers: list[str]) -> list[str]:
    gaps: list[str] = []
    if proof.get("version") != PROOF_VERSION or not valid_digest(proof, "lean_proof_receipt_digest"):
        blockers.append("v028_lean_proof_receipt_invalid")
    exact = {
        "canonical_repository": CANONICAL_REPOSITORY,
        "source_v027_bridge_state_digest": source["v027"],
        "source_v026_analytic_state_digest": source["v026"],
        "dense_operator_identity_digest": source["identity"],
        "bridge_schema_sha256": module_sha,
    }
    for field, expected in exact.items():
        if proof.get(field) != expected:
            blockers.append(f"v028_proof_{field}_mismatch")
    commit = str(proof.get("canonical_commit", ""))
    if not HEX40.fullmatch(commit):
        blockers.append("v028_proof_commit_not_immutable_hex40")
    for field in ("lean_version", "mathlib_revision", "workflow_name", "workflow_run_id"):
        if not str(proof.get(field, "")).strip():
            blockers.append(f"v028_proof_{field}_missing")
    stages = {str(M(row).get("stage_id", "")): M(row) for row in L(proof.get("proof_stages"))}
    if set(stages) != REQUIRED_STAGES:
        gaps.append("required_proof_stages_incomplete")
    for stage in REQUIRED_STAGES:
        row = stages.get(stage, {})
        if row.get("status") != "proved" or not HEX64.fullmatch(str(row.get("source_file_sha256", ""))):
            gaps.append(f"stage_{stage}_not_proved")
        if row and row.get("declaration") != REQUIRED_DECLARATIONS[stage]:
            blockers.append(f"v028_stage_{stage}_declaration_mismatch")
    bundle = M(proof.get("theorem_bundle"))
    for field, expected in REQUIRED_THEOREM_BUNDLE.items():
        if bundle.get(field) != expected:
            blockers.append(f"v028_theorem_bundle_{field}_mismatch")
    if bundle.get("actual_mathlib_is_self_adjoint") is not True:
        gaps.append("mathlib_is_self_adjoint_not_attested")
    if bundle.get("whole_domain_rayleigh_lower_bound") is not True:
        gaps.append("whole_domain_rayleigh_lower_bound_not_attested")
    lower = number(bundle.get("rayleigh_lower_bound"))
    if lower < number(plan.get("minimum_rayleigh_lower_bound")):
        gaps.append("rayleigh_lower_bound_insufficient")
    if proof.get("build_status") != "success":
        gaps.append("lean_ci_not_success")
    audit = M(proof.get("source_audit"))
    for field in ("no_sorry", "no_admit", "no_axiom_placeholders", "no_unsafe_bridge"):
        if audit.get(field) is not True:
            gaps.append(f"source_audit_{field}_failed")
    if proof.get("runtime_self_adjointness_claimed") is not False:
        blockers.append("v028_runtime_self_adjointness_claim_forbidden")
    if proof.get("unbounded_operator_execution_enabled") is not False:
        blockers.append("v028_unbounded_operator_execution_forbidden")
    return sorted(set(gaps))


@dataclass(frozen=True)
class Result:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    bridge_id: str
    proof_run_id: str
    world_model_id: str
    decision: str
    canonical_commit: str
    dense_operator_identity_digest: str
    proof_stage_count: int
    rayleigh_lower_bound: float
    self_adjoint_bridge_state_digest: str
    ledger_record_digest: str
    blockers: list[str]
    proof_gaps: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def build_world_self_adjoint_lean_receipt_bridge(*, runtime_context: Mapping[str, Any], self_adjoint_bridge_plan: Mapping[str, Any], self_adjoint_bridge_license: Mapping[str, Any], lean_proof_receipt: Mapping[str, Any]) -> Result:
    context, plan, license_value, proof = M(runtime_context), dict(M(self_adjoint_bridge_plan)), M(self_adjoint_bridge_license), dict(M(lean_proof_receipt))
    blockers: list[str] = []
    root_value = context.get("runtime_root")
    root = pathlib.Path(str(root_value)).expanduser().resolve() if root_value else pathlib.Path(".").resolve()
    if not root_value or root == pathlib.Path("/").resolve():
        blockers.append("runtime_root_invalid")
    if context.get("indra_qi_world_self_adjoint_lean_receipt_bridge_v0_28_enabled") is not True or context.get("apply_indra_qi_world_self_adjoint_lean_receipt_bridge_v0_28") is not True:
        blockers.append("v028_bridge_not_enabled")
    validate_plan(plan, blockers)
    source = validate_sources(root, plan, blockers)
    module_sha = validate_formal_module(root, plan, blockers)
    proof_gaps = validate_proof(proof, plan, source, module_sha, blockers)
    expected_license = {
        "version": LICENSE_VERSION,
        "bound_plan_digest": str(plan.get("self_adjoint_bridge_plan_digest", "")),
        "bound_lean_proof_receipt_digest": str(proof.get("lean_proof_receipt_digest", "")),
        "bound_dense_operator_identity_digest": source["identity"],
        "bound_bridge_schema_sha256": module_sha,
    }
    for field, expected in expected_license.items():
        if license_value.get(field) != expected:
            blockers.append(f"v028_license_{field}_mismatch")
    for field in ("state_write_allowed", "recommendation_write_allowed", "ledger_append_allowed", "receipt_write_allowed", "audit_append_allowed"):
        if license_value.get(field) is not True:
            blockers.append(f"v028_license_{field}_not_true")
    for field in ("runtime_theorem_claim_authority_granted", "operator_execution_authority_granted", "world_update_authority_granted", "external_actuation_authority_granted", "truth_authority_granted"):
        if license_value.get(field) is not False:
            blockers.append(f"v028_license_{field}_not_false")
    ledger_path = root / "indra_qi_world_self_adjoint_lean_receipt_bridge_ledger_v0_28.jsonl"
    prior = read_jsonl(ledger_path)
    previous = "GENESIS"
    for index, row in enumerate(prior):
        if row.get("_invalid") or row.get("version") != LEDGER_VERSION or not valid_digest(row, "record_digest") or row.get("prev_record_digest") != previous:
            blockers.append(f"v028_ledger_record_{index}_invalid")
        previous = str(row.get("record_digest", ""))
    run_id = str(plan.get("proof_run_id", ""))
    if any(row.get("proof_run_id") == run_id or row.get("lean_proof_receipt_digest") == proof.get("lean_proof_receipt_digest") for row in prior):
        blockers.append("v028_replay_detected")
    decision = "quarantine_recommended" if blockers else ("awaiting_external_lean_proof" if proof_gaps else "world_self_adjoint_lean_receipt_bridge_ready")
    now = int(time.time())
    common = {
        "bridge_id": str(plan.get("bridge_id", "")),
        "proof_run_id": run_id,
        "world_model_id": str(plan.get("world_model_id", "")),
        "source_v027_bridge_state_digest": source["v027"],
        "source_v026_analytic_state_digest": source["v026"],
        "dense_operator_identity_digest": source["identity"],
        "formal_module_path": FORMAL_MODULE,
        "formal_module_sha256": module_sha,
        "canonical_repository": CANONICAL_REPOSITORY,
        "canonical_commit": str(proof.get("canonical_commit", "")),
        "lean_proof_receipt_digest": str(proof.get("lean_proof_receipt_digest", "")),
        "proof_gaps": proof_gaps,
        "runtime_receipt_not_proof_term": True,
        "runtime_self_adjointness_claimed": False,
        "operator_executed": False,
        "world_updated": False,
        "external_actuation_performed": False,
        "recommendation_only": True,
    }
    prior_state = read(root / "indra_qi_world_self_adjoint_lean_receipt_bridge_state_v0_28.json")
    if prior_state and not valid_digest(prior_state, "self_adjoint_bridge_state_digest"):
        blockers.append("v028_prior_state_invalid")
        decision = "quarantine_recommended"
    state = {"version": STATE_VERSION, **common, "decision": decision, "prev_self_adjoint_bridge_state_digest": str(prior_state.get("self_adjoint_bridge_state_digest", "GENESIS")) if prior_state else "GENESIS", "epoch": now}
    state["self_adjoint_bridge_state_digest"] = state_digest(state)
    recommendation = {"version": RECOMMENDATION_VERSION, **common, "decision": decision, "bridge_ready": decision == "world_self_adjoint_lean_receipt_bridge_ready", "epoch": now}
    recommendation["self_adjoint_bridge_recommendation_digest"] = digest(recommendation)
    ledger = {"version": LEDGER_VERSION, **common, "decision": decision, "self_adjoint_bridge_state_digest": state["self_adjoint_bridge_state_digest"], "prev_record_digest": str(prior[-1].get("record_digest", "GENESIS")) if prior else "GENESIS", "epoch": now}
    ledger["record_digest"] = digest(ledger)
    status = BLOCKED if blockers else READY
    receipt = {"version": VERSION, "status": status, **common, "decision": decision, "self_adjoint_bridge_state_digest": state["self_adjoint_bridge_state_digest"] if not blockers else "", "ledger_record_digest": ledger["record_digest"] if not blockers else "", "blockers": blockers, "epoch": now}
    receipt["packet_id"] = "indra-qi-world-self-adjoint-receipt-" + digest(receipt)[:16]
    if not blockers:
        write(root / "indra_qi_world_self_adjoint_lean_receipt_bridge_state_v0_28.json", state)
        write(root / "indra_qi_world_self_adjoint_lean_receipt_bridge_recommendation_v0_28.json", recommendation)
        append(ledger_path, ledger)
    if license_value.get("receipt_write_allowed") is True:
        write(root / "indra_qi_world_self_adjoint_lean_receipt_bridge_receipt_v0_28.json", receipt)
    if license_value.get("audit_append_allowed") is True:
        append(root / "indra_qi_world_self_adjoint_lean_receipt_bridge_audit_v0_28.jsonl", {**receipt, "audit_record_digest": digest(receipt)})
    return Result(VERSION, status, str(receipt["packet_id"]), str(root), common["bridge_id"], run_id, common["world_model_id"], decision, common["canonical_commit"], source["identity"], len(REQUIRED_STAGES) - sum(1 for gap in proof_gaps if gap.startswith("stage_")), number(M(proof.get("theorem_bundle")).get("rayleigh_lower_bound")), state["self_adjoint_bridge_state_digest"] if not blockers else "", ledger["record_digest"] if not blockers else "", blockers, proof_gaps)
