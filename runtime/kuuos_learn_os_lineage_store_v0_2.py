from __future__ import annotations

import json
import os
import tempfile
from contextlib import contextmanager
from copy import deepcopy
from pathlib import Path
from typing import Any, Iterator, Mapping

import fcntl

from runtime.kuuos_belief_os_types_v0_1 import canonical_json
from runtime.kuuos_learn_os_lineage_kernel_v0_2 import (
    validate_completion_receipt,
    validate_handoff_receipt,
)
from runtime.kuuos_learn_os_lineage_types_v0_2 import (
    STAGE_COMPLETION,
    STAGE_HANDOFF,
    STAGES,
    STORE_COMMIT_VERSION,
    STORE_STATE_VERSION,
    handoff_single_use_key,
    require_int,
    require_string,
    store_commit_digest,
    store_state_digest,
)


class LearnLineageStoreError(RuntimeError):
    pass


def build_initial_learn_lineage_store_state(
    *, store_id: str, now_ms: int
) -> dict[str, Any]:
    state = {
        "version": STORE_STATE_VERSION,
        "store_id": require_string(store_id, "store_id"),
        "commit_count": 0,
        "updated_at_ms": require_int(now_ms, "now_ms"),
        "issued_handoffs": [],
        "completed_handoffs": [],
        "processed_receipt_digests": [],
        "learn_lineage_store_state_digest": "",
    }
    state["learn_lineage_store_state_digest"] = store_state_digest(state)
    return state


def validate_learn_lineage_store_state(state: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    try:
        if state.get("version") != STORE_STATE_VERSION:
            errors.append("learn_lineage_store_state_version_invalid")
        require_string(state.get("store_id"), "store_id")
        require_int(state.get("commit_count"), "commit_count")
        require_int(state.get("updated_at_ms"), "updated_at_ms")
        if state.get("learn_lineage_store_state_digest") != store_state_digest(state):
            errors.append("learn_lineage_store_state_digest_invalid")
        issued = list(state.get("issued_handoffs", []))
        completed = list(state.get("completed_handoffs", []))
        processed = list(state.get("processed_receipt_digests", []))
        issued_keys = [str(item.get("single_use_key", "")) for item in issued]
        issued_digests = [
            str(item.get("handoff_receipt_digest", "")) for item in issued
        ]
        completed_digests = [
            str(item.get("handoff_receipt_digest", "")) for item in completed
        ]
        if len(issued_keys) != len(set(issued_keys)):
            errors.append("learn_lineage_store_single_use_key_duplicate")
        if len(issued_digests) != len(set(issued_digests)):
            errors.append("learn_lineage_store_handoff_duplicate")
        if len(completed_digests) != len(set(completed_digests)):
            errors.append("learn_lineage_store_completion_duplicate")
        if not set(completed_digests).issubset(set(issued_digests)):
            errors.append("learn_lineage_store_completion_without_handoff")
        if len(processed) != len(set(processed)):
            errors.append("learn_lineage_store_processed_duplicate")
        if int(state.get("commit_count", -1)) != len(processed):
            errors.append("learn_lineage_store_commit_count_mismatch")
    except (TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors


class LearnLineageStore:
    def __init__(self, root: str | Path) -> None:
        self.root = Path(root)
        self.genesis_path = self.root / "learn-lineage-genesis.json"
        self.ledger_path = self.root / "learn-lineage-ledger.jsonl"
        self.snapshot_path = self.root / "learn-lineage-snapshot.json"
        self.lock_path = self.root / ".learn-os-v02-lineage.lock"

    @contextmanager
    def _locked(self) -> Iterator[None]:
        self.root.mkdir(parents=True, exist_ok=True)
        with self.lock_path.open("a+", encoding="utf-8") as handle:
            fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
            try:
                yield
            finally:
                fcntl.flock(handle.fileno(), fcntl.LOCK_UN)

    @staticmethod
    def _write_atomic(path: Path, value: Mapping[str, Any]) -> None:
        fd, temporary = tempfile.mkstemp(prefix=path.name + ".", dir=path.parent)
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                handle.write(canonical_json(value) + "\n")
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temporary, path)
        finally:
            if os.path.exists(temporary):
                os.unlink(temporary)

    @staticmethod
    def _read_json(path: Path) -> dict[str, Any]:
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise LearnLineageStoreError(
                f"learn_lineage_json_read_failed:{path.name}"
            ) from exc
        if not isinstance(value, dict):
            raise LearnLineageStoreError(
                f"learn_lineage_json_object_required:{path.name}"
            )
        return value

    def initialize(self, initial_state: Mapping[str, Any]) -> dict[str, Any]:
        errors = validate_learn_lineage_store_state(initial_state)
        if errors:
            raise LearnLineageStoreError(
                "initial_learn_lineage_store_state_invalid:" + ";".join(errors)
            )
        with self._locked():
            if self.genesis_path.exists() or self.ledger_path.exists():
                raise LearnLineageStoreError("learn_lineage_store_already_initialized")
            self._write_atomic(self.genesis_path, dict(initial_state))
            self.ledger_path.touch(exist_ok=False)
            with self.ledger_path.open("a", encoding="utf-8") as handle:
                handle.flush()
                os.fsync(handle.fileno())
            self._write_atomic(self.snapshot_path, dict(initial_state))
        return deepcopy(dict(initial_state))

    def _read_ledger(self) -> list[dict[str, Any]]:
        commits: list[dict[str, Any]] = []
        try:
            with self.ledger_path.open("r", encoding="utf-8") as handle:
                for line_number, raw in enumerate(handle, start=1):
                    line = raw.strip()
                    if not line:
                        raise LearnLineageStoreError(
                            f"learn_lineage_ledger_blank_line:{line_number}"
                        )
                    item = json.loads(line)
                    if not isinstance(item, dict):
                        raise LearnLineageStoreError(
                            f"learn_lineage_ledger_object_required:{line_number}"
                        )
                    commits.append(item)
        except (OSError, json.JSONDecodeError) as exc:
            raise LearnLineageStoreError("learn_lineage_ledger_read_failed") from exc
        return commits

    @staticmethod
    def _apply_receipt(
        state: Mapping[str, Any],
        stage: str,
        receipt: Mapping[str, Any],
        now_ms: int,
    ) -> tuple[str, dict[str, Any]]:
        if stage not in STAGES:
            raise LearnLineageStoreError("learn_lineage_stage_invalid")
        next_state = deepcopy(dict(state))
        if stage == STAGE_HANDOFF:
            errors = validate_handoff_receipt(receipt)
            if errors:
                raise LearnLineageStoreError(
                    "learn_lineage_handoff_invalid:" + ";".join(errors)
                )
            digest = str(receipt["learn_lineage_handoff_receipt_digest"])
            if digest in set(next_state["processed_receipt_digests"]):
                return "REPLAYED", next_state
            key = handoff_single_use_key(receipt)
            if key in {
                str(item["single_use_key"])
                for item in next_state["issued_handoffs"]
            }:
                raise LearnLineageStoreError("learn_lineage_handoff_already_issued")
            next_state["issued_handoffs"] = list(next_state["issued_handoffs"]) + [
                {
                    "single_use_key": key,
                    "handoff_receipt_digest": digest,
                    "verify_completion_receipt_digest": receipt[
                        "verify_lineage_completion_receipt_digest"
                    ],
                    "verify_state_digest": receipt["committed_verify_state_digest"],
                }
            ]
        else:
            errors = validate_completion_receipt(receipt)
            if errors:
                raise LearnLineageStoreError(
                    "learn_lineage_completion_invalid:" + ";".join(errors)
                )
            digest = str(receipt["learn_lineage_completion_receipt_digest"])
            if digest in set(next_state["processed_receipt_digests"]):
                return "REPLAYED", next_state
            handoff_digest = str(receipt["learn_lineage_handoff_receipt_digest"])
            issued = {
                str(item["handoff_receipt_digest"])
                for item in next_state["issued_handoffs"]
            }
            if handoff_digest not in issued:
                raise LearnLineageStoreError(
                    "learn_lineage_completion_handoff_not_issued"
                )
            completed = {
                str(item["handoff_receipt_digest"])
                for item in next_state["completed_handoffs"]
            }
            if handoff_digest in completed:
                raise LearnLineageStoreError(
                    "learn_lineage_completion_already_committed"
                )
            next_state["completed_handoffs"] = list(
                next_state["completed_handoffs"]
            ) + [
                {
                    "handoff_receipt_digest": handoff_digest,
                    "completion_receipt_digest": digest,
                    "learn_state_digest": receipt["committed_learn_state_digest"],
                    "learning_route": receipt["learning_route"],
                    "planos_replan_input_digest": receipt[
                        "planos_replan_input_digest"
                    ],
                }
            ]
        next_state["processed_receipt_digests"] = list(
            next_state["processed_receipt_digests"]
        ) + [digest]
        next_state["commit_count"] = int(next_state["commit_count"]) + 1
        next_state["updated_at_ms"] = require_int(now_ms, "now_ms")
        next_state["learn_lineage_store_state_digest"] = ""
        next_state["learn_lineage_store_state_digest"] = store_state_digest(next_state)
        errors = validate_learn_lineage_store_state(next_state)
        if errors:
            raise LearnLineageStoreError(
                "next_learn_lineage_store_state_invalid:" + ";".join(errors)
            )
        return "COMMITTED", next_state

    def _recover_unlocked(
        self,
    ) -> tuple[dict[str, Any], list[dict[str, Any]]]:
        if not self.genesis_path.exists() or not self.ledger_path.exists():
            raise LearnLineageStoreError("learn_lineage_store_not_initialized")
        state = self._read_json(self.genesis_path)
        errors = validate_learn_lineage_store_state(state)
        if errors:
            raise LearnLineageStoreError(
                "learn_lineage_genesis_invalid:" + ";".join(errors)
            )
        commits = self._read_ledger()
        previous_commit_digest = ""
        for index, commit in enumerate(commits, start=1):
            if commit.get("version") != STORE_COMMIT_VERSION:
                raise LearnLineageStoreError(
                    f"learn_lineage_commit_version_invalid:{index}"
                )
            if commit.get("learn_lineage_store_commit_digest") != store_commit_digest(
                commit
            ):
                raise LearnLineageStoreError(
                    f"learn_lineage_commit_digest_invalid:{index}"
                )
            if commit.get("predecessor_commit_digest") != previous_commit_digest:
                raise LearnLineageStoreError(
                    f"learn_lineage_commit_chain_broken:{index}"
                )
            if commit.get("predecessor_state_digest") != state.get(
                "learn_lineage_store_state_digest"
            ):
                raise LearnLineageStoreError(
                    f"learn_lineage_state_chain_broken:{index}"
                )
            status, state = self._apply_receipt(
                state,
                str(commit.get("stage")),
                dict(commit.get("receipt", {})),
                int(commit.get("committed_at_ms", 0)),
            )
            if status != "COMMITTED":
                raise LearnLineageStoreError(
                    f"learn_lineage_recovery_replay_unexpected:{index}"
                )
            if commit.get("result_state_digest") != state.get(
                "learn_lineage_store_state_digest"
            ):
                raise LearnLineageStoreError(
                    f"learn_lineage_result_digest_mismatch:{index}"
                )
            previous_commit_digest = commit["learn_lineage_store_commit_digest"]
        return state, commits

    def recover(self, *, require_snapshot_match: bool = True) -> dict[str, Any]:
        with self._locked():
            state, _ = self._recover_unlocked()
            if require_snapshot_match:
                snapshot = self._read_json(self.snapshot_path)
                if snapshot.get("learn_lineage_store_state_digest") != state.get(
                    "learn_lineage_store_state_digest"
                ):
                    raise LearnLineageStoreError(
                        "learn_lineage_snapshot_ledger_mismatch"
                    )
            return deepcopy(state)

    def commit(
        self, *, stage: str, receipt: Mapping[str, Any], now_ms: int
    ) -> dict[str, Any]:
        with self._locked():
            state, commits = self._recover_unlocked()
            status, next_state = self._apply_receipt(state, stage, receipt, now_ms)
            if status == "REPLAYED":
                return {"status": status, "state": deepcopy(next_state)}
            commit = {
                "version": STORE_COMMIT_VERSION,
                "commit_index": len(commits) + 1,
                "stage": stage,
                "predecessor_commit_digest": commits[-1][
                    "learn_lineage_store_commit_digest"
                ]
                if commits
                else "",
                "predecessor_state_digest": state[
                    "learn_lineage_store_state_digest"
                ],
                "receipt": deepcopy(dict(receipt)),
                "committed_at_ms": require_int(now_ms, "now_ms"),
                "result_state_digest": next_state[
                    "learn_lineage_store_state_digest"
                ],
                "learn_lineage_store_commit_digest": "",
            }
            commit["learn_lineage_store_commit_digest"] = store_commit_digest(commit)
            with self.ledger_path.open("a", encoding="utf-8") as handle:
                handle.write(canonical_json(commit) + "\n")
                handle.flush()
                os.fsync(handle.fileno())
            self._write_atomic(self.snapshot_path, next_state)
            return {
                "status": "COMMITTED",
                "state": deepcopy(next_state),
                "commit": deepcopy(commit),
            }

    def repair_snapshot(self) -> dict[str, Any]:
        with self._locked():
            state, _ = self._recover_unlocked()
            self._write_atomic(self.snapshot_path, state)
            return deepcopy(state)

    def ledger_commit_count(self) -> int:
        with self._locked():
            _, commits = self._recover_unlocked()
            return len(commits)
