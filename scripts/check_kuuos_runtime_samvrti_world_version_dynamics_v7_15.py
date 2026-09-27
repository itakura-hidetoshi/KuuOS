#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import pathlib
import sys
import tempfile
from typing import Any

REPOSITORY_ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

from runtime.kuuos_runtime_samvrti_world_version_dynamics_v7_15 import (
    BLOCKED,
    CUMULATIVE_DRIFT,
    HISTORY_DISCONNECTED,
    OBSTRUCTED,
    READY,
    REVERSIBLE_LOCAL,
    STRUCTURAL_DRIFT,
    build_samvrti_world_version_dynamics,
)

PLAN = "samvrti_world_version_dynamics_plan_v7_15.json"
SOURCE = "samvrti_world_effect_update_packet_v7_14.json"
INPUT = "samvrti_world_version_diagnostics_input_v7_15.json"
OUTPUT = "samvrti_world_version_dynamics_packet_v7_15.json"


def sha(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    ).hexdigest()


def authority_packet() -> dict[str, Any]:
    return {
        "authority_status": "KUUOS_SAMVRTI_WORLD_VERSION_DYNAMICS_AUTHORITY_READY",
        "plan_read_allowed": True,
        "source_world_update_packet_read_allowed": True,
        "diagnostics_input_read_allowed": True,
        "output_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }


def ctx(root: pathlib.Path) -> dict[str, Any]:
    return {
        "runtime_root": str(root),
        "samvrti_world_version_dynamics_enabled": True,
        "apply_samvrti_world_version_dynamics": True,
    }


def world_version(
    version_id: str,
    *,
    prior: str,
    observed: str,
    paramartha: str = "paramartha-shared",
    world_id: str = "world-A",
) -> dict[str, Any]:
    return {
        "samvrti_world_version_id": version_id,
        "samvrti_world_transition_digest": sha(
            {
                "version_id": version_id,
                "prior": prior,
                "observed": observed,
                "paramartha": paramartha,
                "world_id": world_id,
            }
        ),
        "target_samvrti_world_id": world_id,
        "prior_world_state_digest": prior,
        "observed_world_state_digest": observed,
        "observed_effect_digest": sha({"version_id": version_id, "effect": True}),
        "independent_world_evidence_digest": sha(
            {"version_id": version_id, "evidence": True}
        ),
        "reconciliation_receipt_digest": sha(
            {"version_id": version_id, "reconciliation": True}
        ),
        "verify_state_digest": sha({"version_id": version_id, "verify": True}),
        "transaction_final_receipt_digest": sha(
            {"version_id": version_id, "final": True}
        ),
        "paramartha_carrier_element_id_before": paramartha,
        "paramartha_carrier_element_id_after": paramartha,
        "paramartha_class_changed": False,
        "world_transition_is_observed_conventional_record": True,
        "world_transition_is_ultimate_truth": False,
        "mission_success": "undetermined",
        "mission_success_implied": False,
    }


def source_packet(versions: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "version": "kuuos_runtime_samvrti_world_effect_update_v7_14",
        "status": "KUUOS_SAMVRTI_WORLD_EFFECT_UPDATE_READY",
        "source_lineage_packet_digest": "a" * 64,
        "samvrti_world_effect_records": [],
        "materialized_samvrti_world_versions": versions,
        "summary": {},
        "two_truths_effect_return_boundary": {
            "effect_confirmed_may_update_samvrti_world": True,
            "nonconfirmed_effect_may_fabricate_world_update": False,
            "world_update_may_change_paramartha_class": False,
            "paramartha_carrier_preserved_across_samvrti_transition": True,
            "effect_confirmed_implies_mission_success": False,
            "reconciliation_is_truth": False,
            "world_update_overwrites_history": False,
            "samvrti_world_versions_are_append_only": True,
            "observed_world_transition_is_conventional_not_ultimate": True,
            "compensation_proposal_is_not_world_rollback": True,
            "reobservation_residue_is_preserved": True,
            "source_authority_transferred": False,
        },
    }


def diagnostic(
    version_id: str,
    sequence_index: int,
    *,
    local_change: float = 0.2,
    reversibility: float = 0.9,
    recoverability: float = 0.9,
    impact: float = 0.2,
    axis: str = "axis-a",
    binding: str = "binding-a",
    structural: str = "context-a",
    rebind: bool = False,
) -> dict[str, Any]:
    return {
        "samvrti_world_version_id": version_id,
        "sequence_index": sequence_index,
        "local_change_score": local_change,
        "reversibility": reversibility,
        "recoverability": recoverability,
        "impact_radius": impact,
        "drift_axis_digest": sha(axis),
        "world_binding_signature_digest": sha(binding),
        "structural_context_digest": sha(structural),
        "binding_revalidation_requested": rebind,
        "diagnostic_receipt_digest": sha(
            {
                "version_id": version_id,
                "sequence_index": sequence_index,
                "axis": axis,
                "binding": binding,
                "structural": structural,
                "rebind": rebind,
            }
        ),
    }


def plan(source: dict[str, Any]) -> dict[str, Any]:
    return {
        "version": "kuuos_samvrti_world_version_dynamics_plan_v7_15",
        "source_world_update_packet_digest": sha(source),
        "read_only": True,
        "policy_thresholds_are_semantic_truth": False,
        "world_digest_change_alone_is_structural_drift": False,
        "structural_drift_changes_paramartha_class": False,
        "structural_drift_blocks_world_independent_action": False,
        "history_composition_required": True,
        "source_authority_transfer_allowed": False,
        "max_local_change_score": 0.35,
        "minimum_local_reversibility": 0.75,
        "minimum_local_recoverability": 0.75,
        "maximum_local_impact": 0.30,
        "cumulative_drift_score_threshold": 0.85,
        "repeated_axis_count_threshold": 3,
    }


def write_case(
    root: pathlib.Path,
    source: dict[str, Any],
    diagnostics: list[dict[str, Any]],
    *,
    override_plan: dict[str, Any] | None = None,
) -> None:
    (root / SOURCE).write_text(json.dumps(source), encoding="utf-8")
    (root / PLAN).write_text(
        json.dumps(override_plan or plan(source)),
        encoding="utf-8",
    )
    (root / INPUT).write_text(
        json.dumps(
            {
                "version": "kuuos_samvrti_world_version_diagnostics_input_v7_15",
                "source_world_update_packet_digest": sha(source),
                "diagnostics": diagnostics,
            }
        ),
        encoding="utf-8",
    )


def only_fiber(out: dict[str, Any]) -> dict[str, Any]:
    assert len(out["samvrti_dynamics_fibers"]) == 1
    return out["samvrti_dynamics_fibers"][0]


def test_continuous_small_reversible_history_is_local_dynamics() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        versions = [
            world_version("v1", prior="W0", observed="W1"),
            world_version("v2", prior="W1", observed="W2"),
        ]
        source = source_packet(versions)
        diagnostics = [
            diagnostic("v1", 0, axis="axis-a"),
            diagnostic("v2", 1, axis="axis-b"),
        ]
        write_case(root, source, diagnostics)

        result = build_samvrti_world_version_dynamics(
            runtime_context=ctx(root),
            authority_packet=authority_packet(),
        )
        assert result.status == READY, result.to_dict()
        assert result.reversible_local_fiber_count == 1

        out = json.loads((root / OUTPUT).read_text())
        fiber = only_fiber(out)
        assert fiber["samvrti_dynamics"] == REVERSIBLE_LOCAL
        assert fiber["history_chain_continuous"] is True
        assert fiber["initial_world_state_digest"] == "W0"
        assert fiber["latest_world_state_digest"] == "W2"
        assert fiber["world_dependent_binding_recheck_required"] is False
        assert fiber["world_independent_action_reuse_allowed"] is True
        assert fiber["paramartha_class_changed"] is False


def test_repeated_direction_accumulates_samvrti_drift_without_paramartha_change() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        versions = [
            world_version("v1", prior="W0", observed="W1"),
            world_version("v2", prior="W1", observed="W2"),
            world_version("v3", prior="W2", observed="W3"),
        ]
        source = source_packet(versions)
        diagnostics = [
            diagnostic("v1", 0, local_change=0.18, axis="same-axis"),
            diagnostic("v2", 1, local_change=0.18, axis="same-axis"),
            diagnostic("v3", 2, local_change=0.18, axis="same-axis"),
        ]
        write_case(root, source, diagnostics)

        result = build_samvrti_world_version_dynamics(
            runtime_context=ctx(root),
            authority_packet=authority_packet(),
        )
        assert result.status == READY, result.to_dict()
        assert result.cumulative_drift_fiber_count == 1

        out = json.loads((root / OUTPUT).read_text())
        fiber = only_fiber(out)
        assert fiber["samvrti_dynamics"] == CUMULATIVE_DRIFT
        assert fiber["maximum_repeated_drift_axis_run"] == 3
        assert fiber["distinct_world_binding_signature_count"] == 1
        assert fiber["distinct_structural_context_count"] == 1
        assert fiber["world_dependent_binding_recheck_required"] is False
        assert fiber["paramartha_reclassification_required"] is False


def test_binding_or_structural_change_is_structural_drift_not_paramartha_change() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        versions = [
            world_version("v1", prior="W0", observed="W1"),
            world_version("v2", prior="W1", observed="W2"),
        ]
        source = source_packet(versions)
        diagnostics = [
            diagnostic(
                "v1",
                0,
                binding="binding-old",
                structural="context-old",
            ),
            diagnostic(
                "v2",
                1,
                binding="binding-new",
                structural="context-new",
            ),
        ]
        write_case(root, source, diagnostics)

        result = build_samvrti_world_version_dynamics(
            runtime_context=ctx(root),
            authority_packet=authority_packet(),
        )
        assert result.status == READY, result.to_dict()
        assert result.structural_drift_fiber_count == 1

        out = json.loads((root / OUTPUT).read_text())
        fiber = only_fiber(out)
        assert fiber["samvrti_dynamics"] == STRUCTURAL_DRIFT
        assert fiber["world_dependent_binding_recheck_required"] is True
        assert (
            fiber["existing_world_binding_status"]
            == "recheck_world_dependent_bindings"
        )
        assert fiber["world_independent_action_reuse_allowed"] is True
        assert fiber["paramartha_class_changed"] is False
        assert fiber["paramartha_reclassification_required"] is False


def test_world_state_digest_change_alone_does_not_mean_structural_drift() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        versions = [
            world_version("v1", prior="STATE-A", observed="STATE-B"),
            world_version("v2", prior="STATE-B", observed="STATE-C"),
        ]
        source = source_packet(versions)
        diagnostics = [
            diagnostic("v1", 0, axis="axis-a"),
            diagnostic("v2", 1, axis="axis-b"),
        ]
        write_case(root, source, diagnostics)

        result = build_samvrti_world_version_dynamics(
            runtime_context=ctx(root),
            authority_packet=authority_packet(),
        )
        assert result.status == READY

        out = json.loads((root / OUTPUT).read_text())
        fiber = only_fiber(out)
        assert fiber["samvrti_dynamics"] == REVERSIBLE_LOCAL
        assert out["dependent_origination_dynamics_boundary"][
            "world_digest_change_alone_is_structural_drift"
        ] is False


def test_disconnected_history_is_obstruction_and_not_fabricated() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        versions = [
            world_version("v1", prior="W0", observed="W1"),
            world_version("v2", prior="OTHER", observed="W2"),
        ]
        source = source_packet(versions)
        diagnostics = [
            diagnostic("v1", 0),
            diagnostic("v2", 1),
        ]
        write_case(root, source, diagnostics)

        result = build_samvrti_world_version_dynamics(
            runtime_context=ctx(root),
            authority_packet=authority_packet(),
        )
        assert result.status == OBSTRUCTED, result.to_dict()
        assert result.obstructed_fiber_count == 1

        out = json.loads((root / OUTPUT).read_text())
        fiber = only_fiber(out)
        assert fiber["samvrti_dynamics"] == HISTORY_DISCONNECTED
        assert fiber["history_chain_continuous"] is False
        assert any(
            error.startswith("world_history_chain_break:")
            for error in fiber["fiber_errors"]
        )
        assert out["dependent_origination_dynamics_boundary"][
            "history_discontinuity_is_not_filled_by_fabrication"
        ] is True


def test_explicit_rebind_request_is_structural_signal_not_global_action_block() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        versions = [
            world_version("v1", prior="W0", observed="W1"),
            world_version("v2", prior="W1", observed="W2"),
        ]
        source = source_packet(versions)
        diagnostics = [
            diagnostic("v1", 0),
            diagnostic("v2", 1, rebind=True),
        ]
        write_case(root, source, diagnostics)

        result = build_samvrti_world_version_dynamics(
            runtime_context=ctx(root),
            authority_packet=authority_packet(),
        )
        assert result.status == READY

        out = json.loads((root / OUTPUT).read_text())
        fiber = only_fiber(out)
        assert fiber["samvrti_dynamics"] == STRUCTURAL_DRIFT
        assert fiber["explicit_binding_revalidation_requested"] is True
        assert fiber["world_dependent_binding_recheck_required"] is True
        assert fiber["world_independent_action_reuse_allowed"] is True


def test_policy_thresholds_cannot_be_promoted_to_semantic_truth() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        versions = [world_version("v1", prior="W0", observed="W1")]
        source = source_packet(versions)
        p = plan(source)
        p["policy_thresholds_are_semantic_truth"] = True
        write_case(root, source, [diagnostic("v1", 0)], override_plan=p)

        result = build_samvrti_world_version_dynamics(
            runtime_context=ctx(root),
            authority_packet=authority_packet(),
        )
        assert result.status == BLOCKED, result.to_dict()
        assert "policy_thresholds_semantic_truth_must_be_false" in result.blockers
        assert not (root / OUTPUT).exists()


def main() -> int:
    test_continuous_small_reversible_history_is_local_dynamics()
    test_repeated_direction_accumulates_samvrti_drift_without_paramartha_change()
    test_binding_or_structural_change_is_structural_drift_not_paramartha_change()
    test_world_state_digest_change_alone_does_not_mean_structural_drift()
    test_disconnected_history_is_obstruction_and_not_fabricated()
    test_explicit_rebind_request_is_structural_signal_not_global_action_block()
    test_policy_thresholds_cannot_be_promoted_to_semantic_truth()
    print("PASS: KuuOS Samvrti World-Version Dynamics v7.15")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
