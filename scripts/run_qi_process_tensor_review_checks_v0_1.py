#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
from dataclasses import asdict, dataclass
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CHECKS = [
    "scripts/check_qi_process_tensor_probe_planner_v0_1.py",
    "scripts/check_qi_process_tensor_probe_plan_artifact_writer_v0_1.py",
    "scripts/check_qi_process_tensor_probe_plan_artifact_index_v0_1.py",
    "scripts/check_qi_process_tensor_probe_plan_trend_summary_v0_1.py",
    "scripts/check_qi_process_tensor_review_flow_e2e_v0_1.py",
]


@dataclass(frozen=True)
class CheckResult:
    check_path: str
    returncode: int
    passed: bool
    stdout_tail: str
    stderr_tail: str


@dataclass(frozen=True)
class QiProcessTensorReviewCheckSuiteResult:
    suite_version: str
    suite_status: str
    check_count: int
    passed_count: int
    failed_count: int
    check_results: list[dict[str, Any]]
    suite_only: bool
    read_only: bool
    authority: str = "none"
    grants_execution_authority: bool = False
    grants_probe_execution_authority: bool = False
    grants_next_tick_execution_authority: bool = False
    grants_control_packet_authority: bool = False
    grants_memory_overwrite_authority: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def tail(value: str, limit: int = 1200) -> str:
    return value[-limit:] if len(value) > limit else value


def write_json(path: pathlib.Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def run_suite() -> QiProcessTensorReviewCheckSuiteResult:
    results: list[CheckResult] = []
    for relative in CHECKS:
        path = ROOT / relative
        if not path.is_file():
            results.append(CheckResult(relative, 127, False, "", f"missing:{relative}"))
            continue
        completed = subprocess.run([sys.executable, str(path)], cwd=str(ROOT), text=True, capture_output=True, check=False)
        results.append(CheckResult(relative, completed.returncode, completed.returncode == 0, tail(completed.stdout), tail(completed.stderr)))
    passed = sum(1 for result in results if result.passed)
    failed = len(results) - passed
    return QiProcessTensorReviewCheckSuiteResult(
        suite_version="run_qi_process_tensor_review_checks_v0_1",
        suite_status="QI_PROCESS_TENSOR_REVIEW_CHECK_SUITE_PASSED" if failed == 0 else "QI_PROCESS_TENSOR_REVIEW_CHECK_SUITE_FAILED",
        check_count=len(results),
        passed_count=passed,
        failed_count=failed,
        check_results=[asdict(result) for result in results],
        suite_only=True,
        read_only=True,
    )


def main(argv: list[str] | None = None) -> int:
    write_path = None
    if argv is None:
        argv = sys.argv[1:]
    if argv:
        if len(argv) == 2 and argv[0] == "--write-json":
            write_path = pathlib.Path(argv[1])
        else:
            print("usage: run_qi_process_tensor_review_checks_v0_1.py [--write-json PATH]", file=sys.stderr)
            return 2
    result = run_suite()
    if write_path:
        write_json(write_path, result.to_dict())
    print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if result.suite_status == "QI_PROCESS_TENSOR_REVIEW_CHECK_SUITE_PASSED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
