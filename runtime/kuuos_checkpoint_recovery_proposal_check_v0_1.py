#!/usr/bin/env python3
from __future__ import annotations

import unittest

from tests.test_kuuos_checkpoint_recovery_proposal_v0_1 import (
    CheckpointRecoveryProposalV01Tests,
)


def run_checkpoint_recovery_proposal_v0_1() -> int:
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(
        CheckpointRecoveryProposalV01Tests
    )
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(run_checkpoint_recovery_proposal_v0_1())
