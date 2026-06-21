from __future__ import annotations

import json
import os
from copy import deepcopy
from pathlib import Path
from typing import Any, Mapping

from runtime.kuuos_qi_window_trajectory_types_v0_29 import REPORT_VERSION, report_digest


class TrajectoryLedgerError(ValueError):
    pass


class QiWindowTrajectoryLedger:
    def __init__(self, root: str | Path) -> None:
        self.root = Path(root)
        self.path = self.root / "qi-window-trajectory-ledger-v0-29.jsonl"

    @staticmethod
    def validate_report(report: Mapping[str, Any]) -> list[str]:
        errors: list[str] = []
        if report.get("version") != REPORT_VERSION:
            errors.append("report_version_invalid")
        if not isinstance(report.get("packet_id"), str) or not report.get("packet_id"):
            errors.append("packet_id_required")
        if not isinstance(report.get("source_packet_digest"), str) or not report.get("source_packet_digest"):
            errors.append("source_packet_digest_required")
        if report.get("candidate_only") is not True:
            errors.append("candidate_only_required")
        if report.get("source_history_preserved") is not True:
            errors.append("source_history_preserved_required")
        if report.get("single_decline_closed_future_window") is not False:
            errors.append("single_decline_closure_forbidden")
        if report.get("prior_visible_window_erased") is not False:
            errors.append("prior_visible_window_erasure_forbidden")
        if report.get("relapse_claimed_irreversible") is not False:
            errors.append("irreversibility_claim_forbidden")
        if report.get("prognosis_claimed") is not False:
            errors.append("prognosis_claim_forbidden")
        if report.get("treatment_route_generated") is not False:
            errors.append("treatment_route_forbidden")
        if report.get("trajectory_report_digest") != report_digest(report):
            errors.append("report_digest_invalid")
        return errors

    def initialize(self) -> None:
        self.root.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self.path.write_text("", encoding="utf-8")

    def read_all(self) -> list[dict[str, Any]]:
        self.initialize()
        result: list[dict[str, Any]] = []
        seen: set[str] = set()
        for line_number, line in enumerate(self.path.read_text(encoding="utf-8").splitlines(), start=1):
            if not line.strip():
                continue
            try:
                value = json.loads(line)
            except json.JSONDecodeError as exc:
                raise TrajectoryLedgerError(f"ledger_json_invalid:{line_number}") from exc
            if not isinstance(value, dict):
                raise TrajectoryLedgerError(f"ledger_record_invalid:{line_number}")
            errors = self.validate_report(value)
            if errors:
                raise TrajectoryLedgerError(
                    f"ledger_report_invalid:{line_number}:" + ";".join(errors)
                )
            digest = str(value["trajectory_report_digest"])
            if digest in seen:
                raise TrajectoryLedgerError(f"ledger_duplicate_digest:{line_number}")
            seen.add(digest)
            result.append(value)
        return result

    def append(self, report: Mapping[str, Any]) -> dict[str, Any]:
        self.initialize()
        errors = self.validate_report(report)
        if errors:
            raise TrajectoryLedgerError("report_invalid:" + ";".join(errors))
        existing = self.read_all()
        digest = str(report["trajectory_report_digest"])
        for value in existing:
            if value["trajectory_report_digest"] == digest:
                return {"status": "REPLAYED", "report": deepcopy(value), "ledger_count": len(existing)}
            if value["source_packet_digest"] == report["source_packet_digest"]:
                raise TrajectoryLedgerError("source_packet_already_recorded")
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(
                json.dumps(dict(report), ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"
            )
            handle.flush()
            os.fsync(handle.fileno())
        return {"status": "APPENDED", "report": deepcopy(dict(report)), "ledger_count": len(existing) + 1}


__all__ = ["QiWindowTrajectoryLedger", "TrajectoryLedgerError"]
