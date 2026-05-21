#!/usr/bin/env python3
"""KuuOS State IO Runner v0.1.

File-based runner for the bounded KuuOS closed loop driver.

It reads:
  - raw Qi/OS state JSON
  - evidence JSON or evidence sequence JSON
  - optional state bundle JSON

It writes:
  - full driver result JSON
  - next raw Qi/OS state JSON
  - updated state bundle JSON
  - step trace JSON

This runner does not execute actions, finalize truth, overwrite memory, prove
anything, make clinical decisions, or create completed OS identity.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
import argparse
import json
import sys
from typing import Any, Mapping

try:
    from runtime.kuuos_closed_loop_driver_v0_1 import run_closed_loop_driver
except ModuleNotFoundError:  # direct script execution from runtime/
    from kuuos_closed_loop_driver_v0_1 import run_closed_loop_driver


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
class KuuOSStateIORunManifest:
    run_status: str
    stop_reason: str
    steps_run: int
    raw_state_path: str
    evidence_path: str
    input_state_bundle_path: str | None
    result_path: str
    next_raw_state_path: str
    state_bundle_path: str
    step_trace_path: str
    grants_execution_authority: bool = False
    grants_truth_authority: bool = False
    grants_final_commitment_authority: bool = False
    grants_memory_overwrite_authority: bool = False
    grants_clinical_authority: bool = False
    grants_theorem_authority: bool = False
    grants_completed_identity_authority: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _read_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write("\n")


def run_state_io(
    *,
    raw_state_path: Path,
    evidence_path: Path,
    output_dir: Path,
    max_steps: int,
    state_bundle_path: Path | None = None,
) -> KuuOSStateIORunManifest:
    raw_state = _read_json(raw_state_path)
    evidence = _read_json(evidence_path)
    state_bundle = _read_json(state_bundle_path) if state_bundle_path else None

    result = run_closed_loop_driver(raw_state, evidence, max_steps=max_steps, state_bundle=state_bundle)
    result_dict = result.to_dict()

    result_path = output_dir / "kuuos_driver_result_v0_1.json"
    next_raw_state_path = output_dir / "next_raw_state_v0_1.json"
    updated_state_bundle_path = output_dir / "state_bundle_v0_1.json"
    step_trace_path = output_dir / "step_trace_v0_1.json"

    _write_json(result_path, result_dict)
    _write_json(next_raw_state_path, result.final_raw_state)
    _write_json(updated_state_bundle_path, result.final_state_bundle)
    _write_json(step_trace_path, result.step_trace)

    manifest = KuuOSStateIORunManifest(
        run_status=result.driver_status,
        stop_reason=result.stop_reason,
        steps_run=result.steps_run,
        raw_state_path=str(raw_state_path),
        evidence_path=str(evidence_path),
        input_state_bundle_path=str(state_bundle_path) if state_bundle_path else None,
        result_path=str(result_path),
        next_raw_state_path=str(next_raw_state_path),
        state_bundle_path=str(updated_state_bundle_path),
        step_trace_path=str(step_trace_path),
    )
    _write_json(output_dir / "run_manifest_v0_1.json", manifest.to_dict())
    return manifest


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run bounded KuuOS state IO loop v0.1")
    parser.add_argument("--raw-state", required=True, type=Path)
    parser.add_argument("--evidence", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--max-steps", type=int, default=3)
    parser.add_argument("--state-bundle", type=Path, default=None)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    manifest = run_state_io(
        raw_state_path=args.raw_state,
        evidence_path=args.evidence,
        output_dir=args.output_dir,
        max_steps=args.max_steps,
        state_bundle_path=args.state_bundle,
    )
    print(json.dumps(manifest.to_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
