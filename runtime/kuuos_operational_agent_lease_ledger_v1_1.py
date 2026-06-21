from __future__ import annotations

from copy import deepcopy
import json
import os
from pathlib import Path
from typing import Any, Mapping

from runtime.kuuos_operational_agent_types_v1_1 import sha

USAGE_VERSION = "kuuos_operational_agent_lease_usage_v1_1"


class ExecutionLeaseUsageLedger:
    """Append-only lease consumption ledger. Reservation occurs before adapter call."""

    def __init__(self) -> None:
        self._records: list[dict[str, Any]] = []
        self._uses: dict[str, int] = {}
        self._idempotency_keys: set[str] = set()

    def _ingest(self, record: Mapping[str, Any]) -> None:
        packet = deepcopy(dict(record))
        errors = self.validate_record(packet)
        if errors:
            raise ValueError("lease_usage_record_invalid:" + ";".join(errors))
        lease_id = str(packet["lease_id"])
        expected = self._uses.get(lease_id, 0) + 1
        if packet["use_index"] != expected:
            raise ValueError("lease_usage_sequence_invalid")
        key = str(packet["idempotency_key"])
        if key in self._idempotency_keys:
            raise ValueError("lease_usage_idempotency_replay")
        self._uses[lease_id] = expected
        self._idempotency_keys.add(key)
        self._records.append(packet)

    @staticmethod
    def validate_record(record: Mapping[str, Any]) -> list[str]:
        errors: list[str] = []
        if record.get("version") != USAGE_VERSION:
            errors.append("lease_usage_version_invalid")
        for field in ("lease_id", "intent_id", "idempotency_key", "session_digest"):
            if not isinstance(record.get(field), str) or not record.get(field):
                errors.append(f"lease_usage_{field}_invalid")
        if (
            isinstance(record.get("use_index"), bool)
            or not isinstance(record.get("use_index"), int)
            or record.get("use_index", 0) < 1
        ):
            errors.append("lease_usage_use_index_invalid")
        expected_digest = sha(
            {key: value for key, value in record.items() if key != "usage_digest"}
        )
        if record.get("usage_digest") != expected_digest:
            errors.append("lease_usage_digest_invalid")
        return errors

    def used(self, lease_id: str) -> int:
        return self._uses.get(lease_id, 0)

    def can_consume(
        self, lease: Mapping[str, Any], intent: Mapping[str, Any]
    ) -> list[str]:
        errors: list[str] = []
        lease_id = str(lease.get("lease_id", ""))
        key = str(intent.get("idempotency_key", ""))
        if key in self._idempotency_keys:
            errors.append("intent_replay_forbidden")
        if self.used(lease_id) >= int(lease.get("max_uses", 0)):
            errors.append("lease_use_limit_exhausted")
        return errors

    def reserve(
        self,
        *,
        lease: Mapping[str, Any],
        intent: Mapping[str, Any],
        session_digest: str,
    ) -> dict[str, Any]:
        errors = self.can_consume(lease, intent)
        if errors:
            raise ValueError("lease_reservation_denied:" + ";".join(errors))
        lease_id = str(lease["lease_id"])
        record = {
            "version": USAGE_VERSION,
            "lease_id": lease_id,
            "intent_id": str(intent["intent_id"]),
            "idempotency_key": str(intent["idempotency_key"]),
            "session_digest": session_digest,
            "use_index": self.used(lease_id) + 1,
            "usage_digest": "",
        }
        record["usage_digest"] = sha(
            {key: value for key, value in record.items() if key != "usage_digest"}
        )
        self._ingest(record)
        return deepcopy(record)

    def records(self) -> list[dict[str, Any]]:
        return deepcopy(self._records)


class JsonlExecutionLeaseUsageLedger(ExecutionLeaseUsageLedger):
    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        super().__init__()
        if self.path.exists():
            for line_number, line in enumerate(
                self.path.read_text(encoding="utf-8").splitlines(), start=1
            ):
                if not line.strip():
                    continue
                try:
                    record = json.loads(line)
                except json.JSONDecodeError as exc:
                    raise ValueError(
                        f"lease_usage_json_invalid:{line_number}:{exc.msg}"
                    ) from exc
                if not isinstance(record, dict):
                    raise ValueError(
                        f"lease_usage_json_record_invalid:{line_number}"
                    )
                self._ingest(record)

    def reserve(
        self,
        *,
        lease: Mapping[str, Any],
        intent: Mapping[str, Any],
        session_digest: str,
    ) -> dict[str, Any]:
        record = super().reserve(
            lease=lease, intent=intent, session_digest=session_digest
        )
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(
                json.dumps(
                    record, ensure_ascii=False, sort_keys=True, separators=(",", ":")
                )
                + "\n"
            )
            handle.flush()
            os.fsync(handle.fileno())
        return record
