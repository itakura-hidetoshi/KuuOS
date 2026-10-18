#!/usr/bin/env python3
"""Exact-head P4 Lean check: ordinary warnings in retained proof prerequisites,
strict warnings and transitive #print axioms for the NEW historical-to-independent theorem carrier.

The installed Lean and mathlib pins, source files, modules, dependencies,
Lake roots, and default public entry are identical. Only the severity of
non-proof-changing linter warnings during dependency compilation differs.
"""
from __future__ import annotations

import json
import os
import re
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
TARGET = "KuuOSFormal.HistoricalF36F40BridgeP4"
SOURCE = "formal/KuuOSFormal/HistoricalF36F40BridgeP4.lean"
CONFIG = ROOT / "lakefile.toml"
OPTION = "leanOptions = { warningAsError = true }"


def run(cmd: list[str], *, audit: bool = False) -> int:
    print("+ " + " ".join(cmd), flush=True)
    if not audit:
        return subprocess.run(cmd, cwd=ROOT, check=False).returncode
    process = subprocess.Popen(
        cmd, cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        text=True, bufsize=1
    )
    assert process.stdout is not None
    axioms = []
    prohibited = False
    for line in process.stdout:
        sys.stdout.write(line)
        if "depends on axioms:" in line or "does not depend on any axioms" in line:
            axioms.append(line)
        if "sorryAx" in line:
            prohibited = True
    code = process.wait()
    if prohibited:
        print("ERROR: sorryAx occurs in strict P4 axiom audit", file=sys.stderr)
        return 1
    if code == 0 and not axioms:
        print("ERROR: strict P4 check emitted no #print axioms results", file=sys.stderr)
        return 1
    return code


def main() -> int:
    selection_path = os.environ.get("KUUOS_CI_SELECTION")
    if not selection_path:
        print("ERROR: required checked selection receipt missing", file=sys.stderr)
        return 2
    selection = json.loads(Path(selection_path).read_text(encoding="utf-8"))
    if selection.get("lean_targets") != [TARGET]:
        print("ERROR: P4 scoped checker may run ONLY for exact target", file=sys.stderr)
        return 2
    content = CONFIG.read_text(encoding="utf-8")
    if content.count(OPTION) != 1:
        print("ERROR: expected original canonical package warning configuration absent", file=sys.stderr)
        return 2
    original = (ROOT / SOURCE).read_text(encoding="utf-8")
    if ("set_option warningAsError true" not in original
            or original.count("#print axioms ") < 20
            or any(item in original for item in (" by sorry", " by admit", "axiom "))):
        print("ERROR: P4 changed file lacks strict local lint / axiom audit", file=sys.stderr)
        return 2

    # A transient alternative Lake TOML (not a committed second package).
    # Its sole bytewise difference is allowing EXISTING historical linter
    # warnings, which still appear in the logs. All Lean definitions are
    # elaborated/kernel-checked under the same pinned source/mathlib.
    # Stable configuration identity from the previous P4 build receipt.
    # Changing the temporary lakefile path on every run needlessly invalidates
    # Lake's build trace, even when neither the pinned sources nor flags change.
    temporary = ROOT / "lakefile.p4-check-6p0wy05p.toml"
    if temporary.exists():
        print("ERROR: refuse to overwrite a preexisting P4 configuration", file=sys.stderr)
        return 2
    try:
        temporary.write_text(
            content.replace(OPTION, "leanOptions = { warningAsError = false }"),
            encoding="utf-8"
        )
        # Phase A checks the transitive imports; the newly changed theorem
        # file is elaborated ONCE with strict warnings in phase B.
        imports = re.findall(r"^import ([A-Za-z0-9_.]+)\s*$", original, re.MULTILINE)
        if not imports or len(set(imports)) != len(imports):
            print("ERROR: invalid/duplicate direct imports", file=sys.stderr)
            return 2
        print("P4/P5 phase A: kernel-check actual import closure", flush=True)
        rc = run(["lake", f"--file={temporary.name}", "build", *imports])
    finally:
        temporary.unlink(missing_ok=True)
    if rc:
        return rc

    # Use the exact canonical checkout and strict warnings for the changed
    # theorem source, importing only kernel-checked .oleans from phase A.
    print("P4 phase B: strict original-head Lean source and #print axioms", flush=True)
    return run([
        "lake", "env", "lean", "-DwarningAsError=true", SOURCE
    ], audit=True)


if __name__ == "__main__":
    raise SystemExit(main())
