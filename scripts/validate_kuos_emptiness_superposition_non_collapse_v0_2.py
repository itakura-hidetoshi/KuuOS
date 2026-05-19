#!/usr/bin/env python3
"""
validate_kuos_emptiness_superposition_non_collapse_v0_2.py

Stdlib-only validator for KuuOS Emptiness Superposition Non-Collapse v0.2.

This validator checks that the v0.2 contract, doctrine doc, and validation cases
preserve the KuuOS rule: nonzero competing catuskoti support blocks premature
single-origin authority release unless a context-bound collapse receipt exists.

It does not grant truth, proof, clinical, world, or execution authority.
"""

from __future__ import annotations

import json
import math
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "KUOS_EMPTINESS_SUPERPOSITION_NON_COLLAPSE_v0_2.md"
CONTRACT = ROOT / "specs" / "kuos_emptiness_superposition_non_collapse_contract_v0_2.yaml"
CASES = ROOT / "validation_cases" / "kuos_emptiness_superposition_non_collapse_validation_cases_v0_2.json"

FORBIDDEN_DIRECT_ROUTES = {
    "TRUTH_RELEASE",
    "PROOF_AUTHORITY",
    "EXECUTION_AUTHORITY",
    "CLINICAL_AUTHORITY",
    "WORLD_AUTHORITY",
}
ALLOWED_CONTEXTUAL_ROUTES = {
    "HOLD",
    "REVIEW",
    "REOBSERVE",
    "CONTEXTUAL_COLLAPSE_WITH_RECEIPT",
}
BASIS = ("S", "O", "B", "N")


def approx_norm_squared(amplitudes: dict[str, float]) -> float:
    return sum(float(amplitudes.get(k, 0.0)) ** 2 for k in BASIS)


def nonzero_count(amplitudes: dict[str, float], eps: float = 1e-9) -> int:
    return sum(1 for k in BASIS if abs(float(amplitudes.get(k, 0.0))) > eps)


def evaluate_case(case: dict) -> str:
    amplitudes = case.get("amplitudes", {})
    requested_route = case.get("requested_route")
    has_receipt = bool(case.get("has_collapse_receipt"))

    if set(amplitudes.keys()) != set(BASIS):
        return "FAIL"

    norm2 = approx_norm_squared(amplitudes)
    if not math.isfinite(norm2) or norm2 <= 0.0:
        return "FAIL"

    competing = nonzero_count(amplitudes) >= 2

    if requested_route in FORBIDDEN_DIRECT_ROUTES:
        if competing and not has_receipt:
            return "HOLD"
        if competing and has_receipt:
            return "REVIEW"
        return "REVIEW"

    if requested_route == "CONTEXTUAL_COLLAPSE_WITH_RECEIPT":
        if has_receipt and not competing:
            return "CONTEXTUAL_COLLAPSE_WITH_RECEIPT"
        if has_receipt and competing:
            return "REVIEW"
        return "HOLD"

    if requested_route in ALLOWED_CONTEXTUAL_ROUTES:
        if competing:
            return requested_route
        return "REVIEW"

    return "FAIL"


def require_tokens(path: pathlib.Path, tokens: list[str], errors: list[str]) -> None:
    if not path.is_file():
        errors.append(f"missing file: {path.relative_to(ROOT)}")
        return
    text = path.read_text(encoding="utf-8")
    for token in tokens:
        if token not in text:
            errors.append(f"{path.relative_to(ROOT)} missing token: {token}")


def main() -> int:
    errors: list[str] = []

    require_tokens(
        DOC,
        [
            "Catuskoti Superposition Non-Collapse",
            "candidate-as-superposition",
            "sharp conventional commitment",
            "collapse_context",
            "not execution authority",
            "v0.2",
        ],
        errors,
    )

    require_tokens(
        CONTRACT,
        [
            "kuos_emptiness_superposition_non_collapse_contract_v0_2",
            "Catuskoti Superposition Non-Collapse Theorem",
            "premature_single_origin_release_is_blocked",
            "CONTEXTUAL_COLLAPSE_WITH_RECEIPT",
            "validator_pass_grants_truth",
            "overwrite_forbidden: true",
        ],
        errors,
    )

    if not CASES.is_file():
        errors.append("missing validation cases")
    else:
        data = json.loads(CASES.read_text(encoding="utf-8"))
        for case in data.get("cases", []):
            got = evaluate_case(case)
            expected = case.get("expected_status")
            if got != expected:
                errors.append(f"{case.get('id')}: expected {expected}, got {got}")
            if got in FORBIDDEN_DIRECT_ROUTES:
                errors.append(f"{case.get('id')}: forbidden authority route leaked: {got}")

    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1

    print("PASS: KuuOS emptiness superposition non-collapse v0.2 validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
