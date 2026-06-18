from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Mapping

from runtime.kuuos_observe_os_lineage_kernel_v0_2 import (
    validate_completion_receipt,
    validate_handoff_receipt,
)
from runtime.kuuos_observe_os_lineage_types_v0_2 import (
    STAGE_COMPLETION,
    STAGE_HANDOFF,
    handoff_single_use_key,
)


class ObserveLineageStoreError(RuntimeError):
    pass


class ObserveLineageStore:
    def __init__(self, root: str | Path) -> None:
        self.root = Path(root)
        self._issued: dict[str, dict[str, Any]] = {}
        self._completed: dict[str, dict[str, Any]] = {}
        self._processed: set[str] = set()

    def initialize(self, *, store_id: str, now_ms: int) -> dict[str, Any]:
        self.root.mkdir(parents=True, exist_ok=True)
        return {
            "store_id": store_id,
            "updated_at_ms": now_ms,
            "commit_count": 0,
        }

    def commit(
        self, *, stage: str, receipt: Mapping[str, Any], now_ms: int
    ) -> dict[str, Any]:
        if stage == STAGE_HANDOFF:
            errors = validate_handoff_receipt(receipt)
            digest = str(receipt.get("observe_lineage_handoff_receipt_digest", ""))
            if errors:
                raise ObserveLineageStoreError("invalid_handoff:" + ";".join(errors))
            if digest in self._processed:
                return {"status": "REPLAYED"}
            key = handoff_single_use_key(receipt)
            if key in self._issued:
                raise ObserveLineageStoreError("observe_lineage_handoff_already_issued")
            self._issued[key] = deepcopy(dict(receipt))
        elif stage == STAGE_COMPLETION:
            errors = validate_completion_receipt(receipt)
            digest = str(receipt.get("observe_lineage_completion_receipt_digest", ""))
            if errors:
                raise ObserveLineageStoreError("invalid_completion:" + ";".join(errors))
            if digest in self._processed:
                return {"status": "REPLAYED"}
            handoff_digest = str(receipt.get("observe_lineage_handoff_receipt_digest", ""))
            issued = {
                item["observe_lineage_handoff_receipt_digest"]
                for item in self._issued.values()
            }
            if handoff_digest not in issued:
                raise ObserveLineageStoreError("observe_lineage_handoff_not_issued")
            if handoff_digest in self._completed:
                raise ObserveLineageStoreError("observe_lineage_completion_already_committed")
            self._completed[handoff_digest] = deepcopy(dict(receipt))
        else:
            raise ObserveLineageStoreError("observe_lineage_stage_invalid")
        self._processed.add(digest)
        return {
            "status": "COMMITTED",
            "commit_count": len(self._processed),
            "updated_at_ms": now_ms,
        }

    def ledger_commit_count(self) -> int:
        return len(self._processed)
