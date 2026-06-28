#!/usr/bin/env python3
"""Build the single human and machine audit entry point for a CI run."""

from __future__ import annotations

import argparse
import json
import pathlib
import sys
from typing import Any


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--selection", type=pathlib.Path, required=True)
    parser.add_argument("--receipts-root", type=pathlib.Path, required=True)
    parser.add_argument("--output-dir", type=pathlib.Path, required=True)
    parser.add_argument("--python-result", default="unknown")
    parser.add_argument("--lean-result", default="unknown")
    return parser.parse_args()


def load_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def collect_receipts(root: pathlib.Path) -> dict[str, dict[str, Any]]:
    receipts: dict[str, dict[str, Any]] = {}
    if not root.exists():
        return receipts
    for path in sorted(root.rglob("receipt.json")):
        try:
            receipt = load_json(path)
        except (OSError, json.JSONDecodeError) as exc:
            print(f"WARNING: cannot read receipt {path}: {exc}", file=sys.stderr)
            continue
        check_id = receipt.get("check_id")
        if isinstance(check_id, str) and check_id:
            receipts[check_id] = receipt
    return receipts


def markdown_report(summary: dict[str, Any]) -> str:
    lines = [
        "# KuuOS CI audit report",
        "",
        f"**Overall status:** `{summary['status']}`",
        "",
        "Validation is structural evidence only. CI success is not truth, theorem authority, institutional approval, or execution authority.",
        "",
        "## Selection",
        "",
        f"- Full audit required: `{str(summary['full_audit_required']).lower()}`",
        f"- Changed paths: `{len(summary['changed_paths'])}`",
        f"- Selected checks: `{len(summary['expected_checks'])}`",
    ]
    reasons = summary.get("reasons", [])
    if reasons:
        lines.append("- Reasons: " + "; ".join(str(item) for item in reasons))

    lines.extend(["", "## Check results", "", "| Check | Status | Duration | Return code |", "|---|---:|---:|---:|"])
    for item in summary["check_results"]:
        duration = item.get("duration_seconds")
        duration_text = "-" if duration is None else f"{duration:.3f}s"
        return_code = item.get("return_code")
        return_text = "-" if return_code is None else str(return_code)
        lines.append(
            f"| `{item['check_id']}` | `{item['status']}` | {duration_text} | {return_text} |"
        )

    if summary["missing_receipts"]:
        lines.extend(["", "## Missing receipts", ""])
        lines.extend(f"- `{check_id}`" for check_id in summary["missing_receipts"])

    if summary["unknown_paths"]:
        lines.extend(["", "## Unclassified paths", ""])
        lines.extend(f"- `{path}`" for path in summary["unknown_paths"])

    lines.extend(["", "## Boundaries", ""])
    lines.extend(f"- {boundary}" for boundary in summary.get("boundaries", []))
    return "\n".join(lines) + "\n"


def main() -> int:
    args = parse_args()
    try:
        selection = load_json(args.selection)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: cannot load selection: {exc}", file=sys.stderr)
        return 2

    receipts = collect_receipts(args.receipts_root)
    expected_checks = [item["id"] for item in selection.get("selected_checks", [])]
    missing = sorted(set(expected_checks) - set(receipts))
    failed = sorted(
        check_id for check_id, receipt in receipts.items() if receipt.get("status") != "passed"
    )

    check_results: list[dict[str, Any]] = []
    for check_id in expected_checks:
        receipt = receipts.get(check_id)
        if receipt is None:
            check_results.append(
                {
                    "check_id": check_id,
                    "status": "missing",
                    "duration_seconds": None,
                    "return_code": None,
                }
            )
        else:
            check_results.append(
                {
                    "check_id": check_id,
                    "status": receipt.get("status", "unknown"),
                    "duration_seconds": receipt.get("duration_seconds"),
                    "return_code": receipt.get("return_code"),
                    "input_digest": receipt.get("input_digest"),
                    "validator_digest": receipt.get("validator_digest"),
                }
            )

    workflow_failures = [
        name
        for name, result in (
            ("python-checks", args.python_result),
            ("lean-formal", args.lean_result),
        )
        if result in {"failure", "cancelled", "timed_out", "action_required"}
    ]
    status = "passed" if not (missing or failed or workflow_failures) else "failed"

    summary: dict[str, Any] = {
        "schema_version": "0.1",
        "status": status,
        "full_audit_required": bool(selection.get("full_audit_required", False)),
        "changed_paths": selection.get("changed_paths", []),
        "direct_checks": selection.get("direct_checks", []),
        "expected_checks": expected_checks,
        "check_results": check_results,
        "missing_receipts": missing,
        "failed_checks": failed,
        "workflow_failures": workflow_failures,
        "unknown_paths": selection.get("unknown_paths", []),
        "reasons": selection.get("reasons", []),
        "boundaries": selection.get("boundaries", []),
    }

    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "audit-summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (args.output_dir / "audit-report.md").write_text(
        markdown_report(summary),
        encoding="utf-8",
    )
    print(markdown_report(summary))
    return 0 if status == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
