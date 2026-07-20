from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from pathlib import Path
import unittest

import runtime.kuuos_codeai_typed_structured_edit_ir_v0_1 as m

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "examples" / "codeai_typed_structured_edit_ir_v0_1.json"


def load_example() -> dict:
    return json.loads(EXAMPLE.read_text(encoding="utf-8"))


def reseal(value: dict, field: str) -> dict:
    value.pop(field, None)
    return m.seal(value, field)


class CodeAITypedStructuredEditIRV01Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.data = load_example()

    def build(self):
        return m.build_codeai_typed_structured_edit_ir(
            context_pack=self.data["context_pack"],
            context_receipt=self.data["context_receipt"],
            repository_files=self.data["repository_files"],
            typed_edit_proposal=self.data["typed_edit_proposal"],
            typed_edit_policy=self.data["typed_edit_policy"],
        )

    def reseal_proposal(self) -> None:
        self.data["typed_edit_proposal"] = reseal(
            self.data["typed_edit_proposal"], m.PROPOSAL_DIGEST_FIELD
        )

    def reseal_policy(self) -> None:
        self.data["typed_edit_policy"] = reseal(
            self.data["typed_edit_policy"], m.POLICY_DIGEST_FIELD
        )

    def reseal_context_chain(self) -> None:
        self.data["context_pack"] = reseal(
            self.data["context_pack"], m.CONTEXT_PACK_DIGEST_FIELD
        )
        receipt = self.data["context_receipt"]
        receipt["context_pack_digest"] = self.data["context_pack"][
            m.CONTEXT_PACK_DIGEST_FIELD
        ]
        self.data["context_receipt"] = reseal(
            receipt, m.CONTEXT_RECEIPT_DIGEST_FIELD
        )
        proposal = self.data["typed_edit_proposal"]
        proposal["expected_context_pack_digest"] = self.data["context_pack"][
            m.CONTEXT_PACK_DIGEST_FIELD
        ]
        proposal["expected_context_receipt_digest"] = self.data["context_receipt"][
            m.CONTEXT_RECEIPT_DIGEST_FIELD
        ]
        self.reseal_proposal()

    def test_example_is_exact_and_ready(self) -> None:
        result = self.build()
        self.assertEqual(result.status, m.STATUS_READY)
        self.assertEqual(result.issues, ())
        self.assertEqual(result.typed_edit_ir, self.data["expected_typed_edit_ir"])
        self.assertEqual(result.receipt, self.data["expected_receipt"])

    def test_deterministic_rebuild(self) -> None:
        first = self.build()
        second = self.build()
        self.assertEqual(first, second)

    def test_operation_order_is_path_then_reverse_line_then_id(self) -> None:
        result = self.build()
        self.assertEqual(
            [item["operation_id"] for item in result.typed_edit_ir["operations"]],
            ["replace-build-context-pack", "create-context-types"],
        )
        self.assertEqual(
            [item["application_sequence"] for item in result.typed_edit_ir["operations"]],
            [1, 2],
        )

    def test_proposal_digest_mismatch_blocks(self) -> None:
        self.data["typed_edit_proposal"][m.PROPOSAL_DIGEST_FIELD] = "0" * 64
        result = self.build()
        self.assertIn("typed_edit_proposal_digest_mismatch", result.issues)

    def test_policy_digest_mismatch_blocks(self) -> None:
        self.data["typed_edit_policy"][m.POLICY_DIGEST_FIELD] = "0" * 64
        result = self.build()
        self.assertIn("typed_edit_policy_digest_mismatch", result.issues)

    def test_context_pack_digest_mismatch_blocks(self) -> None:
        self.data["context_pack"][m.CONTEXT_PACK_DIGEST_FIELD] = "0" * 64
        result = self.build()
        self.assertIn("context_pack_digest_mismatch", result.issues)

    def test_context_receipt_digest_mismatch_blocks(self) -> None:
        self.data["context_receipt"][m.CONTEXT_RECEIPT_DIGEST_FIELD] = "0" * 64
        result = self.build()
        self.assertIn("context_receipt_digest_mismatch", result.issues)

    def test_abstention_context_pack_blocks(self) -> None:
        self.data["context_pack"]["codeai_disposition"] = (
            "no_relevant_repository_semantic_context_abstained"
        )
        self.data["context_pack"]["operating_mode"] = "abstain"
        self.reseal_context_chain()
        result = self.build()
        self.assertIn("context_pack_not_built", result.issues)
        self.assertIn("context_pack_not_context_only", result.issues)

    def test_policy_effect_enablement_blocks(self) -> None:
        self.data["typed_edit_policy"]["allow_repository_mutation"] = True
        self.reseal_policy()
        result = self.build()
        self.assertEqual(result.issues, ("typed_edit_policy_effect_or_authority_enabled",))

    def test_proposal_authority_claim_blocks(self) -> None:
        self.data["typed_edit_proposal"]["claims_authority"] = True
        self.reseal_proposal()
        result = self.build()
        self.assertEqual(result.issues, ("typed_edit_proposal_claims_authority",))

    def test_unresolved_question_blocks(self) -> None:
        self.data["typed_edit_proposal"]["unresolved_edit_questions"] = ["Which API?"]
        self.reseal_proposal()
        result = self.build()
        self.assertEqual(result.issues, ("typed_edit_unresolved_questions_present",))

    def test_stale_proposal_blocks(self) -> None:
        self.data["typed_edit_proposal"]["proposal_created_epoch"] = 1
        self.reseal_proposal()
        result = self.build()
        self.assertEqual(result.issues, ("typed_edit_proposal_window_invalid",))

    def test_repository_snapshot_mismatch_blocks(self) -> None:
        self.data["repository_files"]["runtime/context_builder.py"] += "# drift\n"
        result = self.build()
        self.assertIn("repository_snapshot_digest_mismatch", result.issues)

    def test_context_receipt_pack_correspondence_blocks(self) -> None:
        self.data["context_receipt"]["context_pack_digest"] = "1" * 64
        self.data["context_receipt"] = reseal(
            self.data["context_receipt"], m.CONTEXT_RECEIPT_DIGEST_FIELD
        )
        self.data["typed_edit_proposal"]["expected_context_receipt_digest"] = (
            self.data["context_receipt"][m.CONTEXT_RECEIPT_DIGEST_FIELD]
        )
        self.reseal_proposal()
        result = self.build()
        self.assertIn("context_receipt_pack_digest_mismatch", result.issues)

    def test_context_receipt_selected_path_drift_blocks(self) -> None:
        self.data["context_receipt"]["selected_paths"].reverse()
        self.data["context_receipt"] = reseal(
            self.data["context_receipt"], m.CONTEXT_RECEIPT_DIGEST_FIELD
        )
        self.data["typed_edit_proposal"]["expected_context_receipt_digest"] = (
            self.data["context_receipt"][m.CONTEXT_RECEIPT_DIGEST_FIELD]
        )
        self.reseal_proposal()
        result = self.build()
        self.assertIn("context_receipt_selected_paths_mismatch", result.issues)

    def test_supporting_context_path_must_be_selected(self) -> None:
        self.data["typed_edit_proposal"]["supporting_context_paths"].append(
            "runtime/not_selected.py"
        )
        self.reseal_proposal()
        result = self.build()
        self.assertIn(
            "supporting_context_path_not_selected:runtime/not_selected.py", result.issues
        )

    def test_existing_target_must_be_declared_support(self) -> None:
        self.data["typed_edit_proposal"]["supporting_context_paths"] = [
            "tests/test_context_builder.py"
        ]
        self.reseal_proposal()
        result = self.build()
        self.assertIn(
            "existing_target_not_declared_as_support:runtime/context_builder.py",
            result.issues,
        )

    def test_duplicate_operation_id_blocks(self) -> None:
        duplicate = deepcopy(self.data["typed_edit_proposal"]["operations"][0])
        duplicate["path"] = "tests/test_context_builder.py"
        duplicate["anchor_kind"] = "function"
        duplicate["anchor_symbol"] = "test_build_context_pack"
        content = self.data["repository_files"][duplicate["path"]]
        anchor = m._python_locations(content)[0]
        duplicate["expected_file_digest"] = hashlib.sha256(content.encode()).hexdigest()
        duplicate["expected_anchor_digest"] = anchor.digest
        duplicate["expected_start_line"] = anchor.start_line
        duplicate["expected_end_line"] = anchor.end_line
        self.data["typed_edit_proposal"]["operations"].append(duplicate)
        self.reseal_proposal()
        result = self.build()
        self.assertIn("duplicate_operation_id:replace-build-context-pack", result.issues)

    def test_duplicate_symbol_target_blocks(self) -> None:
        duplicate = deepcopy(self.data["typed_edit_proposal"]["operations"][0])
        duplicate["operation_id"] = "replace-build-context-pack-again"
        self.data["typed_edit_proposal"]["operations"].append(duplicate)
        self.reseal_proposal()
        result = self.build()
        self.assertIn(
            "replace-build-context-pack-again:duplicate_symbol_target", result.issues
        )

    def test_duplicate_create_path_blocks(self) -> None:
        duplicate = deepcopy(self.data["typed_edit_proposal"]["operations"][1])
        duplicate["operation_id"] = "create-context-types-again"
        self.data["typed_edit_proposal"]["operations"].append(duplicate)
        self.reseal_proposal()
        result = self.build()
        self.assertIn(
            "create-context-types-again:duplicate_create_path", result.issues
        )

    def test_forbidden_path_blocks(self) -> None:
        operation = self.data["typed_edit_proposal"]["operations"][1]
        operation["path"] = "runtime/private/context_types.py"
        self.reseal_proposal()
        result = self.build()
        self.assertIn("create-context-types:target_path_not_allowed", result.issues)

    def test_operation_not_allowed_blocks(self) -> None:
        self.data["typed_edit_policy"]["allowed_operations"] = [m.OP_CREATE_FILE]
        self.reseal_policy()
        result = self.build()
        self.assertIn("replace-build-context-pack:operation_not_allowed", result.issues)

    def test_language_not_allowed_blocks(self) -> None:
        self.data["typed_edit_policy"]["allowed_languages"] = ["lean"]
        self.reseal_policy()
        result = self.build()
        self.assertIn("replace-build-context-pack:language_not_allowed", result.issues)

    def test_existing_target_language_mismatch_blocks(self) -> None:
        self.data["typed_edit_proposal"]["operations"][0]["language"] = "lean"
        self.reseal_proposal()
        result = self.build()
        self.assertIn("replace-build-context-pack:target_language_mismatch", result.issues)

    def test_expected_file_digest_mismatch_blocks(self) -> None:
        self.data["typed_edit_proposal"]["operations"][0]["expected_file_digest"] = "0" * 64
        self.reseal_proposal()
        result = self.build()
        self.assertIn(
            "replace-build-context-pack:expected_file_digest_mismatch", result.issues
        )

    def test_expected_anchor_digest_mismatch_blocks(self) -> None:
        self.data["typed_edit_proposal"]["operations"][0]["expected_anchor_digest"] = "0" * 64
        self.reseal_proposal()
        result = self.build()
        self.assertIn(
            "replace-build-context-pack:expected_anchor_digest_mismatch", result.issues
        )

    def test_expected_line_mismatch_blocks(self) -> None:
        self.data["typed_edit_proposal"]["operations"][0]["expected_start_line"] = 7
        self.reseal_proposal()
        result = self.build()
        self.assertIn(
            "replace-build-context-pack:expected_start_line_mismatch", result.issues
        )

    def test_missing_anchor_blocks(self) -> None:
        self.data["typed_edit_proposal"]["operations"][0]["anchor_symbol"] = "missing"
        self.reseal_proposal()
        result = self.build()
        self.assertIn("replace-build-context-pack:anchor_not_found", result.issues)

    def test_parse_failure_blocks(self) -> None:
        self.data["repository_files"]["runtime/context_builder.py"] = "def broken(:\n"
        digest = m.canonical_digest(self.data["repository_files"])
        self.data["context_pack"]["repository_snapshot_digest"] = digest
        self.data["context_pack"]["selected_entries"][0]["content_digest"] = hashlib.sha256(
            self.data["repository_files"]["runtime/context_builder.py"].encode()
        ).hexdigest()
        self.data["context_receipt"]["repository_snapshot_digest"] = digest
        self.data["typed_edit_proposal"]["repository_snapshot_digest"] = digest
        self.data["typed_edit_proposal"]["operations"][0]["expected_file_digest"] = (
            self.data["context_pack"]["selected_entries"][0]["content_digest"]
        )
        self.reseal_context_chain()
        result = self.build()
        self.assertIn(
            "replace-build-context-pack:target_parse_failed:SyntaxError", result.issues
        )

    def test_anchor_span_budget_blocks(self) -> None:
        self.data["typed_edit_policy"]["maximum_anchor_span_lines"] = 1
        self.reseal_policy()
        result = self.build()
        self.assertIn(
            "replace-build-context-pack:anchor_span_budget_exceeded", result.issues
        )

    def test_new_text_per_operation_budget_blocks(self) -> None:
        self.data["typed_edit_policy"]["maximum_new_text_bytes_per_operation"] = 8
        self.reseal_policy()
        result = self.build()
        self.assertIn("replace-build-context-pack:new_text_budget_exceeded", result.issues)

    def test_total_new_text_budget_blocks(self) -> None:
        self.data["typed_edit_policy"]["maximum_total_new_text_bytes"] = 20
        self.reseal_policy()
        result = self.build()
        self.assertIn("typed_edit_total_new_text_budget_exceeded", result.issues)

    def test_operation_count_budget_blocks(self) -> None:
        self.data["typed_edit_policy"]["maximum_operations"] = 1
        self.reseal_policy()
        result = self.build()
        self.assertIn("typed_edit_operation_budget_exceeded", result.issues)

    def test_trace_budget_blocks(self) -> None:
        self.data["typed_edit_policy"]["maximum_requirement_trace_ids_per_operation"] = 1
        self.data["typed_edit_proposal"]["operations"][0]["requirement_trace_ids"] = [
            "a", "b"
        ]
        self.reseal_policy()
        self.reseal_proposal()
        result = self.build()
        self.assertIn(
            "replace-build-context-pack:requirement_trace_ids_budget_exceeded",
            result.issues,
        )

    def test_create_existing_path_blocks(self) -> None:
        self.data["typed_edit_proposal"]["operations"][1]["path"] = (
            "runtime/context_builder.py"
        )
        self.reseal_proposal()
        result = self.build()
        self.assertIn("create-context-types:create_file_path_already_exists", result.issues)

    def test_create_requires_absent_precondition(self) -> None:
        self.data["typed_edit_proposal"]["operations"][1]["precondition_kind"] = (
            m.PRECONDITION_SYMBOL_EXACT
        )
        self.reseal_proposal()
        result = self.build()
        self.assertIn(
            "create-context-types:create_file_path_absent_precondition_required",
            result.issues,
        )

    def test_create_can_be_disabled(self) -> None:
        self.data["typed_edit_policy"]["allow_create_file"] = False
        self.reseal_policy()
        result = self.build()
        self.assertIn("create-context-types:create_file_not_allowed", result.issues)

    def test_delete_can_be_disabled(self) -> None:
        operation = self.data["typed_edit_proposal"]["operations"][0]
        operation["operation"] = m.OP_DELETE_SYMBOL
        operation["new_text"] = ""
        self.data["typed_edit_policy"]["allow_delete_symbol"] = False
        self.reseal_proposal()
        self.reseal_policy()
        result = self.build()
        self.assertIn(
            "replace-build-context-pack:delete_symbol_not_allowed", result.issues
        )

    def test_delete_requires_empty_new_text(self) -> None:
        self.data["typed_edit_proposal"]["operations"][0]["operation"] = (
            m.OP_DELETE_SYMBOL
        )
        self.reseal_proposal()
        result = self.build()
        self.assertIn(
            "replace-build-context-pack:delete_symbol_requires_empty_new_text",
            result.issues,
        )

    def test_context_entry_digest_mismatch_blocks(self) -> None:
        self.data["context_pack"]["selected_entries"][0]["content_digest"] = "0" * 64
        self.reseal_context_chain()
        result = self.build()
        self.assertIn(
            "supporting_context_content_digest_mismatch:runtime/context_builder.py",
            result.issues,
        )

    def test_lean_symbol_anchor_is_supported(self) -> None:
        content = (
            "import Mathlib\n\n"
            "def alpha : Nat := 1\n\n"
            "theorem beta : alpha = 1 := by rfl\n"
        )
        self.data["repository_files"]["formal/Example.lean"] = content
        digest = m.canonical_digest(self.data["repository_files"])
        location = [item for item in m._lean_locations(content) if item.name == "beta"][0]
        entry = {
            "path": "formal/Example.lean",
            "content_digest": hashlib.sha256(content.encode()).hexdigest(),
            "language": "lean",
            "declared_symbols": ["alpha", "beta"],
        }
        self.data["context_pack"]["selected_entries"].append(entry)
        self.data["context_pack"]["selected_file_count"] += 1
        self.data["context_pack"]["repository_snapshot_digest"] = digest
        self.data["context_receipt"]["selected_paths"].append("formal/Example.lean")
        self.data["context_receipt"]["repository_snapshot_digest"] = digest
        self.data["typed_edit_proposal"]["repository_snapshot_digest"] = digest
        self.data["typed_edit_proposal"]["supporting_context_paths"].append(
            "formal/Example.lean"
        )
        self.data["typed_edit_proposal"]["operations"] = [
            {
                "operation_id": "replace-beta",
                "operation": m.OP_REPLACE_SYMBOL,
                "path": "formal/Example.lean",
                "language": "lean",
                "precondition_kind": m.PRECONDITION_SYMBOL_EXACT,
                "anchor_kind": "theorem",
                "anchor_symbol": "beta",
                "expected_file_digest": hashlib.sha256(content.encode()).hexdigest(),
                "expected_anchor_digest": location.digest,
                "expected_start_line": location.start_line,
                "expected_end_line": location.end_line,
                "new_text": "theorem beta : alpha = 1 := by decide\n",
                "requirement_trace_ids": ["intent:lean"],
                "test_plan_ids": ["test:lean"],
                "risk_labels": ["formal"],
            }
        ]
        self.data["typed_edit_policy"]["allowed_repository_path_prefixes"].append(
            "formal"
        )
        self.reseal_policy()
        self.reseal_context_chain()
        result = self.build()
        self.assertEqual(result.status, m.STATUS_READY)
        self.assertEqual(result.typed_edit_ir["operations"][0]["anchor_kind"], "theorem")

    def test_receipt_grants_no_authority_or_effect(self) -> None:
        result = self.build()
        receipt = result.receipt
        self.assertFalse(receipt["repository_mutation_performed"])
        self.assertFalse(receipt["provider_invoked"])
        self.assertFalse(receipt["verification_runner_invoked"])
        self.assertFalse(receipt["candidate_selection_authority_granted"])
        self.assertFalse(receipt["execution_authority_granted"])
        self.assertFalse(receipt["whole_file_modify_allowed"])


if __name__ == "__main__":
    unittest.main()
