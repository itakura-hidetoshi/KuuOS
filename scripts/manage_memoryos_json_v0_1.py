#!/usr/bin/env python3
"""
KuuOS / MemoryOS JSON Management v0.1

Purpose:
  - Validate repository JSON without converting CI into authority.
  - Detect invalid JSON and duplicate object keys.
  - Emit canonicalization candidates and a machine-readable report.
  - Preserve MemoryOS boundary vocabulary as visible policy, not as execution authority.

Boundary:
  CI pass != theorem authority
  JSON validity != truth
  Memory persistence != belief sovereignty
  Canonical rendering != destructive rewrite
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple


DEFAULT_IGNORE_DIRS = {
    ".git",
    ".github/actions-cache",
    ".kuos_json_report",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".venv",
    "__pycache__",
    "build",
    "dist",
    "node_modules",
    "site-packages",
}

REQUIRED_MEMORYOS_INVARIANTS = [
    "append_only",
    "same_root_required",
    "lineage_preserved",
    "uncertainty_visibility_required",
    "grave_is_non_destructive",
    "no_blind_promotion",
    "no_hidden_uncertainty",
    "no_destructive_deletion",
    "no_repair_to_governance_direct_jump",
    "reconstructive_recall_not_world_rewrite",
    "compressed_memory_non_authoritative",
    "filesystem_obstruction_visible_not_silent_failure",
]

AUTHORITY_BOUNDARY = {
    "json_validity": "not_truth_authority",
    "ci_pass": "not_theorem_authority",
    "memory_persistence": "not_belief_sovereignty",
    "canonical_rendering": "not_destructive_rewrite",
    "github_artifact": "not_worm_storage",
}


class DuplicateKeyError(ValueError):
    pass


def no_duplicate_object_pairs_hook(pairs: List[Tuple[str, Any]]) -> Dict[str, Any]:
    obj: Dict[str, Any] = {}
    seen = set()
    duplicates: List[str] = []
    for key, value in pairs:
        if key in seen:
            duplicates.append(key)
        seen.add(key)
        obj[key] = value
    if duplicates:
        joined = ", ".join(sorted(set(duplicates)))
        raise DuplicateKeyError(f"duplicate JSON object key(s): {joined}")
    return obj


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def canonical_json(data: Any) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def load_json_no_duplicates(path: Path) -> Any:
    text = path.read_text(encoding="utf-8")
    return json.loads(text, object_pairs_hook=no_duplicate_object_pairs_hook)


def should_ignore(path: Path, root: Path) -> bool:
    try:
        rel_parts = path.relative_to(root).parts
    except ValueError:
        rel_parts = path.parts
    return any(part in DEFAULT_IGNORE_DIRS for part in rel_parts)


def iter_json_files(root: Path) -> Iterable[Path]:
    for dirpath, dirnames, filenames in os.walk(root):
        current = Path(dirpath)
        dirnames[:] = [d for d in dirnames if d not in DEFAULT_IGNORE_DIRS]
        if should_ignore(current, root):
            continue
        for filename in filenames:
            if filename.endswith(".json"):
                candidate = current / filename
                if not should_ignore(candidate, root):
                    yield candidate


@dataclass
class FileCheck:
    path: str
    status: str
    sha256: str | None = None
    root_type: str | None = None
    canonical_sha256: str | None = None
    canonical_matches: bool | None = None
    size_bytes: int | None = None
    error_type: str | None = None
    error: str | None = None


def check_file(path: Path, root: Path, check_canonical: bool) -> FileCheck:
    rel = path.relative_to(root).as_posix()
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        return FileCheck(path=rel, status="FAIL", error_type="utf8_decode_error", error=str(exc))

    try:
        data = json.loads(text, object_pairs_hook=no_duplicate_object_pairs_hook)
    except DuplicateKeyError as exc:
        return FileCheck(
            path=rel,
            status="FAIL",
            sha256=sha256_text(text),
            size_bytes=path.stat().st_size,
            error_type="duplicate_key",
            error=str(exc),
        )
    except json.JSONDecodeError as exc:
        return FileCheck(
            path=rel,
            status="FAIL",
            sha256=sha256_text(text),
            size_bytes=path.stat().st_size,
            error_type="json_decode_error",
            error=f"{exc.msg} at line {exc.lineno}, column {exc.colno}",
        )

    rendered = canonical_json(data)
    matches = rendered == text
    status = "PASS" if (matches or not check_canonical) else "FAIL"
    return FileCheck(
        path=rel,
        status=status,
        sha256=sha256_text(text),
        root_type=type(data).__name__,
        canonical_sha256=sha256_text(rendered),
        canonical_matches=matches,
        size_bytes=path.stat().st_size,
        error_type=(None if status == "PASS" else "canonical_mismatch"),
        error=(None if status == "PASS" else "JSON is valid but not in canonical sorted-key two-space rendering"),
    )


def load_manifest(root: Path) -> Tuple[Dict[str, Any] | None, str | None]:
    manifest_path = root / "manifests" / "memoryos_json_management_manifest_v0_1.json"
    if not manifest_path.exists():
        return None, "manifest_missing"
    try:
        return load_json_no_duplicates(manifest_path), None
    except Exception as exc:  # noqa: BLE001 - report exact obstruction, do not hide it.
        return None, f"manifest_unreadable: {exc}"


def flatten_strings(value: Any) -> List[str]:
    found: List[str] = []
    if isinstance(value, str):
        found.append(value)
    elif isinstance(value, list):
        for item in value:
            found.extend(flatten_strings(item))
    elif isinstance(value, dict):
        for key, item in value.items():
            found.append(str(key))
            found.extend(flatten_strings(item))
    return found


def memoryos_policy_report(manifest: Dict[str, Any] | None, manifest_error: str | None) -> Dict[str, Any]:
    if manifest is None:
        return {
            "status": "WARN",
            "manifest_status": manifest_error,
            "required_invariants": REQUIRED_MEMORYOS_INVARIANTS,
            "present_invariants": [],
            "missing_invariants": REQUIRED_MEMORYOS_INVARIANTS,
            "authority_boundary": AUTHORITY_BOUNDARY,
        }

    strings = set(flatten_strings(manifest))
    present = [item for item in REQUIRED_MEMORYOS_INVARIANTS if item in strings]
    missing = [item for item in REQUIRED_MEMORYOS_INVARIANTS if item not in strings]
    return {
        "status": "PASS" if not missing else "FAIL",
        "manifest_status": "present",
        "required_invariants": REQUIRED_MEMORYOS_INVARIANTS,
        "present_invariants": present,
        "missing_invariants": missing,
        "authority_boundary": manifest.get("authority_boundary", AUTHORITY_BOUNDARY),
    }


def write_report(out_dir: Path, report: Dict[str, Any], canonical_candidates: Dict[str, str]) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "memoryos_json_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    candidate_dir = out_dir / "canonical_candidates"
    candidate_dir.mkdir(parents=True, exist_ok=True)
    for rel_path, rendered in canonical_candidates.items():
        safe_name = rel_path.replace("/", "__")
        (candidate_dir / safe_name).write_text(rendered, encoding="utf-8")


def build_report(root: Path, out_dir: Path, strict: bool, check_canonical: bool) -> Dict[str, Any]:
    manifest, manifest_error = load_manifest(root)
    policy = memoryos_policy_report(manifest, manifest_error)

    checks: List[FileCheck] = []
    canonical_candidates: Dict[str, str] = {}
    for path in sorted(iter_json_files(root)):
        check = check_file(path, root, check_canonical=check_canonical)
        checks.append(check)
        if check.canonical_matches is False and check.error_type == "canonical_mismatch":
            try:
                data = load_json_no_duplicates(path)
                canonical_candidates[check.path] = canonical_json(data)
            except Exception:
                pass

    parse_fail_count = sum(1 for item in checks if item.error_type == "json_decode_error")
    duplicate_key_fail_count = sum(1 for item in checks if item.error_type == "duplicate_key")
    utf8_fail_count = sum(1 for item in checks if item.error_type == "utf8_decode_error")
    canonical_mismatch_count = sum(1 for item in checks if item.canonical_matches is False)
    failed_files = [asdict(item) for item in checks if item.status == "FAIL"]

    hard_fail = bool(parse_fail_count or duplicate_key_fail_count or utf8_fail_count)
    if check_canonical and canonical_mismatch_count:
        hard_fail = True
    if strict and policy["status"] == "FAIL":
        hard_fail = True

    report: Dict[str, Any] = {
        "schema": "kuos.memoryos.json_management.report.v0_1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "status": "FAIL" if hard_fail else "PASS",
        "strict": strict,
        "check_canonical": check_canonical,
        "root": str(root),
        "summary": {
            "files_checked": len(checks),
            "parse_fail_count": parse_fail_count,
            "duplicate_key_fail_count": duplicate_key_fail_count,
            "utf8_fail_count": utf8_fail_count,
            "canonical_mismatch_count": canonical_mismatch_count,
            "failed_file_count": len(failed_files),
        },
        "memoryos_policy": policy,
        "authority_boundary": AUTHORITY_BOUNDARY,
        "files": [asdict(item) for item in checks],
        "failed_files": failed_files,
    }

    write_report(out_dir, report, canonical_candidates)
    return report


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Manage and validate KuuOS MemoryOS-facing JSON files.")
    parser.add_argument("--root", default=".", help="Repository root")
    parser.add_argument("--out-dir", default=".kuos_json_report", help="Report output directory")
    parser.add_argument("--strict", type=int, default=1, choices=[0, 1], help="Fail on MemoryOS policy regression")
    parser.add_argument(
        "--check-canonical",
        type=int,
        default=0,
        choices=[0, 1],
        help="Fail if JSON is valid but not canonical sorted-key two-space rendering",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.root).resolve()
    out_dir = Path(args.out_dir)
    if not out_dir.is_absolute():
        out_dir = root / out_dir

    report = build_report(
        root=root,
        out_dir=out_dir,
        strict=bool(args.strict),
        check_canonical=bool(args.check_canonical),
    )
    print(json.dumps({"status": report["status"], "summary": report["summary"]}, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
