#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import unittest

from runtime.kuuos_repository_alignment_normal_form_v0_80 import (
    certify_repository_alignment_normal_form,
)
from runtime.kuuos_repository_certificate_chain_v0_82 import (
    advance_repository_certificate_chain,
    certificate_chain_record_issues,
    start_repository_certificate_chain,
)
from runtime.kuuos_repository_snapshot_adapter_v0_79 import (
    capture_explicit_repository_snapshot,
)
from scripts.check_kuuos_repository_live_v079 import contract_paths
from tests.test_kuuos_repository_certificate_chain_v0_82 import (
    RepositoryCertificateChainV082Tests,
)

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(
        RepositoryCertificateChainV082Tests
    )
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if not result.wasSuccessful():
        return 1

    snapshot = capture_explicit_repository_snapshot(ROOT, contract_paths())
    normal_form = certify_repository_alignment_normal_form(snapshot)
    genesis = start_repository_certificate_chain(
        "live-repository-certificate-chain",
        "0" * 40,
        snapshot,
        normal_form,
        max_chain_length=4,
    )
    current = advance_repository_certificate_chain(
        "live-repository-certificate-chain",
        genesis,
        snapshot,
        snapshot,
        "0" * 40,
        "1" * 40,
        (),
    )
    if not (
        certificate_chain_record_issues(genesis) == ()
        and certificate_chain_record_issues(current) == ()
        and current.sequence == 1
        and current.current_score == 0
        and current.current_normal_form_preserved
        and not current.full_recheck_performed
        and not current.rechecked_scope_ids
        and not current.external_approval_required
    ):
        return 1

    print(json.dumps({
        "status": "KUUOS_REPOSITORY_CERTIFICATE_CHAIN_V0_82_VALIDATED",
        "commit_parent_binding": True,
        "changed_path_exactness": True,
        "chain_id_binding": True,
        "record_digest_binding": True,
        "commit_replay_rejected": True,
        "bounded_chain_length": True,
        "live_repository_score": current.current_score,
        "external_approval_required": False,
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
