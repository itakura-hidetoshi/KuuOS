#!/usr/bin/env python3
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.horizon_gauge_arbitration_v0_12_artifacts import check_artifacts
from scripts.horizon_gauge_arbitration_v0_12_scenario_fixed import run_scenario

if __name__ == "__main__":
    run_scenario()
    check_artifacts()
    print("PASS: KuuOS horizon gauge arbitration v0.12 checks")
