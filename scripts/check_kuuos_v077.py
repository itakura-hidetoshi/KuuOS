#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import replace
import json

from runtime.kuuos_memory_rollback_ledger_v0_76 import MemoryRollbackLedger
from runtime.kuuos_memory_rollback_request_v0_76 import build_memory_rollback_request
from runtime.kuuos_memory_rollback_v0_76 import rollback_memory_commit
from runtime.kuuos_v077_types import BLOCKED, VERIFIED
from runtime.kuuos_v077_verify import (
    verify_committed_memory_state,
    verify_rolled_back_memory_state,
)
from scripts.check_kuuos_memory_rollback_v076 import committed_fixture


def main() -> int:
    source_state, committed_state, commit_receipt = committed_fixture()

    commit_record = verify_committed_memory_state(
        committed_state,
        commit_receipt,
    )
    assert commit_record.status == VERIFIED
    assert commit_record.exact_state_binding
    assert commit_record.exact_payload_binding
    assert commit_record.revision_successor
    assert commit_record.state_chain_preserved
    assert commit_record.authority_consumption_preserved
    assert commit_record.ledger_binding_preserved
    assert commit_record.record_only
    assert commit_record.writes_enabled is False
    assert commit_record.live_application_enabled is False
    assert commit_record.permission_expansion_enabled is False
    assert commit_record.record_digest

    state_tamper = replace(
        committed_state,
        revision=committed_state.revision + 1,
    )
    state_blocked = verify_committed_memory_state(
        state_tamper,
        commit_receipt,
    )
    assert state_blocked.status == BLOCKED
    assert "commit_observed_state_mismatch" in state_blocked.issues

    receipt_tamper = replace(
        commit_receipt,
        selected_kernel_digest="tampered-kernel",
    )
    receipt_blocked = verify_committed_memory_state(
        committed_state,
        receipt_tamper,
    )
    assert receipt_blocked.status == BLOCKED
    assert "commit_receipt_digest_mismatch" in receipt_blocked.issues
    assert "commit_observed_payload_mismatch" in receipt_blocked.issues

    ledger = MemoryRollbackLedger("verification-ledger-v077", 0)
    rollback_request = build_memory_rollback_request(
        "verification-rollback-v077",
        committed_state,
        source_state,
        ledger,
        commit_receipt,
        commit_receipt.applied_at_epoch + 1,
    )
    restored_state, restored_ledger, rollback_receipt = rollback_memory_commit(
        committed_state,
        source_state,
        ledger,
        rollback_request,
        commit_receipt,
    )
    rollback_record = verify_rolled_back_memory_state(
        restored_state,
        restored_ledger,
        rollback_receipt,
        commit_receipt,
    )
    assert rollback_record.status == VERIFIED
    assert rollback_record.exact_state_binding
    assert rollback_record.exact_payload_binding
    assert rollback_record.revision_successor
    assert rollback_record.state_chain_preserved
    assert rollback_record.authority_consumption_preserved
    assert rollback_record.ledger_binding_preserved
    assert rollback_record.record_only
    assert rollback_record.writes_enabled is False
    assert rollback_record.live_application_enabled is False
    assert rollback_record.permission_expansion_enabled is False
    assert rollback_record.record_digest

    rollback_state_tamper = replace(
        restored_state,
        revision=restored_state.revision + 1,
    )
    rollback_state_blocked = verify_rolled_back_memory_state(
        rollback_state_tamper,
        restored_ledger,
        rollback_receipt,
        commit_receipt,
    )
    assert rollback_state_blocked.status == BLOCKED
    assert "rollback_observed_state_mismatch" in rollback_state_blocked.issues

    ledger_tamper = replace(
        restored_ledger,
        revision=restored_ledger.revision + 1,
    )
    ledger_blocked = verify_rolled_back_memory_state(
        restored_state,
        ledger_tamper,
        rollback_receipt,
        commit_receipt,
    )
    assert ledger_blocked.status == BLOCKED
    assert "rollback_observed_ledger_mismatch" in ledger_blocked.issues

    rollback_receipt_tamper = replace(
        rollback_receipt,
        restored_kernel_digest="tampered-restored-kernel",
    )
    rollback_receipt_blocked = verify_rolled_back_memory_state(
        restored_state,
        restored_ledger,
        rollback_receipt_tamper,
        commit_receipt,
    )
    assert rollback_receipt_blocked.status == BLOCKED
    assert "rollback_receipt_digest_mismatch" in rollback_receipt_blocked.issues
    assert "rollback_observed_payload_mismatch" in rollback_receipt_blocked.issues

    print(json.dumps({
        "status": "KUUOS_POST_TRANSITION_VERIFICATION_V0_77_VALIDATED",
        "commit_record_digest": commit_record.record_digest,
        "rollback_record_digest": rollback_record.record_digest,
        "observed_commit_state_digest": commit_record.observed_state_digest,
        "observed_rollback_state_digest": rollback_record.observed_state_digest,
        "observed_rollback_ledger_digest": rollback_record.observed_ledger_digest,
        "checks": [
            "exact-commit-state-binding",
            "exact-commit-payload-binding",
            "commit-authority-consumption",
            "exact-rollback-state-binding",
            "exact-rollback-payload-binding",
            "rollback-ledger-binding",
            "rollback-authority-remains-consumed",
            "state-tamper-rejected",
            "ledger-tamper-rejected",
            "receipt-tamper-rejected",
            "record-only-no-live-effect",
        ],
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
