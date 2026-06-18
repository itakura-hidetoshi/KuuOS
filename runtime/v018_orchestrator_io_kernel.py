from __future__ import annotations

import json
from pathlib import Path
from tempfile import TemporaryDirectory

from runtime.kuuos_cooperative_execution_supervisor_bundle_v0_16 import find_job
from runtime.kuuos_durable_host_orchestrator_types_v0_18 import BLOCKED, READY
from runtime.kuuos_durable_host_orchestrator_v0_18 import (
    build_orchestrator_plan_files,
    read_json,
    run_orchestrator_cycle_files,
    write_json_atomic,
)
from runtime.v018_orchestrator_fixtures import (
    fixture_state,
    healthy_workers,
    host_license,
    orchestrator_policy,
    queued_jobs_bundle,
    registry,
    supervisor_policy,
)


def _write_list(path: Path, values) -> None:
    path.write_text(json.dumps(values, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> bool:
    with TemporaryDirectory() as temporary:
        root = Path(temporary)
        supervisor_input = root / "supervisor-input.json"
        state_input = root / "orchestrator-input.json"
        workers_path = root / "workers.json"
        license_path = root / "host-license.json"
        policy_path = root / "orchestrator-policy.json"
        plan_path = root / "plan.json"
        supervisor_output = root / "supervisor-output.json"
        state_output = root / "orchestrator-output.json"
        receipt_path = root / "receipt.json"
        audit_path = root / "audit.jsonl"

        bundle = queued_jobs_bundle([("file-job", 1, "fixture.success")])
        state = fixture_state()
        workers = healthy_workers()[:1]
        license_packet = host_license()
        policy = orchestrator_policy(max_assignments_per_cycle=1)
        write_json_atomic(supervisor_input, bundle)
        write_json_atomic(state_input, state)
        _write_list(workers_path, workers)
        write_json_atomic(license_path, license_packet)
        write_json_atomic(policy_path, policy)
        supervisor_before = supervisor_input.read_text(encoding="utf-8")
        state_before = state_input.read_text(encoding="utf-8")

        plan = build_orchestrator_plan_files(
            cycle_id="file-cycle",
            supervisor_bundle_path=supervisor_input,
            orchestrator_state_path=state_input,
            worker_reports_path=workers_path,
            host_license_path=license_path,
            policy_path=policy_path,
            plan_output_path=plan_path,
            registry=registry(),
            now_ms=2000,
        )
        assert plan["dispatch_capacity"] == 1
        result = run_orchestrator_cycle_files(
            supervisor_bundle_path=supervisor_input,
            orchestrator_state_path=state_input,
            plan_path=plan_path,
            worker_reports_path=workers_path,
            host_license_path=license_path,
            policy_path=policy_path,
            supervisor_output_path=supervisor_output,
            orchestrator_output_path=state_output,
            receipt_output_path=receipt_path,
            audit_path=audit_path,
            supervisor_policy=supervisor_policy(),
            registry=registry(),
            now_ms=2000,
        )
        assert result["status"] == READY
        assert supervisor_input.read_text(encoding="utf-8") == supervisor_before
        assert state_input.read_text(encoding="utf-8") == state_before
        assert find_job(read_json(supervisor_output), "file-job")["supervisor_state"] == "completed"
        assert read_json(state_output)["cycle_index"] == 1
        assert read_json(receipt_path)["assignment_count"] == 1
        audit_entries = [json.loads(line) for line in audit_path.read_text(encoding="utf-8").splitlines() if line]
        assert len(audit_entries) == 1
        assert audit_entries[0]["cycle_id"] == "file-cycle"

        blocked_receipt = root / "blocked-receipt.json"
        blocked_audit = root / "blocked-audit.jsonl"
        blocked = run_orchestrator_cycle_files(
            supervisor_bundle_path=supervisor_input,
            orchestrator_state_path=state_input,
            plan_path=plan_path,
            worker_reports_path=workers_path,
            host_license_path=license_path,
            policy_path=policy_path,
            supervisor_output_path=supervisor_input,
            orchestrator_output_path=state_input,
            receipt_output_path=blocked_receipt,
            audit_path=blocked_audit,
            supervisor_policy=supervisor_policy(),
            registry=registry(),
            now_ms=2000,
        )
        assert blocked["status"] == BLOCKED
        assert "in_place_supervisor_write_not_allowed" in blocked["blockers"]
        assert "in_place_orchestrator_write_not_allowed" in blocked["blockers"]
        assert supervisor_input.read_text(encoding="utf-8") == supervisor_before
        assert state_input.read_text(encoding="utf-8") == state_before
    print("PASS: durable host orchestrator v0.18 file I/O")
    return True


if __name__ == "__main__":
    main()
