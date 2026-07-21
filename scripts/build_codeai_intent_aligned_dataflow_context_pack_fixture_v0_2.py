#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy
from typing import Any

from runtime.kuuos_codeai_intent_aligned_dataflow_context_pack_checks_v0_2 import canonical_digest, seal
from runtime.kuuos_codeai_intent_aligned_dataflow_context_pack_schema_v0_2 import (
    HYPOTHESIS_DIGEST_FIELD,
    POLICY_DIGEST_FIELD,
    REQUEST_DIGEST_FIELD,
    SOURCE_RECEIPT_DIGEST_FIELD,
)
from runtime.kuuos_codeai_intent_aligned_dataflow_context_pack_v0_2 import (
    build_intent_aligned_dataflow_context_pack,
)

REPOSITORY_FULL_NAME = "itakura-hidetoshi/KuuOS"
SOURCE_COMMIT_SHA = "1d953b9d8383b5fc1ab42431c6fa9bec39a83b61"


def reference_repository() -> dict[str, str]:
    return {
        "runtime/order_pipeline.py": (
            "from runtime.pricing import apply_tax, compute_subtotal\n"
            "\n"
            "def build_order_total(items: list[int], tax_rate: float) -> float:\n"
            "    subtotal = compute_subtotal(items)\n"
            "    taxed_total = apply_tax(subtotal, tax_rate)\n"
            "    return taxed_total\n"
        ),
        "runtime/pricing.py": (
            "def compute_subtotal(items: list[int]) -> float:\n"
            "    return float(sum(items))\n"
            "\n"
            "def apply_tax(subtotal: float, tax_rate: float) -> float:\n"
            "    tax_amount = subtotal * tax_rate\n"
            "    total = subtotal + tax_amount\n"
            "    return total\n"
        ),
        "tests/test_order_pipeline.py": (
            "from runtime.order_pipeline import build_order_total\n"
            "\n"
            "def test_build_order_total_tracks_tax_dataflow() -> None:\n"
            "    assert build_order_total([100, 50], 0.1) == 165.0\n"
        ),
        "formal/KUOS/CodeAI/PricingReferenceV0_2.lean": (
            "import Mathlib\n"
            "\n"
            "namespace KUOS.CodeAI.PricingReferenceV0_2\n"
            "\n"
            "def computeSubtotal (items : List Nat) : Nat := items.sum\n"
            "\n"
            "def applyTaxBasisPoints (subtotal rate : Nat) : Nat :=\n"
            "  subtotal + subtotal * rate / 10000\n"
            "\n"
            "end KUOS.CodeAI.PricingReferenceV0_2\n"
        ),
        "formal/KUOS/CodeAI/OrderPipelineReferenceV0_2.lean": (
            "import KUOS.CodeAI.PricingReferenceV0_2\n"
            "\n"
            "namespace KUOS.CodeAI.OrderPipelineReferenceV0_2\n"
            "\n"
            "open PricingReferenceV0_2\n"
            "\n"
            "def buildOrderTotal (items : List Nat) (rate : Nat) : Nat :=\n"
            "  applyTaxBasisPoints (computeSubtotal items) rate\n"
            "\n"
            "theorem buildOrderTotal_nonnegative (items : List Nat) (rate : Nat) :\n"
            "    0 ≤ buildOrderTotal items rate := by omega\n"
            "\n"
            "end KUOS.CodeAI.OrderPipelineReferenceV0_2\n"
        ),
        "docs/order_pipeline_dataflow.md": (
            "# Order total dataflow\n"
            "\n"
            "The order pipeline sends `items` into `compute_subtotal`, then sends the resulting "
            "`subtotal` and `tax_rate` into `apply_tax`. The Lean reference mirrors the same "
            "dependency through `computeSubtotal`, `applyTaxBasisPoints`, and `buildOrderTotal`.\n"
        ),
        "config/unrelated_feature.json": '{"feature":"unrelated","enabled":true}\n',
    }


def reference_source_receipt(repository: dict[str, str]) -> dict[str, Any]:
    return seal(
        {
            "schema_version": "v0.1",
            "profile_version": "CodeAI Intent Repository Observation v0.1",
            "codeai_disposition": "intent_repository_observation_supported",
            "operating_mode": "read_only",
            "repository_observation_read_only": True,
            "repository_mutation_performed": False,
            "repository_full_name": REPOSITORY_FULL_NAME,
            "source_commit_sha": SOURCE_COMMIT_SHA,
            "tree_digest": canonical_digest(repository),
        },
        SOURCE_RECEIPT_DIGEST_FIELD,
    )


def _hypothesis(
    hypothesis_id: str,
    statement: str,
    query_terms: list[str],
    expected_symbols: list[str],
) -> dict[str, Any]:
    return seal(
        {
            "hypothesis_id": hypothesis_id,
            "statement": statement,
            "query_terms": query_terms,
            "expected_symbols": expected_symbols,
        },
        HYPOTHESIS_DIGEST_FIELD,
    )


def reference_request(repository: dict[str, str], source_receipt: dict[str, Any]) -> dict[str, Any]:
    return seal(
        {
            "request_id": "intent-dataflow-context-001",
            "request_revision": "r1",
            "intent_text": "Strengthen order-total tax dataflow context across runtime tests and Lean reference proofs.",
            "initial_query_terms": ["order", "total", "tax", "dataflow"],
            "candidate_hypotheses": [
                _hypothesis(
                    "h-runtime-tax-flow",
                    "The runtime patch risk lies between subtotal production and tax application.",
                    ["subtotal", "apply_tax", "tax_rate"],
                    ["build_order_total", "compute_subtotal", "apply_tax"],
                ),
                _hypothesis(
                    "h-formal-alignment",
                    "The formal reference must preserve the same subtotal-to-tax dependency.",
                    ["computeSubtotal", "applyTaxBasisPoints", "buildOrderTotal"],
                    ["computeSubtotal", "applyTaxBasisPoints", "buildOrderTotal_nonnegative"],
                ),
            ],
            "target_path_prefixes": ["runtime", "tests", "formal", "docs"],
            "target_symbols": [
                "build_order_total",
                "compute_subtotal",
                "apply_tax",
                "buildOrderTotal",
                "applyTaxBasisPoints",
            ],
            "required_roles": ["source", "test", "formal", "documentation"],
            "request_created_epoch": 100,
            "repository_snapshot_digest": canonical_digest(repository),
            "expected_source_observation_receipt_digest": source_receipt[SOURCE_RECEIPT_DIGEST_FIELD],
        },
        REQUEST_DIGEST_FIELD,
    )


def reference_policy() -> dict[str, Any]:
    return seal(
        {
            "expected_repository_full_name": REPOSITORY_FULL_NAME,
            "expected_source_commit_sha": SOURCE_COMMIT_SHA,
            "allowed_repository_path_prefixes": ["runtime", "tests", "formal", "docs", "config"],
            "forbidden_repository_path_prefixes": [".git", ".secrets"],
            "supported_file_suffixes": [".py", ".lean", ".md", ".json"],
            "maximum_repository_snapshot_bytes": 32768,
            "maximum_candidate_files": 16,
            "maximum_selected_files": 6,
            "maximum_file_bytes": 8192,
            "maximum_excerpt_bytes": 4096,
            "maximum_total_context_bytes": 16384,
            "maximum_query_terms": 32,
            "maximum_hypotheses": 4,
            "maximum_dependency_depth": 3,
            "minimum_intent_evidence_score": 4,
            "maximum_request_age": 20,
            "evaluation_epoch": 110,
            "allow_text_fallback": True,
            "require_dependency_path": True,
            "require_symbol_digest": True,
            "allow_repository_mutation": False,
            "allow_network_access": False,
            "allow_secret_access": False,
            "allow_candidate_selection_authority": False,
            "allow_execution_authority": False,
        },
        POLICY_DIGEST_FIELD,
    )


def build_reference_inputs() -> dict[str, Any]:
    repository = reference_repository()
    source_receipt = reference_source_receipt(repository)
    request = reference_request(repository, source_receipt)
    policy = reference_policy()
    return {
        "repository_snapshot": repository,
        "source_observation_receipt": source_receipt,
        "request": request,
        "policy": policy,
    }


def build_reference_result() -> dict[str, Any]:
    inputs = build_reference_inputs()
    result = build_intent_aligned_dataflow_context_pack(**inputs)
    if result.status != "ready" or result.context_pack is None or result.receipt is None:
        raise RuntimeError("reference context pack did not build: " + ",".join(result.issues))
    return {
        "inputs": deepcopy(inputs),
        "context_pack": result.context_pack,
        "receipt": result.receipt,
    }


if __name__ == "__main__":
    import json

    print(json.dumps(build_reference_result(), ensure_ascii=False, indent=2, sort_keys=True))
