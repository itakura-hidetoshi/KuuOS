#!/usr/bin/env python3
from __future__ import annotations

import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "write_qi_actuation_license_candidate_v0_1.py"
PHASE_CLI = ROOT / "scripts" / "write_qi_license_candidate_phase_v0_1.py"
PHASE_PACKET = ROOT / "packets" / "qi_process_tensor_review_phase_boundary_packet_v0_1.json"


def main() -> int:
    errors: list[str] = []
    for path in [CLI, PHASE_CLI, PHASE_PACKET]:
        if not path.is_file():
            errors.append(f"missing:{path}")
    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1

    completed = subprocess.run([sys.executable, str(CLI)], cwd=str(ROOT), text=True, capture_output=True, check=False)
    if completed.returncode != 2:
        errors.append(f"legacy_cli_returncode_should_be_2:{completed.returncode}")
    if "Deprecated legacy entrypoint" not in completed.stderr:
        errors.append("legacy_cli_deprecation_message_missing")
    if "write_qi_license_candidate_phase_v0_1.py" not in completed.stderr:
        errors.append("phase_cli_redirect_missing")
    if "qi_process_tensor_review_phase_boundary_packet_v0_1.json" not in completed.stderr:
        errors.append("phase_packet_redirect_missing")

    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1
    print("PASS: legacy Qi finality license entrypoint is deprecated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
