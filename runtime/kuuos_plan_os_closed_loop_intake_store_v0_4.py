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
from runtime.kuuos_plan_os_closed_loop_intake_kernel_v0_4 import (
    validate_bind_receipt,
    validate_intake_receipt,
)
from runtime.kuuos_plan_os_closed_loop_intake_types_v0_4 import (
    STAGE_BIND,
    STAGE_INTAKE,
    STAGES,
    STORE_COMMIT_VERSION,
    STORE_STATE_VERSION,
    intake_single_use_key,
    require_int,
    require_string,
    store_commit_digest,
    store_state_digest,
)


class ClosedLoopIntakeStoreError(RuntimeError):
    pass


def build_initial_closed_loop_intake_store_state(
    *, store_id: str, now_ms: int
) -> dict[str, Any]:
    state = {
        "version": STORE_STATE_VERSION,
        "store_id": require_string(store_id, "store_id"),
        "commit_count": 0,
        "updated_at_ms": require_int(now_ms, "now_ms"),
        "intakes": [],
        "bindings": [],
        "processed_receipt_digests": [],
        "closed_loop_intake_store_state_digest": "",
    }
    state["closed_loop_intake_store_state_digest"] = store_state_digest(state)
    return state


def validate_closed_loop_intake_store_state(
    state: Mapping[str, Any]
) -> list[str]:
    errors: list[str] = []
    try:
        if state.get("version") != STORE_STATE_VERSION:
            errors.append("closed_loop_store_state_version_invalid")
        require_string(state.get("store_id"), "store_id")
        require_int(state.get("commit_count"), "commit_count")
        require_int(state.get("updated_at_ms"), "updated_at_ms")
        if state.get("closed_loop_intake_store_state_digest") != store_state_digest(
            state
        ):
            errors.append("closed_loop_store_state_digest_invalid")
        intakes = list(state.get("intakes", []))
        bindings = list(state.get("bindings", []))
        processed = list(state.get("processed_receipt_digests", []))
        intake_keys = [str(item.get("single_use_key", "")) for item in intakes]
        intake_digests = [str(item.get("intake_receipt_digest", "")) for item in intakes]
        bound_intakes = [str(item.get("intake_receipt_digest", "")) for item in bindings]
        if len(intake_keys) != len(set(intake_keys)):
            errors.append("closed_loop_store_intake_key_duplicate")
        if len(intake_digests) != len(set(intake_digests)):
            errors.append("closed_loop_store_intake_duplicate")
        if len(bound_intakes) != len(set(bound_intakes)):
            errors.append("closed_loop_store_bind_duplicate")
        if not set(bound_intakes).issubset(set(intake_digests)):
            errors.append("closed_loop_store_bind_without_intake")
        if len(processed) != len(set(processed)):
            errors.append("closed_loop_store_processed_duplicate")
        if int(state.get("commit_count", -1)) != len(processed):
            errors.append("closed_loop_store_commit_count_mismatch")
    except (TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors


class ClosedLoopIntakeStore:
    def __init__(self, root: str | Path) -> None:
        self.root = Path(root)
        self.genesis_path = self.root / "closed-loop-intake-genesis.json"
        self.ledger_path = self.root / "closed-loop-intake-ledger.jsonl"
        self.snapshot_path = self.root / "closed-loop-intake-snapshot.json"
        self.lock_path = self.root / ".plan-os-v04-intake.lock"

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
            raise ClosedLoopIntakeStoreError(
                f"closed_loop_json_read_failed:{path.name}"
            ) from exc
        if not isinstance(value, dict):
            raise ClosedLoopIntakeStoreError(
                f"closed_loop_json_object_required:{path.name}"
            )
        return value

    def initialize(self, initial_state: Mapping[str, Any]) -> dict[str, Any]:
        errors = validate_closed_loop_intake_store_state(initial_state)
        if errors:
            raise ClosedLoopIntakeStoreError(
                "closed_loop_initial_state_invalid:" + ";".join(errors)
            )
        with self._locked():
            if self.genesis_path.exists() or self.ledger_path.exists():
                raise ClosedLoopIntakeStoreError("closed_loop_store_already_initialized")
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
                        raise ClosedLoopIntakeStoreError(
                            f"closed_loop_ledger_blank_line:{line_number}"
                        )
                    item = json.loads(line)
                    if not isinstance(item, dict):
                        raise ClosedLoopIntakeStoreError(
                            f"closed_loop_ledger_object_required:{line_number}"
                        )
                    commits.append(item)
        except (OSError, json.JSONDecodeError) as exc:
            raise ClosedLoopIntakeStoreError("closed_loop_ledger_read_failed") from exc
        return commits

    @staticmethod
    def _apply_receipt(
        state: Mapping[str, Any],
        stage: str,
        receipt: Mapping[str, Any],
        now_ms: int,
    ) -> tuple[str, dict[str, Any]]:
        if stage not in STAGES:
            raise ClosedLoopIntakeStoreError("closed_loop_stage_invalid")
        next_state = deepcopy(dict(state))
        if stage == STAGE_INTAKE:
            errors = validate_intake_receipt(receipt)
            if errors:
                raise ClosedLoopIntakeStoreError(
                    "closed_loop_intake_invalid:" + ";".join(errors)
                )
            digest = str(receipt["closed_loop_intake_receipt_digest"])
            if digest in set(next_state["processed_receipt_digests"]):
                return "REPLAYED", next_state
            key = intake_single_use_key(receipt)
            if key in {
                str(item["single_use_key"])
                for item in next_state["intakes"]
            }:
                raise ClosedLoopIntakeStoreError(
                    "closed_loop_intake_already_committed"
                )
            next_state["intakes"] = list(next_state["intakes"]) + [
                {
                    "single_use_key": key,
                    "intake_receipt_digest": digest,
                    "learn_completion_receipt_digest": receipt[
                        "learn_lineage_completion_receipt_digest"
                    ],
                    "current_plan_state_digest": receipt[
                        "current_plan_state_digest"
                    ],
                    "current_cycle_index": receipt["current_cycle_index"],
                }
            ]
        else:
            errors = validate_bind_receipt(receipt)
            if errors:
                raise ClosedLoopIntakeStoreError(
                    "closed_loop_bind_invalid:" + ";".join(errors)
                )
            digest = str(receipt["closed_loop_bind_receipt_digest"])
            if digest in set(next_state["processed_receipt_digests"]):
                return "REPLAYED", next_state
            intake_digest = str(receipt["closed_loop_intake_receipt_digest"])
            issued = {
                str(item["intake_receipt_digest"])
                for item in next_state["intakes"]
            }
            if intake_digest not in issued:
                raise ClosedLoopIntakeStoreError(
                    "closed_loop_bind_intake_not_committed"
                )
            already_bound = {
                str(item["intake_receipt_digest"])
                for item in next_state["bindings"]
            }
            if intake_digest in already_bound:
                raise ClosedLoopIntakeStoreError(
                    "closed_loop_intake_already_bound"
                )
            next_state["bindings"] = list(next_state["bindings"]) + [
                {
                    "intake_receipt_digest": intake_digest,
                    "bind_receipt_digest": digest,
                    "replan_id": receipt["replan_id"],
                    "replan_state_digest": receipt["replan_state_digest"],
                    "current_cycle_index": receipt["current_cycle_index"],
                    "active_from_cycle": receipt["active_from_cycle"],
                }
            ]
        next_state["processed_receipt_digests"] = list(
            next_state["processed_receipt_digests"]
        ) + [digest]
        next_state["commit_count"] = int(next_state["commit_count"]) + 1
        next_state["updated_at_ms"] = require_int(now_ms, "now_ms")
        next_state["closed_loop_intake_store_state_digest"] = ""
        next_state["closed_loop_intake_store_state_digest"] = store_state_digest(
            next_state
        )
        errors = validate_closed_loop_intake_store_state(next_state)
        if errors:
            raise ClosedLoopIntakeStoreError(
                "closed_loop_next_state_invalid:" + ";".join(errors)
            )
        return "COMMITTED", next_state

    def _recover_unlocked(
        self,
    ) -> tuple[dict[str, Any], list[dict[str, Any]]]:
        if not self.genesis_path.exists() or not self.ledger_path.exists():
            raise ClosedLoopIntakeStoreError("closed_loop_store_not_initialized")
        state = self._read_json(self.genesis_path)
        errors = validate_closed_loop_intake_store_state(state)
        if errors:
            raise ClosedLoopIntakeStoreError(
                "closed_loop_genesis_invalid:" + ";".join(errors)
            )
        commits = self._read_ledger()
        previous_commit_digest = ""
        for index, commit in enumerate(commits, start=1):
            if commit.get("version") != STORE_COMMIT_VERSION:
                raise ClosedLoopIntakeStoreError(
                    f"closed_loop_commit_version_invalid:{index}"
                )
            if commit.get("closed_loop_intake_store_commit_digest") != store_commit_digest(
                commit
            ):
                raise ClosedLoopIntakeStoreError(
                    f"closed_loop_commit_digest_invalid:{index}"
                )
            if commit.get("predecessor_commit_digest") != previous_commit_digest:
                raise ClosedLoopIntakeStoreError(
                    f"closed_loop_commit_chain_broken:{index}"
                )
            if commit.get("predecessor_state_digest") != state.get(
                "closed_loop_intake_store_state_digest"
            ):
                raise ClosedLoopIntakeStoreError(
                    f"closed_loop_state_chain_broken:{index}"
                )
            status, state = self._apply_receipt(
                state,
                str(commit.get("stage")),
                dict(commit.get("receipt", {})),
                int(commit.get("committed_at_ms", 0)),
            )
            if status != "COMMITTED":
                raise ClosedLoopIntakeStoreError(
                    f"closed_loop_recovery_replay_unexpected:{index}"
                )
            if commit.get("result_state_digest") != state.get(
                "closed_loop_intake_store_state_digest"
            ):
                raise ClosedLoopIntakeStoreError(
                    f"closed_loop_result_digest_mismatch:{index}"
                )
            previous_commit_digest = commit[
                "closed_loop_intake_store_commit_digest"
            ]
        return state, commits

    def recover(self, *, require_snapshot_match: bool = True) -> dict[str, Any]:
        with self._locked():
            state, _ = self._recover_unlocked()
            if require_snapshot_match:
                snapshot = self._read_json(self.snapshot_path)
                if snapshot.get(
                    "closed_loop_intake_store_state_digest"
                ) != state.get("closed_loop_intake_store_state_digest"):
                    raise ClosedLoopIntakeStoreError(
                        "closed_loop_snapshot_ledger_mismatch"
                    )
            return deepcopy(state)

    def commit(
        self, *, stage: str, receipt: Mapping[str, Any], now_ms: int
    ) -> dict[str, Any]:
        with self._locked():
            state, commits = self._recover_unlocked()
            status, next_state = self._apply_receipt(
                state, stage, receipt, now_ms
            )
            if status == "REPLAYED":
                return {"status": status, "state": deepcopy(next_state)}
            commit = {
                "version": STORE_COMMIT_VERSION,
                "commit_index": len(commits) + 1,
                "stage": stage,
                "predecessor_commit_digest": commits[-1][
                    "closed_loop_intake_store_commit_digest"
                ]
                if commits
                else "",
                "predecessor_state_digest": state[
                    "closed_loop_intake_store_state_digest"
                ],
                "receipt": deepcopy(dict(receipt)),
                "committed_at_ms": require_int(now_ms, "now_ms"),
                "result_state_digest": next_state[
                    "closed_loop_intake_store_state_digest"
                ],
                "closed_loop_intake_store_commit_digest": "",
            }
            commit["closed_loop_intake_store_commit_digest"] = store_commit_digest(
                commit
            )
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
