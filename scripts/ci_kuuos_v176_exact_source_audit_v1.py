#!/usr/bin/env python3
"""Exact v1.76 source/Lean kernel/axiom certification. No GitHub writes.

Intended for KuuOS PR #3555 only after local pinned-Sandbox Lean green.
A PR cannot earn certification from the old CodeAI candidate probes.
The caller-declared SOURCE_HEAD is provenance, not self-authenticating authority.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from scripts.kuuos_lean_mcp_repair_loop_v1 import mask_lean_comments
SOURCE = ROOT / "formal/KUOS/DependentOriginationStandardTypeABoundaryPrismRawTransfiniteV1_76.lean"
LEGACY = ROOT / "legacy/v5.291/formal/KUOS/DependentOriginationStandardTypeABoundaryPrismRawTransfiniteV1_76.lean"
MODULE = "KUOS.DependentOriginationStandardTypeABoundaryPrismRawTransfiniteV1_76"
NAMESPACE = "KUOS.DependentOriginationStandardTypeABoundaryPrismRawTransfiniteV1_76"
EXPECTED_SOURCE_BLOB = "c2aa2dff8fb981650f4fa655545c7101fa1750c8"
EXPECTED_LEGACY_BLOB = "c7fd4eb959d05a2eeb430ea39a12d04ed4030ee9"
EXPECTED_DECLARATIONS = 41
LEAN_PIN = "leanprover/lean4:v4.30.0-rc2"
MATHLIB_PIN = "5450b53e5ddc75d46418fabb605edbf36bd0beb6"
STANDARD_AXIOMS = frozenset({"propext", "Classical.choice", "Quot.sound"})
DECL_PATTERN = re.compile(
    r"(?m)^(?:@\[[^\]]+\]\s*)?(?:noncomputable\s+)?"
    r"(?:def|theorem|lemma|structure|instance|abbrev)\s+([^\s(:]+)"
)
AUDIT_PATTERN = re.compile(
    r"'(" + re.escape(NAMESPACE) + r"\.[^']+)'\s+depends on axioms:\s*\[([^\]]*)\]",
    re.S,
)
FREE_PATTERN = re.compile(
    r"'(" + re.escape(NAMESPACE) + r"\.[^']+)'\s+does not depend on any axioms",
    re.S,
)
DIAGNOSTIC = re.compile(r"(?m)^.*?\.lean:\d+:\d+:\s*(?:error|warning):")


class AuditFailure(Exception):
    pass


def blob(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def verify_inputs() -> tuple[bytes, list[str]]:
    if (ROOT / "lean-toolchain").read_text().strip() != LEAN_PIN:
        raise AuditFailure("PIN_MISMATCH lean-toolchain")
    manifest = json.loads((ROOT / "lake-manifest.json").read_text())
    mathlib = [x.get("rev") for x in manifest.get("packages", []) if x.get("name") == "mathlib"]
    if mathlib != [MATHLIB_PIN]:
        raise AuditFailure("PIN_MISMATCH mathlib")
    src = SOURCE.read_bytes()
    if blob(src) != EXPECTED_SOURCE_BLOB:
        raise AuditFailure("EXACT_SOURCE_MISMATCH " + blob(src))
    if blob(LEGACY.read_bytes()) != EXPECTED_LEGACY_BLOB:
        raise AuditFailure("LEGACY_MISMATCH")
    text = src.decode("utf8")
    no_comments = mask_lean_comments(text)
    if re.search(r"(?m)^\s*(?:sorry|admit|axiom)\b", no_comments):
        raise AuditFailure("PROOF_BYPASS")
    decls = DECL_PATTERN.findall(no_comments)
    if len(decls) != EXPECTED_DECLARATIONS or len(set(decls)) != EXPECTED_DECLARATIONS:
        raise AuditFailure("DECLARATION_INVENTORY_MISMATCH")
    return src, decls


def run_logged(cmd: list[str], log: Path, timeout: int) -> None:
    with log.open("xb") as out:
        try:
            result = subprocess.run(cmd, cwd=ROOT, stdout=out,
                                    stderr=subprocess.STDOUT, check=False,
                                    timeout=timeout)
        except subprocess.TimeoutExpired as exc:
            raise AuditFailure("NO_DATA_TIMEOUT " + " ".join(cmd[:3])) from exc
    if result.returncode:
        raise AuditFailure("LEAN_NONZERO " + str(result.returncode))
    if DIAGNOSTIC.search(log.read_text(errors="replace")):
        raise AuditFailure("LEAN_DIAGNOSTICS")


def check_axioms(log: str, decls: list[str]) -> tuple[list[str], dict[str, list[str]]]:
    reports: dict[str, list[str]] = {}
    for name, body in AUDIT_PATTERN.findall(log):
        ax = sorted(a.strip() for a in body.split(",") if a.strip())
        if name in reports and reports[name] != ax:
            raise AuditFailure("AXIOM_REPORT_CONFLICT")
        reports[name] = ax
    for name in FREE_PATTERN.findall(log):
        if name in reports and reports[name]:
            raise AuditFailure("AXIOM_REPORT_CONFLICT")
        reports[name] = []
    expected = {NAMESPACE + "." + d for d in decls}
    if set(reports) != expected or len(reports) != EXPECTED_DECLARATIONS:
        raise AuditFailure("AXIOM_NO_DATA")
    union = set(a for axioms in reports.values() for a in axioms)
    if union - STANDARD_AXIOMS or "sorryAx" in log:
        raise AuditFailure("AXIOM_OBSTRUCTION: " + ",".join(sorted(union - STANDARD_AXIOMS)))
    return sorted(union), reports


def execute(out: Path, timeout: int) -> dict:
    src, decls = verify_inputs()
    out.mkdir(parents=True, exist_ok=True)
    if list(out.iterdir()):
        raise AuditFailure("APPEND_ONLY_VIOLATION: receipt directory not empty")
    head = os.environ.get("SOURCE_HEAD")
    if not head or re.fullmatch("[a-f0-9]{40}", head) is None:
        raise AuditFailure("NO_DATA: SOURCE_HEAD not a declared 40-hex GitHub ref")
    build = ["lake", "-KleanArgs=-DwarningAsError=true",
             "-KleanArgs=-DsorryAsError=true", "build", MODULE]
    run_logged(build, out / "strict-build.log", timeout=timeout)
    with tempfile.TemporaryDirectory(prefix=".kuuos-v176-audit-", dir=ROOT) as temp:
        audit = Path(temp) / "exact-v176-41-axioms.lean"
        audit.write_text("import " + MODULE + "\n" +
                         "\n".join("#print axioms " + NAMESPACE + "." + x for x in decls) +
                         "\n", encoding="utf8")
        cmd = ["lake", "env", "lean", "-DwarningAsError=true",
               "-Dweak.sorryAsError=true", str(audit)]
        run_logged(cmd, out / "axiom-audit.log", timeout=timeout)
    used, results = check_axioms((out / "axiom-audit.log").read_text(errors="replace"), decls)
    receipt = {
        "kind": "KUUOS_V176_EXACT_SOURCE_LEAN_AUDIT_V1",
        "head": head,
        "head_authority": "GITHUB_WORKFLOW_CHECKOUT_INPUT_NOT_INDEPENDENTLY_VERIFIED_BY_THIS_SCRIPT",
        "source_blob": blob(src),
        "legacy_blob": EXPECTED_LEGACY_BLOB,
        "source_sha256": hashlib.sha256(src).hexdigest(),
        "lean_pin": LEAN_PIN,
        "mathlib_pin": MATHLIB_PIN,
        "compiled_module": MODULE,
        "public_declarations": len(decls),
        "exact_41_axiom_reports": len(results),
        "axioms": used,
        "sorryAx": False,
        "warnings": 0,
        "errors": 0,
        "strict_build": "SUCCESS",
        "independent_external_approval": "CI_JOB_PENDING_UNTIL_WORKFLOW_SUCCESS",
        "merged": False,
    }
    (out / "receipt.json").write_text(
        json.dumps(receipt, indent=2, ensure_ascii=False) + "\n", encoding="utf8"
    )
    return receipt


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--timeout-seconds", type=int, default=3600)
    args = p.parse_args()
    if not 60 <= args.timeout_seconds <= 5400:
        p.error("timeout outside bounded scope")
    try:
        receipt = execute(args.out.resolve(), args.timeout_seconds)
    except (OSError, ValueError, AuditFailure) as e:
        print("KUUOS_V176_HOLD " + json.dumps({"status":"UNAUTHENTICATED",
              "obstruction":str(e),"merged":False}), file=sys.stderr)
        return 2
    print("KUUOS_V176_EXACT_SOURCE_LOCAL_GREEN " + json.dumps(receipt, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
