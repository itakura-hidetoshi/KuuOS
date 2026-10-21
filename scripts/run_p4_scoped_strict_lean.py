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
import signal
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
TARGET = "KuuOSFormal.HistoricalF36F40BridgeP4"
SOURCE = "formal/KuuOSFormal/HistoricalF36F40BridgeP4.lean"
CONFIG = ROOT / "lakefile.toml"
OPTION = "leanOptions = { warningAsError = true }"


def run(cmd: list[str], *, audit: bool = False,
        build_budget_seconds: int | None = None) -> int:
    print("+ " + " ".join(cmd), flush=True)
    if not audit:
        # A first-time F47 dependency import can take longer than the
        # old 50-minute Actions ceiling. Checkpoint at a smaller budget,
        # stop ALL Lake/Lean writers, and save the valid prefix for a
        # subsequent exact-head verification. This is a failed check,
        # never a certificate of a proof that has not been elaborated.
        proc = subprocess.Popen(cmd, cwd=ROOT, start_new_session=True)
        try:
            return proc.wait(timeout=build_budget_seconds)
        except subprocess.TimeoutExpired:
            print("ERROR: historical Lean dependency build checkpoint; "
                  "terminating writers before saving reusable .lake/build",
                  file=sys.stderr, flush=True)
            try:
                os.killpg(proc.pid, signal.SIGTERM)
            except ProcessLookupError:
                pass
            try:
                proc.wait(timeout=20)
            except subprocess.TimeoutExpired:
                pass
            # The Lake parent can exit before all of its Lean children.
            # Terminate any remaining group members before archiving.
            try:
                os.killpg(proc.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            proc.wait()
            return 124
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
        requires_f47 = (
            "KUOS.DependentOriginationGrayC60MixedBoundaryThreeHomV5_195" in imports
        )
        # This runs strictly within the configured GitHub job ceiling;
        # a cold, unfinished closure remains RED, with an archived,
        # trace-checked prefix for the next iteration of the SAME PR.
        budget_minutes = 78 if requires_f47 else 42
        print(f"Historical Lean dependency build budget: {budget_minutes} min",
              flush=True)
        rc = run(["lake", f"--file={temporary.name}", "build", *imports],
                 build_budget_seconds=budget_minutes * 60)
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
