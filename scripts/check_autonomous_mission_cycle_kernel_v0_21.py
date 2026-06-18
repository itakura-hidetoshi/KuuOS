from runtime.v021_autonomous_mission_cycle_kernel import run_kernel


if __name__ == "__main__":
    result = run_kernel()
    if result.get("status") != "V021_AUTONOMOUS_MISSION_CYCLE_OK":
        raise SystemExit(1)
    print(result)
