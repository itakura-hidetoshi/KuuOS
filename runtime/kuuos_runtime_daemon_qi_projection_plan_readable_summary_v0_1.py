#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import argparse
import json
from typing import Any, Mapping


@dataclass(frozen=True)
class KuuOSQiProjectionPlanReadableSummary:
    summary_version: str
    summary_status: str
    title: str
    lines: list[str]
    recommended_next_runtime_mode: str | None
    next_tick_preparation: str | None
    required_pre_tick_actions: list[str]
    projection_statuses: dict[str, str]
    readable_summary_only: bool
    read_only: bool
    grants_execution_authority: bool = False
    grants_next_tick_execution_authority: bool = False
    grants_truth_authority: bool = False
    grants_final_commitment_authority: bool = False
    grants_memory_overwrite_authority: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def to_text(self) -> str:
        return "\n".join([self.title, *self.lines]) + "\n"


def _read_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    value = json.loads(path.read_text(encoding="utf-8"))
    return value if isinstance(value, dict) else {}


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _s(payload: Mapping[str, Any], key: str) -> str | None:
    value = payload.get(key)
    return str(value) if value is not None else None


def _lst(payload: Mapping[str, Any], key: str) -> list[str]:
    value = payload.get(key)
    return [str(item) for item in value] if isinstance(value, list) else []


def _projection_statuses(value: Any) -> dict[str, str]:
    if not isinstance(value, dict):
        return {}
    return {str(k): str(v) for k, v in value.items()}


def compile_qi_projection_plan_readable_summary(
    *,
    projection_plan_result: Mapping[str, Any] | None = None,
) -> KuuOSQiProjectionPlanReadableSummary:
    result = projection_plan_result or {}
    statuses = _projection_statuses(result.get("projection_statuses"))
    mode = _s(result, "recommended_next_runtime_mode")
    reason = _s(result, "recommended_next_reason")
    preparation = _s(result, "next_tick_preparation")
    actions = _lst(result, "required_pre_tick_actions")

    lines: list[str] = []
    lines.append(f"recommended_next_runtime_mode: {mode or 'UNKNOWN'}")
    lines.append(f"recommended_next_reason: {reason or 'UNKNOWN'}")
    lines.append(f"next_tick_preparation: {preparation or 'UNKNOWN'}")
    if actions:
        lines.append("required_pre_tick_actions:")
        lines.extend([f"- {action}" for action in actions])
    else:
        lines.append("required_pre_tick_actions: []")
    if statuses:
        lines.append("projection_statuses:")
        for key in sorted(statuses):
            lines.append(f"- {key}: {statuses[key]}")
    else:
        lines.append("projection_statuses: {}")
    lines.append("authority: none")
    lines.append("scope: readable-summary-only")

    return KuuOSQiProjectionPlanReadableSummary(
        summary_version="kuuos_runtime_daemon_qi_projection_plan_readable_summary_v0_1",
        summary_status="QI_PROJECTION_PLAN_READABLE_SUMMARY_COMPILED",
        title="Qi Routed Cycle Projection Plan — Readable Summary",
        lines=lines,
        recommended_next_runtime_mode=mode,
        next_tick_preparation=preparation,
        required_pre_tick_actions=actions,
        projection_statuses=statuses,
        readable_summary_only=True,
        read_only=True,
    )


def read_and_compile_qi_projection_plan_readable_summary(path: Path) -> KuuOSQiProjectionPlanReadableSummary:
    return compile_qi_projection_plan_readable_summary(projection_plan_result=_read_json(Path(path)))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Render KuuOS Qi projection plan readable summary v0.1")
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--write-json", type=Path, default=None)
    parser.add_argument("--write-text", type=Path, default=None)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    summary = read_and_compile_qi_projection_plan_readable_summary(args.input)
    if args.write_json:
        _write_json(args.write_json, summary.to_dict())
    if args.write_text:
        args.write_text.parent.mkdir(parents=True, exist_ok=True)
        args.write_text.write_text(summary.to_text(), encoding="utf-8")
    print(summary.to_text(), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
