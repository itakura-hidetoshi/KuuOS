#!/usr/bin/env python3
from __future__ import annotations

import pathlib
import unittest

from scripts.select_impacted_checks import load_registry, select

ROOT = pathlib.Path(__file__).resolve().parents[1]
REGISTRY = load_registry(ROOT / "ci" / "check_registry.yaml")


def selected_ids(result: dict[str, object]) -> set[str]:
    checks = result["selected_checks"]
    assert isinstance(checks, list)
    return {str(item["id"]) for item in checks}


def governance_shard_ids(ids: set[str]) -> set[str]:
    return {check_id for check_id in ids if check_id.startswith("full-governance-")}


class CiAuditSelectorV01Tests(unittest.TestCase):
    def test_document_change_keeps_only_structural_gate(self) -> None:
        result = select(REGISTRY, ["docs/example.md"], None)
        self.assertFalse(result["full_audit_required"])
        self.assertEqual(selected_ids(result), {"workflow-integrity"})

    def test_runtime_change_selects_runtime_and_structural_gate(self) -> None:
        result = select(REGISTRY, ["runtime/example.py"], None)
        self.assertFalse(result["full_audit_required"])
        self.assertEqual(selected_ids(result), {"runtime-full", "workflow-integrity"})

    def test_core_spec_change_selects_core_and_structural_gate(self) -> None:
        result = select(REGISTRY, ["specs/example.yaml"], None)
        self.assertFalse(result["full_audit_required"])
        self.assertEqual(selected_ids(result), {"core-governance", "workflow-integrity"})

    def test_decision_change_uses_subsystem_check_instead_of_runtime_full(self) -> None:
        result = select(
            REGISTRY,
            ["runtime/v01_decision_os_relational_deliberation.py"],
            None,
        )
        self.assertFalse(result["full_audit_required"])
        self.assertEqual(selected_ids(result), {"decision-os", "workflow-integrity"})

    def test_formal_subsystem_change_keeps_lean_validation(self) -> None:
        result = select(REGISTRY, ["formal/KUOS/PlanOS/Model.lean"], None)
        self.assertFalse(result["full_audit_required"])
        self.assertEqual(
            selected_ids(result),
            {"lean-formal", "plan-os", "workflow-integrity"},
        )

    def assert_full_governance_shards(self, result: dict[str, object]) -> set[str]:
        ids = selected_ids(result)
        shards = governance_shard_ids(ids)
        self.assertEqual(shards, {f"full-governance-{index:02d}" for index in range(8)})
        self.assertNotIn("full-governance", ids)
        return ids

    def test_any_workflow_change_requires_full_audit(self) -> None:
        path = ".github/workflows/kuuos-v076.yml"
        result = select(REGISTRY, [path], None)
        self.assertTrue(result["full_audit_required"])
        self.assertIn(path, result["full_audit_trigger_paths"])
        self.assert_full_governance_shards(result)

    def test_unknown_path_fails_closed_to_full_audit(self) -> None:
        result = select(REGISTRY, ["new_surface/example.txt"], None)
        self.assertTrue(result["full_audit_required"])
        ids = self.assert_full_governance_shards(result)
        self.assertIn("workflow-integrity", ids)
        self.assertIn("runtime-full", ids)
        self.assertIn("lean-formal", ids)
        self.assertIn("decision-os", ids)
        self.assertIn("evidence-cycle", ids)
        self.assertIn("plan-os", ids)
        self.assertIn("governance-shard-tests", ids)
        self.assertNotIn("core-governance", ids)

    def test_known_but_unmapped_script_fails_closed(self) -> None:
        result = select(REGISTRY, ["scripts/unclassified_validator.py"], None)
        self.assertTrue(result["full_audit_required"])
        self.assertIn("scripts/unclassified_validator.py", result["unmapped_paths"])
        self.assert_full_governance_shards(result)

    def test_audit_control_change_requires_full_audit(self) -> None:
        result = select(REGISTRY, ["ci/check_registry.yaml"], None)
        self.assertTrue(result["full_audit_required"])
        self.assertIn("ci/check_registry.yaml", result["full_audit_trigger_paths"])
        self.assert_full_governance_shards(result)

    def test_diff_failure_requires_full_audit(self) -> None:
        result = select(REGISTRY, [], "synthetic diff failure")
        self.assertTrue(result["full_audit_required"])
        self.assert_full_governance_shards(result)


if __name__ == "__main__":
    unittest.main()
