#!/usr/bin/env python3
"""Validate the Qi Process Tensor v0.2FG release-chain documentation.

This small docs validator prevents the human-readable release-chain surface from
silently losing the v0.2F/v0.2G invariants.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "KUUOS_QI_PROCESS_TENSOR_RELEASE_CHAIN_v0_2FG.md"

REQUIRED_PHRASES = {
    "Qi Process Tensor v0.2F",
    "Qi Process Tensor conventional autonomy v0.2G",
    "multi-time non-Markov temporal structure",
    "history-bearing relational/action flow",
    "Process Tensor collapse to a Markov channel is forbidden",
    "Qi must not be identified with the Process Tensor itself",
    "Current-state-only prediction is forbidden",
    "observation backaction",
    "environment memory",
    "temporal correlation",
    "conventional-truth temporal substrate",
    "not ultimate truth",
    "safety-gated candidate generation",
    "not ungated execution",
    "release-chain guard only",
    "make physical-quantum-qi-deepening-checks",
    "python3 scripts/run_all_governance_full_checks_v0_1.py",
}

FORBIDDEN_PHRASES = {
    "grants execution authority",
    "grants truth authority",
    "grants proof authority",
    "ultimate truth authority",
    "ungated execution is allowed",
    "Markov reduction is acceptable",
    "current-state-only prediction is allowed",
}


def main() -> int:
    errors: list[str] = []
    if not DOC.exists():
        errors.append(f"missing document: {DOC}")
    else:
        text = DOC.read_text(encoding="utf-8")
        for phrase in sorted(REQUIRED_PHRASES):
            if phrase not in text:
                errors.append(f"missing required phrase: {phrase}")
        for phrase in sorted(FORBIDDEN_PHRASES):
            if phrase in text:
                errors.append(f"forbidden phrase present: {phrase}")

    if errors:
        print("Qi Process Tensor v0.2FG docs validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Qi Process Tensor v0.2FG docs validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
