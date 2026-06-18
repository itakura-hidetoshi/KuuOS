from __future__ import annotations

import json
import os
import tempfile
from contextlib import contextmanager
from copy import deepcopy
from pathlib import Path
from typing import Any, Iterator, Mapping

import fcntl

from runtime.kuuos_gauge_qi_process_graphrag_v0_1 import (
    canonical_json,
    digest_payload,
    evaluate_evidence_bundle,
)
from runtime.kuuos_gauge_qi_process_graphrag_types_v0_2 import (
    APPLY_RESULT_VERSION,
    PERSISTENT_RECEIPT_VERSION,
    STATE_VERSION,
    STORE_COMMIT_VERSION,
    apply_result_digest,
    copy_boundary,
    copy_non_authority,
    persistent_receipt_digest,
    require_nonempty_string,
    require_nonnegative_int,
    state_digest,
    store_commit_digest,
    validate_fixed_boundary,
    validate_route,
)


class GaugeQiGraphRAGStoreError(RuntimeError):
    pass


def build_initial_graph_rag_state(
    *, lineage_id: str, query_id: str, now_ms: int
) -> dict[str, Any]:
    lineage = require_nonempty_string(lineage_id, "lineage_id")
    query = require_nonempty_string(query_id, "query_id")
    now = require_nonnegative_int(now_ms, "now_ms")
    state = {
        "version": STATE_VERSION,
        "lineage_id": lineage,
        "query_id": query,
        "event_count": 0,
        "run_count": 0,
        "processed_bundle_digests": [],
        "latest_v01_receipt_digest": "",
        "latest_persistent_receipt_digest": "",
        "latest_route": "",
        "evidence_chain_digest": digest_payload(
            {"lineage_id": lineage, "query_id": query, "kind": "evidence_genesis"}
        ),
        "holonomy_chain_digest": digest_payload(
            {"lineage_id": lineage, "query_id": query, "kind": "holonomy_genesis"}
        ),
        "observation_debt_chain_digest": digest_payload(
            {"lineage_id": lineage, "query_id": query, "kind": "debt_genesis"}
        ),
        "receipt_history": [],
        "predecessor_graph_rag_state_digest": "",
        "updated_at_ms": now,
        "boundary": copy_boundary(),
        "non_authority": copy_non_authority(),
        "graph_rag_state_digest": "",
    }
    state["graph_rag_state_digest"] = state_digest(state)
    return state


def validate_graph_rag_state(state: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    try:
        if state.get("version") != STATE_VERSION:
            errors.append("graph_rag_state_version_invalid")
        require_nonempty_string(state.get("lineage_id"), "lineage_id")
        require_nonempty_string(state.get("query_id"), "query_id")
        event_count = require_nonnegative_int(state.get("event_count"), "event_count")
        run_count = require_nonnegative_int(state.get("run_count"), "run_count")
        require_nonnegative_int(state.get("updated_at_ms"), "updated_at_ms")

        processed = list(state.get("processed_bundle_digests", []))
        if len(processed) != len(set(processed)):
            errors.append("processed_bundle_digest_duplicate")
        if len(processed) != event_count:
            errors.append("processed_bundle_count_mismatch")

        history = list(state.get("receipt_history", []))
        if len(history) != event_count:
            errors.append("receipt_history_count_mismatch")
        if run_count != event_count:
            errors.append("run_count_mismatch")

        for field in (
            "evidence_chain_digest",
            "holonomy_chain_digest",
            "observation_debt_chain_digest",
        ):
            require_nonempty_string(state.get(field), field)

        if event_count == 0:
            for field in (
                "latest_v01_receipt_digest",
                "latest_persistent_receipt_digest",
                "latest_route",
            ):
                if state.get(field) != "":
                    errors.append(f"initial_{field}_must_be_empty")
        else:
            require_nonempty_string(
                state.get("latest_v01_receipt_digest"), "latest_v01_receipt_digest"
            )
            require_nonempty_string(
                state.get("latest_persistent_receipt_digest"),
                "latest_persistent_receipt_digest",
            )
            validate_route(state.get("latest_route"), "latest_route")
            if history[-1].get("persistent_receipt_digest") != state.get(
                "latest_persistent_receipt_digest"
            ):
                errors.append("latest_persistent_receipt_history_mismatch")
            if history[-1].get("route") != state.get("latest_route"):
                errors.append("latest_route_history_mismatch")

        errors.extend(validate_fixed_boundary(state))
        if state.get("graph_rag_state_digest") != state_digest(state):
            errors.append("graph_rag_state_digest_invalid")
    except (TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors


def _apply_result(
    *,
    status: str,
    state: Mapping[str, Any],
    source_bundle_digest: str,
    receipt: Mapping[str, Any] | None,
    errors: list[str],
    replayed_receipt_digest: str = "",
) -> dict[str, Any]:
    result = {
        "version": APPLY_RESULT_VERSION,
        "status": status,
        "source_bundle_digest": source_bundle_digest,
        "receipt": deepcopy(dict(receipt)) if receipt is not None else None,
        "state": deepcopy(dict(state)),
        "replayed_receipt_digest": replayed_receipt_digest,
        "errors": list(errors),
        "graph_rag_store_commit_digest": "",
        "graph_rag_apply_result_digest": "",
    }
    result["graph_rag_apply_result_digest"] = apply_result_digest(result)
    return result


def apply_evidence_bundle(
    state: Mapping[str, Any], bundle: Mapping[str, Any], *, now_ms: int
) -> dict[str, Any]:
    state_errors = validate_graph_rag_state(state)
    if state_errors:
        raise ValueError("invalid_graph_rag_state:" + ";".join(state_errors))

    now = require_nonnegative_int(now_ms, "now_ms")
    bundle_digest = digest_payload(bundle)
    processed = set(state.get("processed_bundle_digests", []))
    if bundle_digest in processed:
        prior = next(
            (
                item
                for item in state.get("receipt_history", [])
                if item.get("source_bundle_digest") == bundle_digest
            ),
            None,
        )
        return _apply_result(
            status="REPLAYED",
            state=state,
            source_bundle_digest=bundle_digest,
            receipt=None,
            errors=[],
            replayed_receipt_digest=(
                str(prior.get("persistent_receipt_digest", "")) if prior else ""
            ),
        )

    if bundle.get("query_id") != state.get("query_id"):
        return _apply_result(
            status="REJECTED",
            state=state,
            source_bundle_digest=bundle_digest,
            receipt=None,
            errors=["graph_rag_query_lineage_mismatch"],
        )
    if now < int(state.get("updated_at_ms", 0)):
        return _apply_result(
            status="REJECTED",
            state=state,
            source_bundle_digest=bundle_digest,
            receipt=None,
            errors=["graph_rag_time_regression"],
        )

    try:
        v01_receipt = evaluate_evidence_bundle(bundle)
    except (TypeError, ValueError) as exc:
        return _apply_result(
            status="REJECTED",
            state=state,
            source_bundle_digest=bundle_digest,
            receipt=None,
            errors=[str(exc)],
        )

    if v01_receipt.get("source_bundle_digest") != bundle_digest:
        raise ValueError("v01_source_bundle_digest_mismatch")

    persistent_receipt = {
        "version": PERSISTENT_RECEIPT_VERSION,
        "lineage_id": state["lineage_id"],
        "query_id": state["query_id"],
        "run_index": int(state["run_count"]) + 1,
        "source_bundle_digest": bundle_digest,
        "v01_receipt_digest": v01_receipt["receipt_digest"],
        "route": v01_receipt["route"],
        "admissible_paths": list(v01_receipt["admissible_paths"]),
        "plurality_preserved": bool(v01_receipt["plurality_preserved"]),
        "path_results_digest": digest_payload(v01_receipt["path_results"]),
        "cycle_results_digest": digest_payload(v01_receipt["cycle_results"]),
        "max_curvature_residual": v01_receipt["max_curvature_residual"],
        "max_path_action": v01_receipt["max_path_action"],
        "minimum_evidence_sufficiency": v01_receipt[
            "minimum_evidence_sufficiency"
        ],
        "next_observation_target": v01_receipt["next_observation_target"],
        "process_tensor_digest": v01_receipt["process_tensor_digest"],
        "history_window_digest": v01_receipt["history_window_digest"],
        "predecessor_graph_rag_state_digest": state["graph_rag_state_digest"],
        "created_at_ms": now,
        "boundary": copy_boundary(),
        "non_authority": copy_non_authority(),
        "persistent_receipt_digest": "",
    }
    persistent_receipt["persistent_receipt_digest"] = persistent_receipt_digest(
        persistent_receipt
    )

    next_state = deepcopy(dict(state))
    next_state["predecessor_graph_rag_state_digest"] = state[
        "graph_rag_state_digest"
    ]
    next_state["event_count"] = int(state["event_count"]) + 1
    next_state["run_count"] = int(state["run_count"]) + 1
    next_state["processed_bundle_digests"] = list(
        state["processed_bundle_digests"]
    ) + [bundle_digest]
    next_state["latest_v01_receipt_digest"] = v01_receipt["receipt_digest"]
    next_state["latest_persistent_receipt_digest"] = persistent_receipt[
        "persistent_receipt_digest"
    ]
    next_state["latest_route"] = v01_receipt["route"]
    next_state["evidence_chain_digest"] = digest_payload(
        {
            "previous_evidence_chain_digest": state["evidence_chain_digest"],
            "persistent_receipt_digest": persistent_receipt[
                "persistent_receipt_digest"
            ],
            "source_bundle_digest": bundle_digest,
            "route": v01_receipt["route"],
        }
    )
    next_state["holonomy_chain_digest"] = digest_payload(
        {
            "previous_holonomy_chain_digest": state["holonomy_chain_digest"],
            "cycle_results_digest": persistent_receipt["cycle_results_digest"],
            "admissible_paths": persistent_receipt["admissible_paths"],
            "max_curvature_residual": persistent_receipt[
                "max_curvature_residual"
            ],
        }
    )
    next_state["observation_debt_chain_digest"] = digest_payload(
        {
            "previous_observation_debt_chain_digest": state[
                "observation_debt_chain_digest"
            ],
            "next_observation_target": persistent_receipt[
                "next_observation_target"
            ],
            "max_path_action": persistent_receipt["max_path_action"],
            "minimum_evidence_sufficiency": persistent_receipt[
                "minimum_evidence_sufficiency"
            ],
        }
    )
    next_state["receipt_history"] = list(state["receipt_history"]) + [
        {
            "event_index": next_state["event_count"],
            "run_index": next_state["run_count"],
            "source_bundle_digest": bundle_digest,
            "v01_receipt_digest": v01_receipt["receipt_digest"],
            "persistent_receipt_digest": persistent_receipt[
                "persistent_receipt_digest"
            ],
            "route": v01_receipt["route"],
            "admissible_paths": list(v01_receipt["admissible_paths"]),
            "next_observation_target": v01_receipt["next_observation_target"],
            "evidence_chain_digest": next_state["evidence_chain_digest"],
            "holonomy_chain_digest": next_state["holonomy_chain_digest"],
            "observation_debt_chain_digest": next_state[
                "observation_debt_chain_digest"
            ],
            "created_at_ms": now,
        }
    ]
    next_state["updated_at_ms"] = now
    next_state["graph_rag_state_digest"] = ""
    next_state["graph_rag_state_digest"] = state_digest(next_state)
    next_errors = validate_graph_rag_state(next_state)
    if next_errors:
        raise ValueError("next_graph_rag_state_invalid:" + ";".join(next_errors))

    return _apply_result(
        status="APPLIED",
        state=next_state,
        source_bundle_digest=bundle_digest,
        receipt=persistent_receipt,
        errors=[],
    )


class GaugeQiGraphRAGStore:
    def __init__(self, root: str | Path) -> None:
        self.root = Path(root)
        self.genesis_path = self.root / "graph-rag-genesis.json"
        self.ledger_path = self.root / "graph-rag-ledger.jsonl"
        self.snapshot_path = self.root / "graph-rag-snapshot.json"
        self.lock_path = self.root / ".graph-rag.lock"

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
        path.parent.mkdir(parents=True, exist_ok=True)
        fd, temporary_name = tempfile.mkstemp(
            prefix=path.name + ".", dir=path.parent
        )
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                handle.write(canonical_json(value))
                handle.write("\n")
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temporary_name, path)
        finally:
            if os.path.exists(temporary_name):
                os.unlink(temporary_name)

    @staticmethod
    def _read_json(path: Path) -> dict[str, Any]:
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise GaugeQiGraphRAGStoreError(
                f"graph_rag_json_read_failed:{path.name}"
            ) from exc
        if not isinstance(value, dict):
            raise GaugeQiGraphRAGStoreError(
                f"graph_rag_json_object_required:{path.name}"
            )
        return value

    def initialize(self, initial_state: Mapping[str, Any]) -> dict[str, Any]:
        errors = validate_graph_rag_state(initial_state)
        if errors:
            raise GaugeQiGraphRAGStoreError(
                "initial_graph_rag_state_invalid:" + ";".join(errors)
            )
        with self._locked():
            if self.genesis_path.exists() or self.ledger_path.exists():
                raise GaugeQiGraphRAGStoreError("graph_rag_store_already_initialized")
            self._write_atomic(self.genesis_path, initial_state)
            self.ledger_path.touch(exist_ok=False)
            with self.ledger_path.open("a", encoding="utf-8") as handle:
                handle.flush()
                os.fsync(handle.fileno())
            self._write_atomic(self.snapshot_path, initial_state)
        return deepcopy(dict(initial_state))

    def _read_ledger(self) -> list[dict[str, Any]]:
        commits: list[dict[str, Any]] = []
        try:
            with self.ledger_path.open("r", encoding="utf-8") as handle:
                for line_number, raw in enumerate(handle, start=1):
                    line = raw.strip()
                    if not line:
                        raise GaugeQiGraphRAGStoreError(
                            f"graph_rag_ledger_blank_line:{line_number}"
                        )
                    try:
                        item = json.loads(line)
                    except json.JSONDecodeError as exc:
                        raise GaugeQiGraphRAGStoreError(
                            f"graph_rag_ledger_malformed_json:{line_number}"
                        ) from exc
                    if not isinstance(item, dict):
                        raise GaugeQiGraphRAGStoreError(
                            f"graph_rag_ledger_object_required:{line_number}"
                        )
                    commits.append(item)
        except OSError as exc:
            raise GaugeQiGraphRAGStoreError("graph_rag_ledger_read_failed") from exc
        return commits

    def _recover_unlocked(self) -> tuple[dict[str, Any], list[dict[str, Any]]]:
        if not self.genesis_path.exists() or not self.ledger_path.exists():
            raise GaugeQiGraphRAGStoreError("graph_rag_store_not_initialized")
        state = self._read_json(self.genesis_path)
        errors = validate_graph_rag_state(state)
        if errors:
            raise GaugeQiGraphRAGStoreError(
                "graph_rag_genesis_invalid:" + ";".join(errors)
            )

        commits = self._read_ledger()
        previous_commit_digest = ""
        for index, commit in enumerate(commits, start=1):
            if commit.get("version") != STORE_COMMIT_VERSION:
                raise GaugeQiGraphRAGStoreError(
                    f"graph_rag_ledger_version_invalid:{index}"
                )
            if commit.get("graph_rag_store_commit_digest") != store_commit_digest(
                commit
            ):
                raise GaugeQiGraphRAGStoreError(
                    f"graph_rag_ledger_commit_digest_invalid:{index}"
                )
            if commit.get("predecessor_commit_digest") != previous_commit_digest:
                raise GaugeQiGraphRAGStoreError(
                    f"graph_rag_ledger_chain_broken:{index}"
                )
            if commit.get("predecessor_graph_rag_state_digest") != state.get(
                "graph_rag_state_digest"
            ):
                raise GaugeQiGraphRAGStoreError(
                    f"graph_rag_state_chain_broken:{index}"
                )
            bundle = commit.get("bundle")
            if not isinstance(bundle, dict):
                raise GaugeQiGraphRAGStoreError(
                    f"graph_rag_ledger_bundle_invalid:{index}"
                )
            result = apply_evidence_bundle(
                state, bundle, now_ms=int(commit.get("created_at_ms", -1))
            )
            if result.get("status") != "APPLIED":
                raise GaugeQiGraphRAGStoreError(
                    f"graph_rag_ledger_replay_rejected:{index}"
                )
            receipt = result.get("receipt")
            if not isinstance(receipt, dict):
                raise GaugeQiGraphRAGStoreError(
                    f"graph_rag_ledger_receipt_missing:{index}"
                )
            if receipt.get("persistent_receipt_digest") != commit.get(
                "persistent_receipt_digest"
            ):
                raise GaugeQiGraphRAGStoreError(
                    f"graph_rag_ledger_receipt_digest_mismatch:{index}"
                )
            result_state = result["state"]
            if result_state.get("graph_rag_state_digest") != commit.get(
                "result_graph_rag_state_digest"
            ):
                raise GaugeQiGraphRAGStoreError(
                    f"graph_rag_ledger_result_state_mismatch:{index}"
                )
            state = result_state
            previous_commit_digest = commit["graph_rag_store_commit_digest"]
        return state, commits

    def recover(self, *, repair_snapshot: bool = False) -> dict[str, Any]:
        with self._locked():
            state, _ = self._recover_unlocked()
            snapshot_matches = False
            if self.snapshot_path.exists():
                try:
                    snapshot_matches = self._read_json(self.snapshot_path) == state
                except GaugeQiGraphRAGStoreError:
                    snapshot_matches = False
            if not snapshot_matches:
                if not repair_snapshot:
                    raise GaugeQiGraphRAGStoreError(
                        "graph_rag_snapshot_ledger_mismatch"
                    )
                self._write_atomic(self.snapshot_path, state)
            return deepcopy(state)

    def apply(
        self, bundle: Mapping[str, Any], *, now_ms: int
    ) -> dict[str, Any]:
        with self._locked():
            state, commits = self._recover_unlocked()
            result = apply_evidence_bundle(state, bundle, now_ms=now_ms)
            if result["status"] != "APPLIED":
                return result

            receipt = result["receipt"]
            next_state = result["state"]
            commit = {
                "version": STORE_COMMIT_VERSION,
                "predecessor_commit_digest": (
                    commits[-1]["graph_rag_store_commit_digest"] if commits else ""
                ),
                "predecessor_graph_rag_state_digest": state[
                    "graph_rag_state_digest"
                ],
                "source_bundle_digest": result["source_bundle_digest"],
                "bundle": deepcopy(dict(bundle)),
                "created_at_ms": require_nonnegative_int(now_ms, "now_ms"),
                "persistent_receipt_digest": receipt[
                    "persistent_receipt_digest"
                ],
                "result_graph_rag_state_digest": next_state[
                    "graph_rag_state_digest"
                ],
                "graph_rag_store_commit_digest": "",
            }
            commit["graph_rag_store_commit_digest"] = store_commit_digest(commit)
            try:
                with self.ledger_path.open("a", encoding="utf-8") as handle:
                    handle.write(canonical_json(commit))
                    handle.write("\n")
                    handle.flush()
                    os.fsync(handle.fileno())
            except OSError as exc:
                raise GaugeQiGraphRAGStoreError(
                    "graph_rag_ledger_append_failed"
                ) from exc
            self._write_atomic(self.snapshot_path, next_state)

            result["graph_rag_store_commit_digest"] = commit[
                "graph_rag_store_commit_digest"
            ]
            result["graph_rag_apply_result_digest"] = ""
            result["graph_rag_apply_result_digest"] = apply_result_digest(result)
            return result
