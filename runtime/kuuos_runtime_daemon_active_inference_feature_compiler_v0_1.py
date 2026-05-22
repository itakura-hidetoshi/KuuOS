#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
import argparse
import json
from typing import Any, Mapping

NON_AUTHORITY_FLAGS = {
    "grants_execution_authority": False,
    "grants_truth_authority": False,
    "grants_final_commitment_authority": False,
    "grants_memory_overwrite_authority": False,
    "grants_clinical_authority": False,
    "grants_theorem_authority": False,
    "grants_completed_identity_authority": False,
}

@dataclass(frozen=True)
class KuuOSActiveInferenceFeatureBundle:
    compiler_version: str
    compiler_status: str
    primary_qi_process_tensor: dict[str, Any] | None
    active_inference_inputs: dict[str, Any]
    optional_lenses: dict[str, Any]
    hard_constraints: dict[str, Any]
    preference_priors: dict[str, Any]
    feature_compiler_reason: str
    missing_source_count: int
    allowed_projection: list[str]
    grants_execution_authority: bool = False
    grants_truth_authority: bool = False
    grants_final_commitment_authority: bool = False
    grants_memory_overwrite_authority: bool = False
    grants_clinical_authority: bool = False
    grants_theorem_authority: bool = False
    grants_completed_identity_authority: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _read_json(path: Path) -> dict[str, Any] | None:
    if not path.is_file():
        return None
    value = json.loads(path.read_text(encoding="utf-8"))
    return value if isinstance(value, dict) else None


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _tick_density(daemon_dir: Path) -> int:
    path = daemon_dir / "daemon_tick_log_v0_1.json"
    if not path.is_file():
        return 0
    value = json.loads(path.read_text(encoding="utf-8"))
    return len(value) if isinstance(value, list) else 0


def _latest_qi_summary_from_tick_log(daemon_dir: Path) -> dict[str, Any] | None:
    tick_log_path = daemon_dir / "daemon_tick_log_v0_1.json"
    if not tick_log_path.is_file():
        return None
    tick_log = json.loads(tick_log_path.read_text(encoding="utf-8"))
    if not isinstance(tick_log, list) or not tick_log:
        return None
    last_trace = tick_log[-1].get("step_trace_path")
    if not isinstance(last_trace, str):
        return None
    trace_path = Path(last_trace)
    if not trace_path.is_file():
        return None
    trace = json.loads(trace_path.read_text(encoding="utf-8"))
    if not isinstance(trace, list) or not trace:
        return None
    summary = trace[-1].get("qi_process_tensor_summary")
    return dict(summary) if isinstance(summary, Mapping) else None


def compile_active_inference_features(
    *,
    qi_process_tensor_summary: Mapping[str, Any] | None,
    yinyang_result: Mapping[str, Any] | None = None,
    four_image_result: Mapping[str, Any] | None = None,
    qi_policy_result: Mapping[str, Any] | None = None,
    emptiness_result: Mapping[str, Any] | None = None,
    wa_result: Mapping[str, Any] | None = None,
    tick_density: int = 0,
) -> KuuOSActiveInferenceFeatureBundle:
    qique = qi_policy_result.get("daemon_qique_gauge") if isinstance(qi_policy_result, Mapping) and isinstance(qi_policy_result.get("daemon_qique_gauge"), Mapping) else None
    missing_sources = sum(1 for source in [qi_process_tensor_summary, yinyang_result, four_image_result, qi_policy_result, emptiness_result, wa_result] if source is None)

    summary = dict(qi_process_tensor_summary) if isinstance(qi_process_tensor_summary, Mapping) else None
    visible = bool(summary.get("process_tensor_visible", False)) if summary else False
    missing_requirements = list(summary.get("missing_process_requirements", [])) if summary else ["qi_process_tensor_summary"]

    yinyang_state = yinyang_result.get("yinyang_polarity_state") if isinstance(yinyang_result, Mapping) else None
    four_phase = four_image_result.get("four_image_phase") if isinstance(four_image_result, Mapping) else None
    qi_mode = qi_policy_result.get("recommended_tick_mode") if isinstance(qi_policy_result, Mapping) else None
    qique_regime = qique.get("qique_regime") if isinstance(qique, Mapping) else None
    emptiness_action = emptiness_result.get("recommended_emptiness_action") if isinstance(emptiness_result, Mapping) else None
    wa_posture = wa_result.get("recommended_runtime_posture") if isinstance(wa_result, Mapping) else None

    hard_constraints = {
        "boundary_hard_constraint": yinyang_state == "BOUNDARY_YIN_REQUIRED" or qi_mode == "QUARANTINE_REVIEW" or emptiness_action == "HOLD_OR_QUARANTINE_NONFINAL",
        "reification_hard_constraint": emptiness_action in {"HOLD_AND_COMPACT_TRACE", "HOLD_OR_QUARANTINE_NONFINAL"},
        "observation_hard_constraint": not visible or qi_mode in {"REQUEST_MORE_EVIDENCE", "REOBSERVE_QI_PROCESS"},
        "missing_requirements": missing_requirements,
    }

    preference_priors = {
        "wa_preferred_posture": wa_posture,
        "qi_policy_prior": qi_mode,
        "avoid_nihilism": wa_posture not in {None, "HOLD_WITH_RECOVERY", "QUARANTINE_WITH_RETURN_PATH"},
        "prefer_recovery_path": wa_posture in {"HOLD_WITH_RECOVERY", "QUARANTINE_WITH_RETURN_PATH"} or four_phase == "GREATER_YIN",
        "prefer_compact_when_dense": tick_density >= 5 or four_phase == "GREATER_YANG",
    }

    active_inputs = {
        "yinyang_polarity_state": yinyang_state,
        "four_image_phase": four_phase,
        "qi_policy_mode": qi_mode,
        "qique_regime": qique_regime,
        "emptiness_action": emptiness_action,
        "wa_posture": wa_posture,
        "tick_density": tick_density,
        "missing_source_count": missing_sources,
        "process_tensor_visible": visible,
        "process_history_length": int(summary.get("process_history_length", 0) or 0) if summary else 0,
        "transition_support_count": int(summary.get("transition_support_count", 0) or 0) if summary else 0,
        "memory_support_count": int(summary.get("memory_support_count", 0) or 0) if summary else 0,
        "nonmarkov_support_count": int(summary.get("nonmarkov_support_count", 0) or 0) if summary else 0,
    }

    optional_lenses = {
        "yinyang": dict(yinyang_result) if isinstance(yinyang_result, Mapping) else None,
        "four_image": dict(four_image_result) if isinstance(four_image_result, Mapping) else None,
        "qique": dict(qique) if isinstance(qique, Mapping) else None,
        "emptiness": dict(emptiness_result) if isinstance(emptiness_result, Mapping) else None,
        "wa": dict(wa_result) if isinstance(wa_result, Mapping) else None,
    }

    status = "FEATURES_COMPILED_WITH_PRIMARY_QI" if summary else "FEATURES_COMPILED_WITHOUT_PRIMARY_QI"
    reason = "primary_qi_process_tensor_is_kernel_input_optional_lenses_are_advisory" if summary else "primary_qi_process_tensor_missing_optional_lenses_only"

    return KuuOSActiveInferenceFeatureBundle(
        compiler_version="kuuos_runtime_daemon_active_inference_feature_compiler_v0_1",
        compiler_status=status,
        primary_qi_process_tensor=summary,
        active_inference_inputs=active_inputs,
        optional_lenses=optional_lenses,
        hard_constraints=hard_constraints,
        preference_priors=preference_priors,
        feature_compiler_reason=reason,
        missing_source_count=missing_sources,
        allowed_projection=["active_inference_feature_bundle", "feature_advisory_not_policy"],
    )


def read_and_compile_active_inference_features(daemon_dir: Path) -> KuuOSActiveInferenceFeatureBundle:
    qi_summary = _latest_qi_summary_from_tick_log(daemon_dir)
    yinyang = _read_json(daemon_dir / "daemon_yinyang_polarity_result_v0_1.json")
    four = _read_json(daemon_dir / "daemon_four_image_phase_result_v0_1.json")
    policy = _read_json(daemon_dir / "daemon_qi_policy_result_v0_1.json")
    emptiness = _read_json(daemon_dir / "daemon_emptiness_gate_result_v0_1.json")
    wa = _read_json(daemon_dir / "daemon_wa_function_result_v0_1.json")
    return compile_active_inference_features(
        qi_process_tensor_summary=qi_summary,
        yinyang_result=yinyang,
        four_image_result=four,
        qi_policy_result=policy,
        emptiness_result=emptiness,
        wa_result=wa,
        tick_density=_tick_density(daemon_dir),
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Compile KuuOS Active Inference feature bundle v0.1")
    parser.add_argument("--daemon-dir", type=Path, required=True)
    parser.add_argument("--write", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    result = read_and_compile_active_inference_features(args.daemon_dir)
    if args.write:
        _write_json(args.daemon_dir / "daemon_active_inference_feature_bundle_v0_1.json", result.to_dict())
    print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
