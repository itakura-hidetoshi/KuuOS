#!/usr/bin/env python3
from __future__ import annotations

import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
INDEX = ROOT / "docs" / "KUSTRING_RUNTIME_CHAIN_INDEX_v0_2.md"
FINALITY = ROOT / "docs" / "KUSTRING_RUNTIME_FINALITY_PACKET_v0_2.md"
LEDGER = ROOT / "docs" / "kustring_runtime_finality_ci_ledger_v0_2.md"

REQUIRED_FILES = [INDEX, FINALITY, LEDGER]

INDEX_TOKENS = [
    "KuString Runtime Chain Index v0.2",
    "examples/kustring_runtime_v0_2.py",
    "tests/test_kustring_runtime_v0_2.py",
    "scripts/eval_kustring_runtime_packets_v0_2.py",
    "scripts/export_kustring_runtime_audit_v0_2.py",
    "scripts/build_kustring_runtime_audit_chain_v0_2.py",
    "scripts/export_kustring_runtime_worm_receipt_v0_2.py",
    "scripts/build_kustring_runtime_bundle_v0_2.py",
    "scripts/build_kustring_runtime_attestation_v0_2.py",
    "docs/KUSTRING_RUNTIME_CLOSURE_PACKET_v0_2.md",
    "docs/KUSTRING_RUNTIME_FINALITY_PACKET_v0_2.md",
    "docs/kustring_runtime_finality_ci_ledger_v0_2.md",
    "Workflow run ID: `25960729451`",
    "Workflow job ID: `76315481134`",
    "Head SHA: `8eae6d696b6128cfecb71430b19123ca6ed43003`",
    "Artifact digest: `sha256:6f6bb5e4f204cbd63334625cc2295b54b33d10eddf610ce666547047fd0985ad`",
    "implementation-level runtime finality only",
    "proof authority",
    "truth authority",
    "clinical authority",
    "execution authority",
    "governance-bypass authority",
    "Append-only rule",
]

FINALITY_TOKENS = [
    "runtime finality CI ledger",
    "runtime finality report artifact",
    "Ledger: docs/kustring_runtime_finality_ci_ledger_v0_2.md",
    "Workflow run ID: `25960729451`",
    "Workflow job ID: `76315481134`",
    "Artifact digest: `sha256:6f6bb5e4f204cbd63334625cc2295b54b33d10eddf610ce666547047fd0985ad`",
    "does not grant proof authority, truth authority, clinical authority, execution authority, or governance-bypass authority",
]

LEDGER_TOKENS = [
    "Status: CI green",
    "Workflow run ID: `25960729451`",
    "Workflow job ID: `76315481134`",
    "Head SHA: `8eae6d696b6128cfecb71430b19123ca6ed43003`",
    "Result: `success`",
    "Artifact digest: `sha256:6f6bb5e4f204cbd63334625cc2295b54b33d10eddf610ce666547047fd0985ad`",
    "proof authority",
    "truth authority",
    "clinical authority",
    "execution authority",
]

FORBIDDEN_POSITIVE_ASSERTIONS = [
    "proof_authority_granted: true",
    "truth_authority_granted: true",
    "clinical_authority_granted: true",
    "execution_authority_granted: true",
    "governance_bypass_authority_granted: true",
    "CI success grants execution authority",
    "CI success is theorem truth",
]


def require_tokens(label: str, text: str, tokens: list[str], errors: list[str]) -> None:
    for token in tokens:
        if token not in text:
            errors.append(f"{label} missing: {token}")


def main() -> int:
    errors: list[str] = []
    for path in REQUIRED_FILES:
        if not path.is_file():
            errors.append(f"missing file: {path.relative_to(ROOT)}")

    index_text = INDEX.read_text(encoding="utf-8") if INDEX.is_file() else ""
    finality_text = FINALITY.read_text(encoding="utf-8") if FINALITY.is_file() else ""
    ledger_text = LEDGER.read_text(encoding="utf-8") if LEDGER.is_file() else ""

    require_tokens("chain index", index_text, INDEX_TOKENS, errors)
    require_tokens("finality packet", finality_text, FINALITY_TOKENS, errors)
    require_tokens("CI ledger", ledger_text, LEDGER_TOKENS, errors)

    for label, text in [
        ("chain index", index_text),
        ("finality packet", finality_text),
        ("CI ledger", ledger_text),
    ]:
        for token in FORBIDDEN_POSITIVE_ASSERTIONS:
            if token in text:
                errors.append(f"{label} forbidden positive assertion: {token}")

    if errors:
        for err in errors:
            print("ERROR:", err)
        return 1

    print("PASS: KuString runtime chain index checked")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
