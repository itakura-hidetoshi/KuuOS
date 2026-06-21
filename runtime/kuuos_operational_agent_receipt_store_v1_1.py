from __future__ import annotations

from copy import deepcopy
import json
import os
from pathlib import Path
from typing import Any, Mapping

from runtime.kuuos_operational_agent_types_v1_1 import copy_boundaries, sha

RECEIPT_VERSION = "kuuos_operational_agent_receipt_v1_1"


class AppendOnlyReceiptStore:
    def __init__(self, *, same_root_id: str) -> None:
        if not isinstance(same_root_id, str) or not same_root_id.strip():
            raise ValueError("same_root_id_required")
        self._same_root_id = same_root_id.strip()
        self._records: list[dict[str, Any]] = []

    @staticmethod
    def _digest(receipt: Mapping[str, Any]) -> str:
        packet = deepcopy(dict(receipt))
        packet.pop("receipt_digest", None)
        return sha(packet)

    def _build_receipt(
        self, *, record_type: str, payload: Mapping[str, Any]
    ) -> dict[str, Any]:
        if not isinstance(record_type, str) or not record_type.strip():
            raise ValueError("receipt_record_type_required")
        sequence = len(self._records) + 1
        previous = (
            self._records[-1]["receipt_digest"] if self._records else "GENESIS"
        )
        value = {
            "version": RECEIPT_VERSION,
            "sequence": sequence,
            "same_root_id": self._same_root_id,
            "record_type": record_type.strip(),
            "previous_receipt_digest": previous,
            "payload": deepcopy(dict(payload)),
            **copy_boundaries(),
            "receipt_digest": "",
        }
        value["receipt_digest"] = self._digest(value)
        return value

    def append(
        self, *, record_type: str, payload: Mapping[str, Any]
    ) -> dict[str, Any]:
        receipt = self._build_receipt(record_type=record_type, payload=payload)
        self._records.append(receipt)
        return deepcopy(receipt)

    def records(self) -> list[dict[str, Any]]:
        return deepcopy(self._records)

    def validate(self) -> list[str]:
        errors: list[str] = []
        previous = "GENESIS"
        for index, record in enumerate(self._records, start=1):
            if record.get("version") != RECEIPT_VERSION:
                errors.append(f"receipt_version_invalid:{index}")
            if record.get("sequence") != index:
                errors.append(f"receipt_sequence_invalid:{index}")
            if record.get("same_root_id") != self._same_root_id:
                errors.append(f"receipt_same_root_invalid:{index}")
            if record.get("previous_receipt_digest") != previous:
                errors.append(f"receipt_chain_invalid:{index}")
            if record.get("receipt_digest") != self._digest(record):
                errors.append(f"receipt_digest_invalid:{index}")
            previous = str(record.get("receipt_digest", ""))
        return errors


class JsonlAppendOnlyReceiptStore(AppendOnlyReceiptStore):
    def __init__(self, *, same_root_id: str, path: str | Path) -> None:
        self.path = Path(path)
        super().__init__(same_root_id=same_root_id)
        if self.path.exists():
            for line_number, line in enumerate(
                self.path.read_text(encoding="utf-8").splitlines(), start=1
            ):
                if not line.strip():
                    continue
                try:
                    value = json.loads(line)
                except json.JSONDecodeError as exc:
                    raise ValueError(
                        f"receipt_json_invalid:{line_number}:{exc.msg}"
                    ) from exc
                if not isinstance(value, dict):
                    raise ValueError(f"receipt_json_record_invalid:{line_number}")
                self._records.append(value)
            errors = self.validate()
            if errors:
                raise ValueError("receipt_chain_invalid:" + ";".join(errors))

    def append(
        self, *, record_type: str, payload: Mapping[str, Any]
    ) -> dict[str, Any]:
        receipt = self._build_receipt(record_type=record_type, payload=payload)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        encoded = json.dumps(
            receipt, ensure_ascii=False, sort_keys=True, separators=(",", ":")
        )
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(encoded + "\n")
            handle.flush()
            os.fsync(handle.fileno())
        self._records.append(receipt)
        return deepcopy(receipt)
