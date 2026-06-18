from __future__ import annotations

import json
from pathlib import Path
from tempfile import TemporaryDirectory

from runtime.kuuos_cooperative_execution_supervisor_bundle_v0_16 import find_job
from runtime.kuuos_cooperative_host_adapter_types_v0_17 import BLOCKED, READY
from runtime.kuuos_cooperative_host_adapter_v0_17 import (
    build_host_license,
    project_host_work_files,
    read_json,
    run_host_tick_files,
    write_json_atomic,
)
from runtime.v017_host_adapter_fixtures import queued_bundle, registry, steps, supervisor_policy


def main() -> bool:
    with TemporaryDirectory() as temporary:
        root = Path(temporary)
        input_bundle_path = root / "input_bundle.json"
        projection_path = root / "projection.json"
        license_path = root / "license.json"
        output_bundle_path = root / "output_bundle.json"
        receipt_path = root / "receipt.json"
        audit_path = root / "audit.jsonl"

        bundle = queued_bundle(job_id="file-job", job_steps=steps(1), policy=supervisor_policy())
        license_packet = build_host_license(
            license_id="file-license",
            issued_at_ms=1000,
            expires_at_ms=100000,
            operation_allowlist=["fixture.success"],
            max_steps_per_slice=1,
            max_cost_per_slice=1.0,
            lease_duration_ms=1000,
        )
        write_json_atomic(input_bundle_path, bundle)
        write_json_atomic(license_path, license_packet)
        input_before = input_bundle_path.read_text(encoding="utf-8")

        projection = project_host_work_files(
            supervisor_bundle_path=input_bundle_path,
            projection_output_path=projection_path,
            now_ms=2000,
            operation_allowlist=["fixture.success"],
        )
        assert projection["adapter_state"] == "work_ready"
        result = run_host_tick_files(
            supervisor_bundle_path=input_bundle_path,
            projection_path=projection_path,
            host_license_path=license_path,
            output_bundle_path=output_bundle_path,
            receipt_output_path=receipt_path,
            audit_path=audit_path,
            worker_id="worker-file",
            invocation_id="file-invocation",
            now_ms=2000,
            supervisor_policy=supervisor_policy(),
            registry=registry(),
        )
        assert result["status"] == READY
        assert input_bundle_path.read_text(encoding="utf-8") == input_before
        output_bundle = read_json(output_bundle_path)
        assert find_job(output_bundle, "file-job")["supervisor_state"] == "completed"
        receipt = read_json(receipt_path)
        assert receipt["status"] == READY
        lines = [json.loads(line) for line in audit_path.read_text(encoding="utf-8").splitlines() if line]
        assert len(lines) == 1
        assert lines[0]["adapter_state"] == "completed"

        blocked_bundle_path = root / "blocked_bundle.json"
        blocked_projection_path = root / "blocked_projection.json"
        blocked_receipt_path = root / "blocked_receipt.json"
        blocked_audit_path = root / "blocked_audit.jsonl"
        blocked_bundle = queued_bundle(job_id="in-place-block", job_steps=steps(1), policy=supervisor_policy())
        write_json_atomic(blocked_bundle_path, blocked_bundle)
        project_host_work_files(
            supervisor_bundle_path=blocked_bundle_path,
            projection_output_path=blocked_projection_path,
            now_ms=3000,
            operation_allowlist=["fixture.success"],
        )
        blocked_before = blocked_bundle_path.read_text(encoding="utf-8")
        blocked = run_host_tick_files(
            supervisor_bundle_path=blocked_bundle_path,
            projection_path=blocked_projection_path,
            host_license_path=license_path,
            output_bundle_path=blocked_bundle_path,
            receipt_output_path=blocked_receipt_path,
            audit_path=blocked_audit_path,
            worker_id="worker-file",
            invocation_id="in-place-block-invocation",
            now_ms=3000,
            supervisor_policy=supervisor_policy(),
            registry=registry(),
        )
        assert blocked["status"] == BLOCKED
        assert "in_place_bundle_write_not_allowed" in blocked["blockers"]
        assert blocked_bundle_path.read_text(encoding="utf-8") == blocked_before
    print("PASS: cooperative host adapter v0.17 file I/O")
    return True


if __name__ == "__main__":
    main()
