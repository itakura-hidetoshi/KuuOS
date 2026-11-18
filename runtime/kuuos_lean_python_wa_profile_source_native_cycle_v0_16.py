"""Witnessed Plural->Wa profile/source checks in the isolated native v0.16 child.

The child obtains a committed Plural witness from its actual local Plural
store's ledger recovery on first Wa transition, then reuses that fixed
point-in-time witness. It wraps only v0.15's imported checked evaluator.
The old native kernel, receipt, store and eight routes remain unchanged.

Local ledger recovery is not external signature verification. Read-only
postflight reconstruction and stdout counters do not attest history.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

from contextlib import contextmanager
from dataclasses import dataclass
import json
import os
from pathlib import Path
import subprocess
import sys
from typing import Any, Iterator

from runtime import kuuos_lean_python_guarded_native_cycle_v0_10 as core
from runtime import kuuos_lean_python_wa_evaluation_guard_v0_15 as evaluation
from runtime import kuuos_lean_python_wa_evaluation_native_cycle_v0_15 as prior
from runtime.kuuos_decision_os_plural_store_v0_2 import PluralDecisionStore
from runtime.kuuos_lean_python_isolated_native_receipt_evidence_v0_9 import (
    IsolatedEvidenceAudit, ROOT,
)
from runtime.kuuos_lean_python_os_path_composition_v0_6 import _finite_json, _fingerprint
from runtime.kuuos_lean_python_wa_profile_source_guard_v0_16 import (
    WaProfileSourceBoundaryError, checked_apply_wa_profile_source_event,
)

VERSION = "kuuos_lean_python_wa_profile_source_native_cycle_v0_16"
SOURCE_MAIN = "9bbd82a95a579a8091a1cb5d7e7f7b92eb254924"
SUCCESS = "WA_COMMITTED_LOCAL_PLURAL_WITNESS_AND_PROFILE_CHECKED"
REPORT_KEYS = frozenset((
    "version", "source_main", "status", "evaluation_report",
    "wa_profile_source_guard_calls", "source_witness_digest",
    "plural_recovered_locally", "profile_digest_checked",
    "external_issuer_authenticated", "lean_python_refinement_proved",
))


@dataclass(frozen=True)
class WaProfileSourceNativeRun:
    status: str
    state_guard_calls: tuple[tuple[str, int], ...]
    pre_host_guard_calls: int
    wa_numeric_guard_calls: int
    wa_gate_guard_calls: int
    wa_evaluation_guard_calls: int
    wa_profile_source_guard_calls: int
    native_audit: IsolatedEvidenceAudit
    source_witness_digest: str
    source_main: str = SOURCE_MAIN
    scope: str = "local_Plural_store_recovery_Wa_projection_and_normalized_profile_digest"
    source_recovered_locally: bool = True
    source_external_authenticity_established: bool = False
    profile_digest_binding_checked: bool = True
    external_issuer_authenticated: bool = False
    historical_guard_execution_proved: bool = False
    lean_python_refinement_proved: bool = False
    original_native_sources_modified: bool = False
    all_store_writes_guarded: bool = False
    all_effects_prevented_on_any_failure: bool = False
    host_rollback_guaranteed: bool = False
    state_commit_atomic_with_host: bool = False
    execution_authority_granted: bool = False
    truth_authority_granted: bool = False
    git_merge_authority_granted: bool = False
    guard_observation_mode: str = "local_child_stdout_unattested"
    counts_include_recovery_replays: bool = True


def audit_local_evidence(root: Any) -> IsolatedEvidenceAudit:
    """Use v0.9's original read-only evidence; do not attest v0.16 history."""
    return prior.audit_local_evidence(root)


@contextmanager
def _guard_profile_source_boundary(
    root: Path, counters: dict[str, int], witness_identity: list[str],
) -> Iterator[None]:
    if (type(counters) is not dict or set(counters) != {"DecisionOSWa"}
            or type(counters["DecisionOSWa"]) is not int or counters["DecisionOSWa"] != 0
            or type(witness_identity) is not list or witness_identity != [""]):
        raise ValueError("fresh_wa_profile_source_counter_and_witness_required")
    if prior.checked_apply_wa_evaluation_event is not evaluation.checked_apply_wa_evaluation_event:
        raise ValueError("original_evaluation_boundary_binding_required")
    cached: list[dict[str, Any]] = []

    def guarded(state: Any, event: Any) -> dict[str, Any]:
        if not cached:
            # This is actual local append-only Plural store replay/recovery,
            # not a caller-provided standalone digest or a cryptographic issuer.
            try:
                recovered = PluralDecisionStore(root / "plural").recover(
                    require_snapshot_match=True
                )
                captured = _finite_json(recovered)
            except Exception as exc:
                raise WaProfileSourceBoundaryError(
                    "NO_DATA", ("local_plural_recovery_failed:" + type(exc).__name__,)
                ) from exc
            cached.append(captured)
            witness_identity[0] = _fingerprint(captured)
        outcome = checked_apply_wa_profile_source_event(state, event, cached[0])
        counters["DecisionOSWa"] += 1
        return outcome

    with core._replace_binding(prior, "checked_apply_wa_evaluation_event", guarded):
        yield


def _make_child_report(
    evaluation_report: dict[str, Any], count: int, witness_digest: str,
) -> dict[str, Any]:
    return {
        "version": VERSION, "source_main": SOURCE_MAIN, "status": SUCCESS,
        "evaluation_report": _finite_json(evaluation_report),
        "wa_profile_source_guard_calls": count,
        "source_witness_digest": witness_digest,
        "plural_recovered_locally": True,
        "profile_digest_checked": True,
        "external_issuer_authenticated": False,
        "lean_python_refinement_proved": False,
    }


def _checked_report(value: Any, audit: IsolatedEvidenceAudit
                    ) -> tuple[tuple[tuple[str, int], ...], int, int, int, int, int, str]:
    report = _finite_json(value)
    if type(report) is not dict or set(report) != REPORT_KEYS:
        raise ValueError("child_report_inventory_invalid")
    if (report["version"] != VERSION or report["source_main"] != SOURCE_MAIN
            or report["status"] != SUCCESS or report["plural_recovered_locally"] is not True
            or report["profile_digest_checked"] is not True
            or report["external_issuer_authenticated"] is not False
            or report["lean_python_refinement_proved"] is not False):
        raise ValueError("child_report_status_or_scope_invalid")
    digest = report["source_witness_digest"]
    if (type(digest) is not str or len(digest) != 64
            or any(letter not in "0123456789abcdef" for letter in digest)):
        raise ValueError("child_report_witness_digest_invalid")
    state_counts, host_count, numeric_count, gate_count, eval_count = prior._checked_report(
        report["evaluation_report"], audit,
    )
    count = report["wa_profile_source_guard_calls"]
    if type(count) is not int or count <= 0 or count != eval_count:
        raise ValueError("child_report_every_evaluation_requires_source_guard")
    return state_counts, host_count, numeric_count, gate_count, eval_count, count, digest


def _source_preflight() -> None:
    from scripts.check_kuuos_lean_python_wa_profile_source_sources_v0_16 import check_sources
    issues = check_sources(ROOT)
    if issues:
        raise ValueError("wa_profile_source_preflight_failed:" + ";".join(issues))


def _child_fixture_entry(root: Path) -> dict[str, Any]:
    root = core._fresh_root(root)
    _source_preflight()
    counts = {"DecisionOSWa": 0}
    witness = [""]
    with _guard_profile_source_boundary(root, counts, witness):
        old_report = prior._child_fixture_entry(root)
    audit = audit_local_evidence(root)
    report = _make_child_report(old_report, counts["DecisionOSWa"], witness[0])
    _checked_report(report, audit)
    return report


def build_wa_profile_source_native_fixture(root: Path) -> WaProfileSourceNativeRun:
    """One original native eight-route fixture in a fresh child process.

    Parent postflight recovers the local Plural ledger again and checks its
    digest against the child-reported local witness. This is a point-in-time
    local consistency test; no external signer or historical guard attestation.
    """
    root = core._fresh_root(root)
    _source_preflight()
    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT)
    completed = subprocess.run(
        [sys.executable, "-m", "runtime.kuuos_lean_python_wa_profile_source_native_cycle_v0_16",
         "--fixture-child", str(root)],
        cwd=ROOT, env=env, capture_output=True, text=True, timeout=180, check=False,
    )
    if completed.returncode != 0:
        detail = (completed.stderr or completed.stdout)[-1000:]
        raise RuntimeError(
            "wa_profile_source_native_child_failed:" + str(completed.returncode) + ":" + detail
        )
    if len(completed.stdout.encode("utf-8")) > core.MAX_CHILD_OUTPUT_BYTES:
        raise ValueError("child_report_too_large")
    try:
        child_report = json.loads(completed.stdout)
    except (ValueError, TypeError, RecursionError) as exc:
        raise ValueError("child_report_invalid_json") from exc
    audit = audit_local_evidence(root)
    (states, host_count, numeric_count, gate_count, evaluation_count,
     count, witness_digest) = _checked_report(child_report, audit)
    current_plural = PluralDecisionStore(root / "plural").recover(
        require_snapshot_match=True
    )
    if _fingerprint(_finite_json(current_plural)) != witness_digest:
        raise ValueError("child_witness_differs_from_recovered_local_plural")
    return WaProfileSourceNativeRun(
        status=SUCCESS, state_guard_calls=states, pre_host_guard_calls=host_count,
        wa_numeric_guard_calls=numeric_count, wa_gate_guard_calls=gate_count,
        wa_evaluation_guard_calls=evaluation_count,
        wa_profile_source_guard_calls=count,
        native_audit=audit, source_witness_digest=witness_digest,
    )


def main(argv: list[str]) -> int:
    if len(argv) != 2 or argv[0] != "--fixture-child":
        print("explicit --fixture-child ROOT required", file=sys.stderr)
        return 2
    try:
        report = _child_fixture_entry(Path(argv[1]))
    except Exception as exc:
        print("wa_profile_source_fixture_failed:" + type(exc).__name__ + ":" + str(exc),
              file=sys.stderr)
        return 1
    print(json.dumps(report, ensure_ascii=False, sort_keys=True, allow_nan=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))


__all__ = (
    "VERSION", "SOURCE_MAIN", "SUCCESS", "WaProfileSourceNativeRun",
    "build_wa_profile_source_native_fixture", "audit_local_evidence",
)
