#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import argparse
import json
import pathlib
from typing import Any


REQUIRED_PATH_FIELDS = [
    "raw_state_path",
    "evidence_path",
    "control_path",
]

REQUIRED_NUMERIC_FIELDS = [
    "max_outer_iterations",
    "max_daemon_ticks",
    "max_steps_per_tick",
    "requested_max_reentry_cycles",
    "sleep_seconds_between_iterations",
]


@dataclass(frozen=True)
class QiPersistentSupervisorProfileValidationResult:
    validation_version: str
    validation_status: str
    profile_path: str
    profile_version: str | None
    out_dir: str | None
    resolved_paths: dict[str, str]
    blockers: list[str]
    warnings: list[str]
    profile_only: bool
    read_only: bool
    grants_execution_authority: bool = False
    grants_next_tick_execution_authority: bool = False
    grants_truth_authority: bool = False
    grants_final_commitment_authority: bool = False
    grants_memory_overwrite_authority: bool = False
    grants_clinical_authority: bool = False
    grants_theorem_authority: bool = False
    grants_completed_identity_authority: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def read_json(path: pathlib.Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    value = json.loads(path.read_text(encoding="utf-8"))
    return value if isinstance(value, dict) else {}


def write_json(path: pathlib.Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def resolve_path(profile_dir: pathlib.Path, value: Any) -> pathlib.Path | None:
    if value is None:
        return None
    path = pathlib.Path(str(value))
    return path if path.is_absolute() else (profile_dir / path).resolve()


def numeric_value(profile: dict[str, Any], key: str, default: float) -> float:
    try:
        return float(profile.get(key, default))
    except (TypeError, ValueError):
        return default


def validate_profile(profile_path: pathlib.Path) -> QiPersistentSupervisorProfileValidationResult:
    profile_path = pathlib.Path(profile_path)
    blockers: list[str] = []
    warnings: list[str] = []
    resolved_paths: dict[str, str] = {}

    if not profile_path.is_file():
        blockers.append("profile_not_found")
        return QiPersistentSupervisorProfileValidationResult(
            validation_version="qi_persistent_supervisor_profile_validator_v0_1",
            validation_status="QI_PERSISTENT_SUPERVISOR_PROFILE_BLOCKED",
            profile_path=str(profile_path),
            profile_version=None,
            out_dir=None,
            resolved_paths={},
            blockers=blockers,
            warnings=warnings,
            profile_only=True,
            read_only=True,
        )

    profile = read_json(profile_path)
    profile_dir = profile_path.parent
    profile_version = profile.get("profile_version")
    if profile_version != "qi_persistent_supervisor_profile_v0_1":
        blockers.append("profile_version_mismatch")

    for key in REQUIRED_PATH_FIELDS:
        value = profile.get(key)
        if value is None:
            blockers.append(f"missing_field:{key}")
            continue
        resolved = resolve_path(profile_dir, value)
        if resolved is None:
            blockers.append(f"unresolvable_path:{key}")
            continue
        resolved_paths[key] = str(resolved)
        if not resolved.is_file():
            blockers.append(f"path_not_found:{key}")

    out_dir_value = profile.get("out_dir")
    if out_dir_value is None:
        blockers.append("missing_field:out_dir")
        out_dir = None
    else:
        out_dir_path = resolve_path(profile_dir, out_dir_value)
        out_dir = str(out_dir_path) if out_dir_path else None
        if out_dir_path:
            resolved_paths["out_dir"] = str(out_dir_path)

    max_outer_iterations = numeric_value(profile, "max_outer_iterations", 0)
    max_daemon_ticks = numeric_value(profile, "max_daemon_ticks", 0)
    max_steps_per_tick = numeric_value(profile, "max_steps_per_tick", 0)
    requested_max_reentry_cycles = numeric_value(profile, "requested_max_reentry_cycles", -1)
    sleep_seconds_between_iterations = numeric_value(profile, "sleep_seconds_between_iterations", -1)

    for key in REQUIRED_NUMERIC_FIELDS:
        if key not in profile:
            warnings.append(f"missing_numeric_field_using_runtime_default:{key}")
    if max_outer_iterations < 1:
        blockers.append("max_outer_iterations_below_one")
    if max_daemon_ticks < 1:
        blockers.append("max_daemon_ticks_below_one")
    if max_steps_per_tick < 1:
        blockers.append("max_steps_per_tick_below_one")
    if requested_max_reentry_cycles < 0:
        blockers.append("requested_max_reentry_cycles_below_zero")
    if sleep_seconds_between_iterations < 0:
        blockers.append("sleep_seconds_between_iterations_below_zero")

    if profile.get("authority") != "none":
        blockers.append("authority_not_none")
    if profile.get("scope") != "persistent_supervisor_profile_example":
        warnings.append("scope_not_example_profile")

    status = "QI_PERSISTENT_SUPERVISOR_PROFILE_VALID" if not blockers else "QI_PERSISTENT_SUPERVISOR_PROFILE_BLOCKED"
    return QiPersistentSupervisorProfileValidationResult(
        validation_version="qi_persistent_supervisor_profile_validator_v0_1",
        validation_status=status,
        profile_path=str(profile_path),
        profile_version=str(profile_version) if profile_version is not None else None,
        out_dir=out_dir,
        resolved_paths=resolved_paths,
        blockers=blockers,
        warnings=warnings,
        profile_only=True,
        read_only=True,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate KuuOS Qi persistent supervisor profile v0.1")
    parser.add_argument("--profile", type=pathlib.Path, required=True)
    parser.add_argument("--write", type=pathlib.Path, default=None)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    result = validate_profile(args.profile)
    if args.write:
        write_json(args.write, result.to_dict())
    print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if result.validation_status == "QI_PERSISTENT_SUPERVISOR_PROFILE_VALID" else 1


if __name__ == "__main__":
    raise SystemExit(main())
