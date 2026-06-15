#!/usr/bin/env python3
import pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.delayed_credit_multihorizon_v0_11_artifacts import check_artifacts
from scripts.delayed_credit_multihorizon_v0_11_scenario import run_scenario
if __name__ == "__main__":
    run_scenario()
    check_artifacts()
    print("PASS: KuuOS delayed credit multi-horizon v0.11 checks")
