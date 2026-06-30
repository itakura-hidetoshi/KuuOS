#!/usr/bin/env python3
import unittest

from runtime.v111_checkpoint_candidate_validation_runtime import run_v111
from tests.test_kuuos_checkpoint_evidence_envelope_v1_12 import (
    CheckpointEvidenceEnvelopeV112Tests,
)


def run_v112() -> int:
    if run_v111() != 0:
        return 1
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(
        CheckpointEvidenceEnvelopeV112Tests
    )
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1
