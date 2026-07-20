from __future__ import annotations

import unittest

from runtime.kuuos_codeai_selective_repository_semantic_context_pack_v0_1 import (
    DISPOSITION_ABSTAINED,
    DISPOSITION_BUILT,
    MODE_ABSTAIN,
    MODE_CONTEXT_ONLY,
    PACK_DIGEST_FIELD,
    POLICY_DIGEST_FIELD,
    RECEIPT_DIGEST_FIELD,
    REQUEST_DIGEST_FIELD,
    SOURCE_RECEIPT_DIGEST_FIELD,
    STATUS_BLOCKED,
    STATUS_READY,
    build_codeai_selective_repository_semantic_context_pack,
    canonical_digest,
    digest_without,
    seal,
)

EPOCH = 1784325000
COMMIT = "7" * 40


def source_receipt(**changes: object) -> dict:
    value = {
        "schema_version": "v0.1",
        "profile_version": "CodeAI v0.1",
        "intent_packet_digest": "1" * 64,
        "repository_observation_digest": "2" * 64,
        "observation_policy_digest": "3" * 64,
        "intent_id": "intent-context-pack",
        "intent_revision": "r1",
        "source_actor_id": "operator",
        "authority_owner_id": "owner",
        "repository_full_name": "itakura-hidetoshi/KuuOS",
        "source_commit_sha": COMMIT,
        "resulting_commit_sha": COMMIT,
        "source_branch": "main",
        "tree_digest": "tree-context-pack",
        "observed_path_count": 4,
        "unavailable_path_count": 0,
        "declared_path_count": 4,
        "baseline_checks_complete": True,
        "codeai_disposition": "intent_repository_observation_supported",
        "operating_mode": "read_only",
        "route_receipt_recorded": True,
        "codeai_profile_ready": True,
        "clarification_required": False,
        "reobservation_required": False,
        "abstained": False,
        "handover_required": False,
        "repository_observation_read_only": True,
        "code_change_candidate_created": False,
        "execution_lease_issued": False,
        "repository_mutation_performed": False,
        "git_ref_changed": False,
        "branch_created": False,
        "commit_created": False,
        "push_performed": False,
        "pull_request_created": False,
        "merge_performed": False,
        "deployment_performed": False,
        "secret_access_performed": False,
        "selection_authority_granted": False,
        "execution_authority_granted": False,
        "merge_authority_granted": False,
        "deployment_authority_granted": False,
        "secret_access_authority_granted": False,
        "intent_treated_as_truth": False,
        "repository_observation_treated_as_repository_truth": False,
        "validation_treated_as_correctness_proof": False,
        "history_read_only": True,
        "future_only": True,
        "active_now": False,
    }
    value.update(changes)
    return seal(value, SOURCE_RECEIPT_DIGEST_FIELD)


def repository() -> dict[str, str]:
    return {
        "runtime/context_builder.py": (
            "from dataclasses import dataclass\n"
            "import json\n\n"
            "@dataclass\n"
            "class SemanticContext:\n"
            "    name: str\n\n"
            "def build_context_pack(query: str) -> SemanticContext:\n"
            "    return SemanticContext(query)\n"
        ),
        "runtime/unrelated.py": "def unrelated_feature() -> int:\n    return 1\n",
        "tests/test_context_builder.py": (
            "from runtime.context_builder import build_context_pack\n\n"
            "def test_build_context_pack() -> None:\n"
            "    assert build_context_pack('x').name == 'x'\n"
        ),
        "docs/CONTEXT.md": "# Semantic context pack\n\nSelective repository context.\n",
        "formal/ContextPack.lean": (
            "import Mathlib.Data.Nat.Basic\n\n"
            "namespace ContextPack\n\n"
            "structure SelectedContext where\n"
            "  score : Nat\n\n"
            "theorem score_nonnegative (c : SelectedContext) : 0 ≤ c.score := by omega\n\n"
            "end ContextPack\n"
        ),
    }


def request(repo: dict[str, str] | None = None, **changes: object) -> dict:
    repo = repo or repository()
    value = {
        "request_id": "context-pack-request",
        "request_revision": "r1",
        "intent_text": "Build selective semantic context for the context pack implementation.",
        "query_terms": ["context", "semantic"],
        "target_path_prefixes": ["runtime"],
        "target_symbols": ["build_context_pack"],
        "test_plan_ids": ["test:context-pack"],
        "required_roles": ["source", "test"],
        "request_created_epoch": EPOCH - 10,
        "repository_snapshot_digest": canonical_digest(repo),
        "expected_source_observation_receipt_digest": source_receipt()[SOURCE_RECEIPT_DIGEST_FIELD],
        "prior_pack_digests": [],
        "unresolved_context_questions": [],
    }
    value.update(changes)
    return seal(value, REQUEST_DIGEST_FIELD)


def policy(**changes: object) -> dict:
    value = {
        "expected_repository_full_name": "itakura-hidetoshi/KuuOS",
        "expected_source_commit_sha": COMMIT,
        "allowed_repository_path_prefixes": ["runtime", "tests", "docs", "formal"],
        "forbidden_repository_path_prefixes": ["runtime/private"],
        "supported_file_suffixes": [".py", ".lean", ".md", ".json", ".toml", ".yml", ".yaml"],
        "maximum_repository_snapshot_bytes": 200000,
        "maximum_candidate_files": 20,
        "maximum_selected_files": 4,
        "maximum_file_bytes": 50000,
        "maximum_excerpt_bytes": 4000,
        "maximum_total_context_bytes": 30000,
        "maximum_symbols_per_file": 32,
        "maximum_imports_per_file": 32,
        "maximum_query_terms": 12,
        "maximum_request_age": 3600,
        "evaluation_epoch": EPOCH,
        "allow_text_fallback": True,
        "require_relevant_context": True,
        "allow_empty_context_abstention": True,
        "allow_repository_mutation": False,
        "allow_network_access": False,
        "allow_secret_access": False,
        "allow_candidate_selection_authority": False,
        "allow_execution_authority": False,
    }
    value.update(changes)
    return seal(value, POLICY_DIGEST_FIELD)


class SelectiveRepositorySemanticContextPackTests(unittest.TestCase):
    def build(
        self,
        *,
        repo: dict[str, str] | None = None,
        source: dict | None = None,
        context_request: dict | None = None,
        context_policy: dict | None = None,
    ):
        repo = repo or repository()
        source = source or source_receipt()
        context_request = context_request or request(repo)
        context_policy = context_policy or policy()
        return build_codeai_selective_repository_semantic_context_pack(
            source_observation_receipt=source,
            repository_files=repo,
            context_request=context_request,
            context_policy=context_policy,
        )

    def test_relevant_source_and_test_are_selected(self) -> None:
        result = self.build()
        self.assertEqual(result.status, STATUS_READY)
        self.assertIsNotNone(result.context_pack)
        paths = [entry["path"] for entry in result.context_pack["selected_entries"]]
        self.assertIn("runtime/context_builder.py", paths)
        self.assertIn("tests/test_context_builder.py", paths)
        self.assertNotIn("runtime/unrelated.py", paths)
        self.assertEqual(result.context_pack["codeai_disposition"], DISPOSITION_BUILT)
        self.assertEqual(result.context_pack["operating_mode"], MODE_CONTEXT_ONLY)

    def test_selection_is_deterministic(self) -> None:
        first = self.build()
        second = self.build()
        self.assertEqual(first.context_pack, second.context_pack)
        self.assertEqual(first.receipt, second.receipt)

    def test_target_symbol_is_recorded_as_reason(self) -> None:
        result = self.build()
        entry = next(
            item for item in result.context_pack["selected_entries"]
            if item["path"] == "runtime/context_builder.py"
        )
        self.assertIn("target_symbol:build_context_pack", entry["selection_reasons"])
        self.assertIn("build_context_pack", entry["declared_symbols"])

    def test_python_imports_are_extracted(self) -> None:
        result = self.build()
        entry = next(
            item for item in result.context_pack["selected_entries"]
            if item["path"] == "runtime/context_builder.py"
        )
        self.assertIn("dataclasses", entry["imports"])
        self.assertIn("json", entry["imports"])
        self.assertEqual(entry["parse_status"], "parsed")

    def test_lean_semantics_are_extracted_when_targeted(self) -> None:
        repo = repository()
        req = request(
            repo,
            query_terms=["SelectedContext"],
            target_path_prefixes=["formal"],
            target_symbols=["SelectedContext"],
            required_roles=["formal"],
            test_plan_ids=[],
        )
        result = self.build(repo=repo, context_request=req)
        self.assertEqual(result.status, STATUS_READY)
        self.assertEqual(result.context_pack["selected_entries"][0]["path"], "formal/ContextPack.lean")
        self.assertIn("Mathlib.Data.Nat.Basic", result.context_pack["selected_entries"][0]["imports"])
        self.assertIn("SelectedContext", result.context_pack["selected_entries"][0]["declared_symbols"])

    def test_maximum_selected_files_is_enforced(self) -> None:
        result = self.build(context_policy=policy(maximum_selected_files=1))
        self.assertEqual(result.status, STATUS_READY)
        self.assertEqual(result.context_pack["selected_file_count"], 1)
        self.assertGreater(result.context_pack["omitted_relevant_file_count"], 0)

    def test_snapshot_digest_mismatch_blocks(self) -> None:
        malformed = request(repository())
        malformed["repository_snapshot_digest"] = "0" * 64
        malformed = seal(malformed, REQUEST_DIGEST_FIELD)
        result = self.build(context_request=malformed)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn("repository_snapshot_digest_mismatch", result.issues)

    def test_source_receipt_digest_mismatch_blocks(self) -> None:
        malformed = source_receipt()
        malformed[SOURCE_RECEIPT_DIGEST_FIELD] = "0" * 64
        result = self.build(
            source=malformed,
            context_request=request(
                repository(),
                expected_source_observation_receipt_digest="0" * 64,
            ),
        )
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn("source_observation_receipt_digest_mismatch", result.issues)

    def test_unsupported_source_receipt_blocks(self) -> None:
        malformed = source_receipt(codeai_disposition="intent_clarification_hold")
        req = request(
            repository(),
            expected_source_observation_receipt_digest=malformed[SOURCE_RECEIPT_DIGEST_FIELD],
        )
        result = self.build(source=malformed, context_request=req)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn("source_observation_receipt_not_supported", result.issues)

    def test_non_read_only_source_receipt_blocks(self) -> None:
        malformed = source_receipt(operating_mode="proposal_only")
        req = request(
            repository(),
            expected_source_observation_receipt_digest=malformed[SOURCE_RECEIPT_DIGEST_FIELD],
        )
        result = self.build(source=malformed, context_request=req)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn("source_observation_receipt_not_read_only", result.issues)

    def test_effect_enabled_policy_blocks(self) -> None:
        result = self.build(context_policy=policy(allow_network_access=True))
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertEqual(result.issues, ("context_policy_effect_or_authority_enabled",))

    def test_candidate_selection_authority_policy_blocks(self) -> None:
        result = self.build(context_policy=policy(allow_candidate_selection_authority=True))
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertEqual(result.issues, ("context_policy_effect_or_authority_enabled",))

    def test_stale_request_blocks(self) -> None:
        req = request(repository(), request_created_epoch=EPOCH - 5000)
        result = self.build(context_request=req)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertEqual(result.issues, ("context_request_window_invalid",))

    def test_future_request_blocks(self) -> None:
        req = request(repository(), request_created_epoch=EPOCH + 1)
        result = self.build(context_request=req)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertEqual(result.issues, ("context_request_window_invalid",))

    def test_query_term_budget_blocks(self) -> None:
        terms = [f"term-{index}" for index in range(4)]
        req = request(repository(), query_terms=terms)
        result = self.build(
            context_request=req,
            context_policy=policy(maximum_query_terms=3),
        )
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertEqual(result.issues, ("context_query_term_budget_exceeded",))

    def test_repository_snapshot_budget_blocks(self) -> None:
        result = self.build(context_policy=policy(maximum_repository_snapshot_bytes=10))
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertEqual(result.issues, ("repository_snapshot_budget_exceeded",))

    def test_forbidden_target_prefix_blocks(self) -> None:
        req = request(repository(), target_path_prefixes=["runtime/private"])
        result = self.build(context_request=req)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertEqual(result.issues, ("target_path_prefix_forbidden:runtime/private",))

    def test_target_prefix_outside_allowed_scope_blocks(self) -> None:
        req = request(repository(), target_path_prefixes=["secrets"])
        result = self.build(context_request=req)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertEqual(result.issues, ("target_path_prefix_not_allowed:secrets",))

    def test_no_relevant_context_abstains_when_allowed(self) -> None:
        repo = repository()
        req = request(
            repo,
            query_terms=["does-not-exist"],
            target_path_prefixes=[],
            target_symbols=[],
            test_plan_ids=[],
            required_roles=[],
        )
        result = self.build(repo=repo, context_request=req)
        self.assertEqual(result.status, STATUS_READY)
        self.assertEqual(result.context_pack["selected_file_count"], 0)
        self.assertEqual(result.context_pack["codeai_disposition"], DISPOSITION_ABSTAINED)
        self.assertEqual(result.context_pack["operating_mode"], MODE_ABSTAIN)

    def test_no_relevant_context_blocks_when_abstention_disabled(self) -> None:
        repo = repository()
        req = request(
            repo,
            query_terms=["does-not-exist"],
            target_path_prefixes=[],
            target_symbols=[],
            test_plan_ids=[],
            required_roles=[],
        )
        result = self.build(
            repo=repo,
            context_request=req,
            context_policy=policy(allow_empty_context_abstention=False),
        )
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertEqual(result.issues, ("no_relevant_semantic_context",))

    def test_python_parse_failure_uses_fallback_when_allowed(self) -> None:
        repo = {"runtime/broken.py": "def broken(:\n"}
        req = request(
            repo,
            query_terms=["broken"],
            target_path_prefixes=["runtime"],
            target_symbols=[],
            test_plan_ids=[],
            required_roles=["source"],
        )
        result = self.build(repo=repo, context_request=req)
        self.assertEqual(result.status, STATUS_READY)
        entry = result.context_pack["selected_entries"][0]
        self.assertEqual(entry["parse_status"], "fallback")
        self.assertEqual(entry["parse_error_type"], "SyntaxError")

    def test_python_parse_failure_blocks_without_fallback(self) -> None:
        repo = {"runtime/broken.py": "def broken(:\n"}
        req = request(
            repo,
            query_terms=["broken"],
            target_path_prefixes=["runtime"],
            target_symbols=[],
            test_plan_ids=[],
            required_roles=["source"],
        )
        result = self.build(
            repo=repo,
            context_request=req,
            context_policy=policy(allow_text_fallback=False),
        )
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn("semantic_parse_failed:runtime/broken.py:SyntaxError", result.issues)

    def test_candidate_file_budget_blocks(self) -> None:
        result = self.build(context_policy=policy(maximum_candidate_files=1))
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertEqual(result.issues, ("semantic_candidate_file_budget_exceeded",))

    def test_oversized_file_is_reported_without_forwarding_content(self) -> None:
        repo = {
            "runtime/large.py": "def context():\n    return '" + ("x" * 2000) + "'\n"
        }
        req = request(
            repo,
            query_terms=["context"],
            target_path_prefixes=["runtime"],
            target_symbols=["context"],
            test_plan_ids=[],
            required_roles=["source"],
        )
        result = self.build(
            repo=repo,
            context_request=req,
            context_policy=policy(
                maximum_file_bytes=100,
                allow_empty_context_abstention=True,
            ),
        )
        self.assertEqual(result.status, STATUS_READY)
        self.assertEqual(result.context_pack["selected_file_count"], 0)
        self.assertEqual(
            result.context_pack["oversized_eligible_paths"],
            ["runtime/large.py"],
        )

    def test_pack_and_receipt_digests_are_sealed(self) -> None:
        result = self.build()
        self.assertEqual(
            result.context_pack[PACK_DIGEST_FIELD],
            digest_without(result.context_pack, PACK_DIGEST_FIELD),
        )
        self.assertEqual(
            result.receipt[RECEIPT_DIGEST_FIELD],
            digest_without(result.receipt, RECEIPT_DIGEST_FIELD),
        )

    def test_receipt_preserves_no_effect_boundaries(self) -> None:
        result = self.build()
        self.assertTrue(result.receipt["repository_snapshot_read_only"])
        self.assertFalse(result.receipt["full_repository_forwarded"])
        self.assertFalse(result.receipt["provider_invoked"])
        self.assertFalse(result.receipt["repository_mutation_performed"])
        self.assertFalse(result.receipt["git_effect_performed"])
        self.assertFalse(result.receipt["candidate_selection_authority_granted"])
        self.assertFalse(result.receipt["execution_authority_granted"])
        self.assertFalse(result.receipt["repository_content_treated_as_truth"])
        self.assertFalse(result.receipt["semantic_match_treated_as_correctness_proof"])

    def test_request_extra_field_blocks(self) -> None:
        malformed = request(repository())
        malformed["extra"] = True
        malformed = seal(malformed, REQUEST_DIGEST_FIELD)
        result = self.build(context_request=malformed)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertTrue(
            any(item.startswith("context_request_extra_fields") for item in result.issues)
        )

    def test_duplicate_query_terms_block(self) -> None:
        malformed = request(repository())
        malformed["query_terms"] = ["context", "context"]
        malformed = seal(malformed, REQUEST_DIGEST_FIELD)
        result = self.build(context_request=malformed)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn("context_request_invalid_string_list:query_terms", result.issues)

    def test_invalid_repository_path_blocks(self) -> None:
        repo = {"../escape.py": "x = 1\n"}
        req = request(repo)
        result = self.build(repo=repo, context_request=req)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn("repository_file_path_invalid:../escape.py", result.issues)


if __name__ == "__main__":
    unittest.main()
