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

from runtime.kuuos_runtime_middle_way_action_lifting_v7_12 import (
    BOUNDED_PROBE,
    EXECUTE_EXACT,
    EXECUTE_TRANSFERRED,
    EXECUTE_WORLD_INDEPENDENT,
    FRESH_AUTHORITY_REQUIRED,
    PARTIAL,
    READY,
    REPLAN_REQUIRED,
    build_middle_way_action_lifting,
)

PLAN = "middle_way_action_lifting_plan_v7_12.json"
SOURCE = "two_truths_noncollapse_packet_v7_11.json"
INPUT = "middle_way_action_candidates_input_v7_12.json"
OUTPUT = "middle_way_action_lifting_packet_v7_12.json"


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
        "authority_status": "KUUOS_MIDDLE_WAY_ACTION_LIFTING_AUTHORITY_READY",
        "plan_read_allowed": True,
        "source_two_truths_packet_read_allowed": True,
        "action_candidates_read_allowed": True,
        "output_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }


def ctx(root: pathlib.Path) -> dict[str, Any]:
    return {
        "runtime_root": str(root),
        "middle_way_action_lifting_enabled": True,
        "apply_middle_way_action_lifting": True,
    }


def source_packet() -> dict[str, Any]:
    return {
        "version": "kuuos_runtime_two_truths_noncollapse_v7_11",
        "status": "KUUOS_TWO_TRUTHS_NONCOLLAPSE_READY",
        "source_choice_packet_digest": "a" * 64,
        "semantic_subjects": [
            {
                "semantic_subject_id": "subject-A",
                "paramartha_state": "paramartha_equivalence_available",
                "paramartha_carrier_element_id": "paramartha-shared",
                "samvrti_world_id": "world-A",
                "samvrti_state": "observed",
                "samvrti_operational_signature": "1" * 64,
                "lineage_digest": "a" * 64,
                "paramartha_equivalence_erases_samvrti_world": False,
                "samvrti_world_is_ultimate_substance": False,
            },
            {
                "semantic_subject_id": "subject-B",
                "paramartha_state": "paramartha_equivalence_available",
                "paramartha_carrier_element_id": "paramartha-shared",
                "samvrti_world_id": "world-B",
                "samvrti_state": "observed",
                "samvrti_operational_signature": "2" * 64,
                "lineage_digest": "b" * 64,
                "paramartha_equivalence_erases_samvrti_world": False,
                "samvrti_world_is_ultimate_substance": False,
            },
            {
                "semantic_subject_id": "subject-C",
                "paramartha_state": "paramartha_equivalence_available",
                "paramartha_carrier_element_id": "paramartha-shared",
                "samvrti_world_id": "",
                "samvrti_state": "held",
                "samvrti_operational_signature": "",
                "lineage_digest": "",
                "paramartha_equivalence_erases_samvrti_world": False,
                "samvrti_world_is_ultimate_substance": False,
            },
        ],
        "two_truths_relations": [],
        "summary": {},
        "two_truths_boundary": {
            "paramartha_and_samvrti_are_separate_surfaces": True,
            "paramartha_equivalence_may_erase_samvrti_difference": False,
            "same_paramartha_does_not_imply_conventional_substitutability": True,
            "samvrti_difference_is_error": False,
            "samvrti_difference_can_be_operationally_required": True,
            "conventional_substitution_requires_samvrti_equivalence": True,
            "nihilistic_collapse_into_paramartha_allowed": False,
            "reification_of_samvrti_allowed": False,
            "paramartha_carrier_is_ultimate_substance": False,
            "samvrti_world_is_ultimate_substance": False,
            "world_id_defines_paramartha_identity": False,
            "raw_conventional_operational_values_persisted": False,
            "source_authority_transferred": False,
        },
    }


def plan(source: dict[str, Any]) -> dict[str, Any]:
    return {
        "version": "kuuos_middle_way_action_lifting_plan_v7_12",
        "source_two_truths_packet_digest": sha(source),
        "read_only": True,
        "direct_execution_request_is_block_reason": False,
        "paramartha_only_action_is_automatically_blocked": False,
        "world_binding_mismatch_is_automatically_blocked": False,
        "fresh_external_authority_required_for_effect": True,
        "runtime_assessment_executes_action": False,
        "maximum_execution_risk": 0.50,
        "minimum_execution_reversibility": 0.40,
        "minimum_execution_recoverability": 0.50,
        "maximum_execution_impact": 0.50,
        "probe_maximum_risk": 0.25,
        "probe_minimum_reversibility": 0.80,
        "probe_minimum_recoverability": 0.80,
        "probe_maximum_impact": 0.20,
        "noncompensable_maximum_impact": 0.10,
    }


def auth(
    *,
    state: str = "valid",
    worlds: list[str] | None = None,
    action_classes: list[str] | None = None,
    fresh: bool = True,
    probe: bool = False,
) -> dict[str, Any]:
    return {
        "state": state,
        "fresh": fresh,
        "authorization_digest": "c" * 64 if state == "valid" else "",
        "capability_lease_digest": "d" * 64 if state == "valid" else "",
        "authorized_world_ids": worlds or [],
        "authorized_action_classes": action_classes or [],
        "probe_authorized": probe,
    }


def action(
    action_id: str,
    subject_id: str,
    *,
    target_world: str = "",
    direct: bool = True,
    action_class: str = "local_action",
    effect_mode: str = "reversible_effect",
    world_dependence: str = "contextual",
    invariant_across_worlds: bool = False,
    transfer_mode: str = "none",
    transfer_witness: str = "",
    risk: float = 0.20,
    reversibility: float = 0.90,
    recoverability: float = 0.90,
    impact: float = 0.20,
    human_review: bool = False,
    prohibited: bool = False,
    authority: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "action_id": action_id,
        "semantic_subject_id": subject_id,
        "direct_execution_requested": direct,
        "action_class": action_class,
        "effect_mode": effect_mode,
        "target_samvrti_world_id": target_world,
        "world_dependence": world_dependence,
        "action_invariant_across_samvrti": invariant_across_worlds,
        "transfer_mode": transfer_mode,
        "transfer_witness_digest": transfer_witness,
        "estimated_risk": risk,
        "reversibility": reversibility,
        "recoverability": recoverability,
        "impact_radius": impact,
        "requires_human_review": human_review,
        "explicitly_prohibited": prohibited,
        "required_evidence_digests": ["e" * 64],
        "available_evidence_digests": ["e" * 64],
        "authority": authority or auth(),
    }


def packet(source: dict[str, Any], actions: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "version": "kuuos_middle_way_action_candidates_input_v7_12",
        "source_two_truths_packet_digest": sha(source),
        "actions": actions,
    }


def write_case(
    root: pathlib.Path,
    source: dict[str, Any],
    actions: list[dict[str, Any]],
) -> None:
    (root / SOURCE).write_text(json.dumps(source), encoding="utf-8")
    (root / PLAN).write_text(json.dumps(plan(source)), encoding="utf-8")
    (root / INPUT).write_text(
        json.dumps(packet(source, actions)),
        encoding="utf-8",
    )


def by_id(out: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        item["action_id"]: item
        for item in out["action_assessments"]
    }


def test_exact_world_direct_execution_is_candidate_not_blocked() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        source = source_packet()
        actions = [
            action(
                "exact",
                "subject-A",
                target_world="world-A",
                authority=auth(
                    worlds=["world-A"],
                    action_classes=["local_action"],
                ),
            )
        ]
        write_case(root, source, actions)
        result = build_middle_way_action_lifting(
            runtime_context=ctx(root),
            authority_packet=authority_packet(),
        )
        assert result.status == READY, result.to_dict()
        out = json.loads((root / OUTPUT).read_text())
        a = by_id(out)["exact"]
        assert a["action_route"] == EXECUTE_EXACT
        assert a["direct_execution_requested"] is True
        assert a["direct_execution_request_was_not_used_as_block_reason"] is True
        assert a["execution_candidate"] is True


def test_certified_cross_world_transfer_can_execute() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        source = source_packet()
        actions = [
            action(
                "transfer",
                "subject-A",
                target_world="world-B",
                transfer_mode="certified",
                transfer_witness="f" * 64,
                authority=auth(
                    worlds=["world-B"],
                    action_classes=["local_action"],
                ),
            )
        ]
        write_case(root, source, actions)
        result = build_middle_way_action_lifting(
            runtime_context=ctx(root),
            authority_packet=authority_packet(),
        )
        assert result.status == READY, result.to_dict()
        out = json.loads((root / OUTPUT).read_text())
        a = by_id(out)["transfer"]
        assert a["action_route"] == EXECUTE_TRANSFERRED
        assert a["world_relation"] == "transferred_world"
        assert a["execution_candidate"] is True


def test_world_mismatch_can_be_bounded_probe_not_block() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        source = source_packet()
        actions = [
            action(
                "probe",
                "subject-A",
                target_world="world-B",
                transfer_mode="bounded_probe",
                risk=0.10,
                reversibility=0.95,
                recoverability=0.95,
                impact=0.10,
                authority=auth(
                    worlds=["world-B"],
                    action_classes=["local_action"],
                    probe=True,
                ),
            )
        ]
        write_case(root, source, actions)
        result = build_middle_way_action_lifting(
            runtime_context=ctx(root),
            authority_packet=authority_packet(),
        )
        assert result.status == READY, result.to_dict()
        out = json.loads((root / OUTPUT).read_text())
        a = by_id(out)["probe"]
        assert a["action_route"] == BOUNDED_PROBE
        assert a["world_relation"] == "world_mismatch"
        assert a["world_mismatch_was_not_used_as_automatic_block_reason"] is True


def test_paramartha_only_world_independent_action_can_execute() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        source = source_packet()
        actions = [
            action(
                "paramartha-only",
                "subject-C",
                action_class="read_metadata",
                effect_mode="read_only",
                world_dependence="none",
                impact=0.0,
                authority=auth(
                    worlds=["WORLD_INDEPENDENT"],
                    action_classes=["read_metadata"],
                ),
            )
        ]
        write_case(root, source, actions)
        result = build_middle_way_action_lifting(
            runtime_context=ctx(root),
            authority_packet=authority_packet(),
        )
        assert result.status == READY, result.to_dict()
        out = json.loads((root / OUTPUT).read_text())
        a = by_id(out)["paramartha-only"]
        assert a["action_route"] == EXECUTE_WORLD_INDEPENDENT
        assert a["paramartha_only_was_not_used_as_automatic_block_reason"] is True
        assert a["execution_candidate"] is True


def test_direct_execution_without_authority_requests_fresh_authority_not_reject() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        source = source_packet()
        actions = [
            action(
                "needs-license",
                "subject-B",
                target_world="world-B",
                authority=auth(
                    state="absent",
                    worlds=[],
                    action_classes=[],
                ),
            )
        ]
        write_case(root, source, actions)
        result = build_middle_way_action_lifting(
            runtime_context=ctx(root),
            authority_packet=authority_packet(),
        )
        assert result.status == PARTIAL, result.to_dict()
        out = json.loads((root / OUTPUT).read_text())
        a = by_id(out)["needs-license"]
        assert a["action_route"] == FRESH_AUTHORITY_REQUIRED
        assert a["direct_execution_requested"] is True
        assert a["action_route"] != "explicitly_prohibited"


def test_high_impact_irreversible_action_is_replan_not_blanket_direct_block() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        source = source_packet()
        actions = [
            action(
                "high-impact",
                "subject-A",
                target_world="world-A",
                effect_mode="noncompensable_effect",
                risk=0.60,
                reversibility=0.10,
                recoverability=0.20,
                impact=0.90,
                authority=auth(
                    worlds=["world-A"],
                    action_classes=["local_action"],
                ),
            )
        ]
        write_case(root, source, actions)
        result = build_middle_way_action_lifting(
            runtime_context=ctx(root),
            authority_packet=authority_packet(),
        )
        assert result.status == PARTIAL, result.to_dict()
        out = json.loads((root / OUTPUT).read_text())
        a = by_id(out)["high-impact"]
        assert a["action_route"] == REPLAN_REQUIRED
        assert "execution_risk_above_threshold" in a["reasons"]
        assert a["direct_execution_request_was_not_used_as_block_reason"] is True


def test_action_invariance_can_support_cross_world_lifting() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        source = source_packet()
        actions = [
            action(
                "invariant-transfer",
                "subject-A",
                target_world="world-B",
                invariant_across_worlds=True,
                transfer_mode="action_invariant",
                authority=auth(
                    worlds=["world-B"],
                    action_classes=["local_action"],
                ),
            )
        ]
        write_case(root, source, actions)
        result = build_middle_way_action_lifting(
            runtime_context=ctx(root),
            authority_packet=authority_packet(),
        )
        assert result.status == READY, result.to_dict()
        out = json.loads((root / OUTPUT).read_text())
        a = by_id(out)["invariant-transfer"]
        assert a["action_route"] == EXECUTE_TRANSFERRED
        assert a["world_relation"] == "transferred_world"


def main() -> int:
    test_exact_world_direct_execution_is_candidate_not_blocked()
    test_certified_cross_world_transfer_can_execute()
    test_world_mismatch_can_be_bounded_probe_not_block()
    test_paramartha_only_world_independent_action_can_execute()
    test_direct_execution_without_authority_requests_fresh_authority_not_reject()
    test_high_impact_irreversible_action_is_replan_not_blanket_direct_block()
    test_action_invariance_can_support_cross_world_lifting()
    print("PASS: KuuOS Middle-Way Action Lifting v7.12")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
