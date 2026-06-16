from __future__ import annotations
import pathlib
from runtime.kuuos_horizon_gauge_arbitration_paths_v0_12 import paths as arbitration_paths


def paths(root: pathlib.Path):
    packet = arbitration_paths(root)
    packet.update({
        "atlas_state": root / "kuuos_context_gauge_atlas_state_v0_13.json",
        "atlas_bundle": root / "kuuos_context_gauge_atlas_bundle_v0_13.json",
        "atlas_decision": root / "kuuos_context_gauge_atlas_decision_v0_13.json",
        "atlas_outcome": root / "kuuos_context_gauge_atlas_outcome_v0_13.json",
        "atlas_child_plan": root / "kuuos_context_gauge_atlas_child_plan_v0_13.json",
        "atlas_child_license": root / "kuuos_context_gauge_atlas_child_license_v0_13.json",
        "atlas_receipt": root / "kuuos_context_gauge_atlas_receipt_v0_13.json",
        "atlas_ledger": root / "kuuos_context_gauge_atlas_ledger_v0_13.jsonl",
        "atlas_audit": root / "kuuos_context_gauge_atlas_audit_v0_13.jsonl",
    })
    return packet
