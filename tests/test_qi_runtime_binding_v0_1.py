from runtime.qi_runtime_binding_v0_1 import evaluate_qi_runtime_binding


BASE_STATE = {
    "cycle_id": "cycle-001",
    "kernel_state": "candidate",
    "candidate_only": True,
    "nonfinal_marker": True,
    "two_truths_gap": True,
    "noncollapse_guard": True,
    "memory_overwrite_blocker": True,
    "world_identity_blocker": True,
    "runtime_variation_visible": True,
    "policy_candidate_receipt": True,
    "value_witness_receipt": True,
    "barrier_witness_receipt": True,
    "receipt_hash": True,
    "support_refs": True,
    "registry_key": True,
    "view_delivery_receipt": True,
    "channel_scope": True,
    "acknowledgment_marker": True,
}


def test_allow_candidate_when_all_inputs_visible():
    receipt = evaluate_qi_runtime_binding(BASE_STATE)
    assert receipt.qi_signal == "ALLOW_CANDIDATE"
    assert receipt.grants_execution_authority is False
    assert receipt.grants_truth_authority is False
    assert receipt.grants_final_commitment_authority is False
    assert receipt.grants_memory_overwrite_authority is False


def test_boundary_failure_quarantines_before_policy_checks():
    state = dict(BASE_STATE)
    state["two_truths_gap"] = False
    state["runtime_variation_visible"] = False
    receipt = evaluate_qi_runtime_binding(state)
    assert receipt.qi_signal == "QUARANTINE"
    assert receipt.qi_reason == "boundary_first_noncollapse_failed"
    assert "two_truths_gap" in receipt.missing_inputs
    assert "quarantine_notice" in receipt.opened_notices


def test_forbidden_authority_projection_quarantines():
    state = dict(BASE_STATE)
    state["truth_commit"] = True
    receipt = evaluate_qi_runtime_binding(state)
    assert receipt.qi_signal == "QUARANTINE"
    assert receipt.qi_reason == "forbidden_authority_projection_present"
    assert "truth_commit" in receipt.blocked_boundaries


def test_missing_candidate_marker_holds():
    state = dict(BASE_STATE)
    state["nonfinal_marker"] = False
    receipt = evaluate_qi_runtime_binding(state)
    assert receipt.qi_signal == "HOLD"
    assert receipt.qi_reason == "candidate_or_nonfinal_marker_missing"
    assert "nonfinal_marker" in receipt.missing_inputs


def test_missing_policy_support_reobserve():
    state = dict(BASE_STATE)
    state["value_witness_receipt"] = False
    receipt = evaluate_qi_runtime_binding(state)
    assert receipt.qi_signal == "REOBSERVE"
    assert receipt.qi_reason == "runtime_policy_flow_support_missing"
    assert "value_witness_receipt" in receipt.missing_inputs


def test_missing_lineage_support_recheck():
    state = dict(BASE_STATE)
    state["registry_key"] = False
    receipt = evaluate_qi_runtime_binding(state)
    assert receipt.qi_signal == "LINEAGE_RECHECK"
    assert receipt.qi_reason == "lineage_flow_support_missing"
    assert "registry_key" in receipt.missing_inputs


def test_missing_delivery_support_recheck():
    state = dict(BASE_STATE)
    state["acknowledgment_marker"] = False
    receipt = evaluate_qi_runtime_binding(state)
    assert receipt.qi_signal == "DELIVERY_RECHECK"
    assert receipt.qi_reason == "projection_delivery_flow_support_missing"
    assert "acknowledgment_marker" in receipt.missing_inputs
