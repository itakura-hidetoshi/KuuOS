from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Mapping

from runtime.kuuos_qi_candidate_lineage_envelope_verify_v0_29 import envelope_is_valid


class CandidateLineageLedger:
    def __init__(self, root: str | Path) -> None:
        self.root = Path(root)
        self.path = self.root / "qi-candidate-lineage-ledger-v0-29.jsonl"

    def initialize(self) -> None:
        self.root.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self.path.write_text("", encoding="utf-8")

    def read_all(self) -> list[dict[str, Any]]:
        self.initialize()
        records: list[dict[str, Any]] = []
        for line in self.path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            value = json.loads(line)
            if not isinstance(value, dict) or not envelope_is_valid(value):
                raise ValueError("lineage_ledger_record_invalid")
            records.append(value)
        return records

    def append(self, envelope: Mapping[str, Any]) -> dict[str, Any]:
        if not envelope_is_valid(envelope):
            raise ValueError("lineage_envelope_invalid")
        existing = self.read_all()
        digest = str(envelope["body_digest"])
        packet_digest = str(envelope["body"]["source_v028_packet_digest"])
        for value in existing:
            if value["body_digest"] == digest:
                return {"status": "REPLAYED", "ledger_count": len(existing)}
            if value["body"]["source_v028_packet_digest"] == packet_digest:
                raise ValueError("source_packet_already_bound")
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(
                json.dumps(dict(envelope), ensure_ascii=False, sort_keys=True) + "\n"
            )
            handle.flush()
            os.fsync(handle.fileno())
        return {"status": "APPENDED", "ledger_count": len(existing) + 1}


__all__ = ["CandidateLineageLedger"]
