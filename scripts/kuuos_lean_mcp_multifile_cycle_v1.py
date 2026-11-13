#!/usr/bin/env python3
"""Bounded multi-file Lean MCP repair in an explicitly isolated checkout.

Reusable v1 Lean MCP one-file loop is the only tactic/patch verification engine.
This layer manages dependency ordering, temporary .olean handoff, rechecking
all candidate bytes, independent export, and unconditional rollback.
No network model, git/gh, pull request, or repository write is performed.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import pathlib
import re
import stat
import subprocess
import sys
import tempfile
from typing import Callable

from scripts.check_kuuos_lean_lsp_mcp_compatibility_v7_17 import require_pins
from scripts.kuuos_lean_mcp_repair_loop_v1 import (
    Obstruction, digest, mcp_tactic_provider, run_loop,
)

VERSION = "kuuos_lean_mcp_multifile_cycle_v1"
SHA40 = re.compile(r"^[0-9a-f]{40}$")
SHA64 = re.compile(r"^[0-9a-f]{64}$")
MODULE = re.compile(r"^[A-Za-z][A-Za-z0-9_]*(?:\.[A-Za-z][A-Za-z0-9_]*)+$")
MAX_FILES = 4


def _safe_target(root: pathlib.Path, value: str, module: str) -> pathlib.Path:
    if not isinstance(value, str) or not value.endswith(".lean") or "\\" in value:
        raise Obstruction("invalid target path")
    path = pathlib.PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts or "." in path.parts:
        raise Obstruction("target must stay inside project root")
    if not (value.startswith("formal/KUOS/") or
            value.startswith("tests/mcp_repair_fixture/")):
        raise Obstruction("target is not in an approved isolated source area")
    dest = root / value
    if not dest.is_file() or dest.is_symlink() or not dest.resolve().is_relative_to(root):
        raise Obstruction("target must be regular, contained and non-symlinked")
    if not MODULE.fullmatch(module):
        raise Obstruction("invalid Lean module name")
    suffix = value.removeprefix("formal/").removeprefix("tests/mcp_repair_fixture/")
    if module != suffix.removesuffix(".lean").replace("/", "."):
        raise Obstruction("Lean module/path mismatch")
    return dest


def verify_manifest(root: pathlib.Path, manifest: dict) -> list[dict]:
    if not isinstance(manifest, dict) or manifest.get("version") != VERSION:
        raise Obstruction("invalid multi-file plan version")
    if not isinstance(manifest.get("source_head"), str) or not SHA40.fullmatch(manifest["source_head"]):
        raise Obstruction("source HEAD must be a real 40-hex Git commit")
    targets = manifest.get("targets")
    if not isinstance(targets, list) or not (2 <= len(targets) <= MAX_FILES):
        raise Obstruction("exactly 2..4 ordered source targets required")
    names: set[str] = set()
    paths: set[str] = set()
    validated: list[dict] = []
    for index, t in enumerate(targets):
        if not isinstance(t, dict) or set(t) != {"path", "module", "sha256", "depends_on"}:
            raise Obstruction("malformed per-file manifest entry")
        path, mod, sha = t["path"], t["module"], t["sha256"]
        if not isinstance(sha, str) or not SHA64.fullmatch(sha):
            raise Obstruction("invalid expected SHA256")
        dep = t["depends_on"]
        if not isinstance(dep, list) or len(dep) != len(set(map(str, dep))):
            raise Obstruction("invalid dependency list")
        if any(not isinstance(x, str) or x not in names for x in dep):
            raise Obstruction("not topologically ordered: dependencies must precede target")
        p = _safe_target(root, path, mod)
        if path in paths or mod in names:
            raise Obstruction("duplicate source or module")
        src = p.read_bytes()
        if digest(src) != sha:
            raise Obstruction("exact baseline SHA256 mismatch: " + path)
        imports = {line.split()[1] for line in src.decode("utf-8").splitlines()
                   if line.startswith("import ") and len(line.split()) == 2}
        for required in dep:
            if required not in imports:
                raise Obstruction("missing direct import of declared dependency: " + required)
        for previous in names:
            if previous in imports and previous not in dep:
                raise Obstruction("undeclared import dependency: " + previous)
        names.add(mod); paths.add(path)
        validated.append({
            "path": path, "module": mod, "sha256": sha,
            "depends_on": list(dep), "source": src,
            "mode": stat.S_IMODE(p.stat().st_mode),
        })
    return validated


def _olean_path(root: pathlib.Path, module: str) -> pathlib.Path:
    return root / ".lake/build/lib/lean" / pathlib.Path(*module.split(".")).with_suffix(".olean")


def compile_into_olean(root: pathlib.Path, rel_file: str, olean: pathlib.Path,
                       *, timeout_seconds: int = 180) -> dict:
    """Compile using pinned Lake. Write only to isolated worktree build artifacts."""
    olean.parent.mkdir(parents=True, exist_ok=True)
    try:
        result = subprocess.run(
            ["lake", "env", "lean", "-o", str(olean), rel_file],
            cwd=root, check=False, capture_output=True, text=True,
            timeout=timeout_seconds,
        )
        return {
            "exit_code": result.returncode, "stdout_tail": result.stdout[-1400:],
            "stderr_tail": result.stderr[-1400:],
        }
    except subprocess.TimeoutExpired:
        return {"exit_code": None, "status": "TIMEOUT"}


def run_multifile(*, root: pathlib.Path, manifest: dict, output_dir: pathlib.Path,
                  provider: Callable = mcp_tactic_provider,
                  max_iterations: int = 2, single_loop: Callable = run_loop,
                  compile_gate: Callable = compile_into_olean) -> dict:
    root = root.resolve(strict=True)
    require_pins(root)
    if max_iterations < 1 or max_iterations > 5:
        raise Obstruction("invalid per-file iteration budget")
    output = output_dir.resolve()
    if output.is_relative_to(root):
        raise Obstruction("candidate export must be outside project checkout")
    selected = verify_manifest(root, manifest)
    # No files are touched before the entire manifest has been validated.
    if not (root / "lake-manifest.json").exists():
        raise Obstruction("no pinned project manifest")
    backup: dict[pathlib.Path, tuple[bytes | None, int | None]] = {}
    for item in selected:
        src = root / item["path"]
        ol = _olean_path(root, item["module"])
        if src in backup or ol in backup:
            raise Obstruction("duplicate backup location")
        backup[src] = (src.read_bytes(), item["mode"])
        backup[ol] = (ol.read_bytes() if ol.exists() else None,
                      stat.S_IMODE(ol.stat().st_mode) if ol.exists() else None)
    record = {
        "version": VERSION, "status": "NO_DATA",
        "source_head": manifest["source_head"],
        "baseline": {t["path"]: t["sha256"] for t in selected},
        "targets": [], "validated_candidates": [],
        "source_and_olean_restored": False, "independent_ci_success": False,
        "github_write_performed": False, "provider": "injected",
    }
    output.mkdir(parents=True, exist_ok=True)
    staged: dict[str, bytes] = {}
    try:
        for item in selected:
            path = item["path"]
            pathobj = root / path
            stage = output / ("stage-" + str(len(staged)))
            stage.mkdir(parents=True, exist_ok=True)
            result = single_loop(
                root=root, rel_file=path, expected_sha256=item["sha256"],
                provider=provider, output_dir=stage, max_iterations=max_iterations,
            )
            check = {
                "path": path, "module": item["module"], "depends_on": item["depends_on"],
                "source_sha256": item["sha256"], "single_file_status": result.get("status"),
                "single_file_source_restored": result.get("source_restored"),
                "rounds": result.get("rounds", []),
            }
            record["targets"].append(check)
            if (result.get("status") != "LOCAL_LEAN_GREEN_CANDIDATE_ONLY" or
                    result.get("source_restored") is not True):
                raise Obstruction("single-file Lean MCP repair is not green: " + path)
            if pathobj.read_bytes() != item["source"]:
                raise Obstruction("single-file loop did not restore baseline source")
            candidate = (stage / "candidate.lean").read_bytes()
            source_candidate = candidate.decode("utf-8")
            if not source_candidate.startswith("import "):
                raise Obstruction("candidate source not a Lean module")
            # Single-file loop's proof-only patch policy preserves declarations.
            # Verify all dependency imports remain the same before activation.
            old_imports = [s for s in item["source"].decode("utf-8").splitlines() if s.startswith("import ")]
            new_imports = [s for s in source_candidate.splitlines() if s.startswith("import ")]
            if new_imports != old_imports:
                raise Obstruction("candidate changed imports")
            pathobj.write_bytes(candidate)
            pathobj.chmod(item["mode"])
            ol = _olean_path(root, item["module"])
            built = compile_gate(root, path, ol)
            check["dependency_olean_gate"] = built
            if built.get("exit_code") != 0 or not ol.exists():
                raise Obstruction("staged dependency compile failed: " + path)
            staged[path] = candidate
            check["candidate_sha256"] = digest(candidate)
        # A second local pass with all staged files and imports simultaneously active.
        for item in selected:
            gate = compile_gate(root, item["path"], _olean_path(root, item["module"]))
            if gate.get("exit_code") != 0:
                raise Obstruction("whole candidate closure compilation failed: " + item["path"])
        for item in selected:
            dest = output / "candidates" / item["path"]
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(staged[item["path"]])
            record["validated_candidates"].append({
                "path": item["path"], "module": item["module"],
                "candidate_sha256": digest(staged[item["path"]]),
                "source_sha256": item["sha256"],
            })
        record["status"] = "LOCAL_MULTIFILE_LEAN_GREEN_CANDIDATES_ONLY"
    except Exception as exc:
        record["status"] = "MULTIFILE_OBSTRUCTION"
        record["obstruction"] = f"{type(exc).__name__}: {str(exc)[:450]}"
    finally:
        # Every source and cached module artifact is restored or deleted exactly.
        for path, (prior, mode) in reversed(list(backup.items())):
            if prior is None:
                path.unlink(missing_ok=True)
            else:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(prior)
                if mode is not None:
                    path.chmod(mode)
        record["source_and_olean_restored"] = all(
            (path.read_bytes() == prior and
             (mode is None or stat.S_IMODE(path.stat().st_mode) == mode))
            if prior is not None else not path.exists()
            for path, (prior, mode) in backup.items()
        )
        if not record["source_and_olean_restored"]:
            record["status"] = "ROLLBACK_OBSTRUCTION"
        if record["status"] != "LOCAL_MULTIFILE_LEAN_GREEN_CANDIDATES_ONLY":
            # Never present an incomplete candidate set as promotable.
            for item in record["validated_candidates"]:
                (output / "candidates" / item["path"]).unlink(missing_ok=True)
            record["validated_candidates"] = []
        (output / "multifile_receipt.json").write_text(json.dumps(record, indent=2) + "\n")
    return record


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--source-manifest", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--provider", choices=["mcp-tactic"], default="mcp-tactic")
    parser.add_argument("--max-iterations", type=int, default=2)
    parser.add_argument("--ack-isolated-worktree", action="store_true")
    args = parser.parse_args()
    if not args.ack_isolated_worktree:
        parser.error("this tool may temporarily replace source bytes; use only in a disposable isolated checkout")
    plan = json.loads(pathlib.Path(args.source_manifest).read_text())
    result = run_multifile(
        root=pathlib.Path(args.project_root), manifest=plan,
        output_dir=pathlib.Path(args.output_dir), max_iterations=args.max_iterations,
    )
    print(json.dumps({k: v for k,v in result.items() if k != "targets"}, ensure_ascii=False))
    return 0 if (result["status"] == "LOCAL_MULTIFILE_LEAN_GREEN_CANDIDATES_ONLY" and
                 result["source_and_olean_restored"]) else 1


if __name__ == "__main__":
    sys.exit(main())
