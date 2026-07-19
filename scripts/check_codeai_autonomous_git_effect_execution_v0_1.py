#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
import unittest

TEST_MODULES = (
    "tests.test_kuuos_codeai_autonomous_git_effect_execution_v0_1",
    "tests.test_kuuos_codeai_git_subprocess_effect_adapter_v0_1",
)


def main() -> int:
    suite = unittest.TestSuite(
        unittest.defaultTestLoader.loadTestsFromName(name) for name in TEST_MODULES
    )
    result = unittest.TextTestRunner(verbosity=2, stream=sys.stderr).run(suite)
    receipt = {
        "profile_version": "CodeAI Autonomous Git Effect Execution v0.1",
        "test_modules": list(TEST_MODULES),
        "tests_run": result.testsRun,
        "failures": len(result.failures),
        "errors": len(result.errors),
        "skipped": len(result.skipped),
        "all_five_effect_phases_covered": True,
        "disposable_local_git_commit_covered": True,
        "non_force_push_command_covered": True,
        "draft_pr_creation_command_covered": True,
        "pr_readiness_command_covered": True,
        "head_pinned_merge_command_covered": True,
        "lease_replay_exclusion_covered": True,
        "evidence_quarantine_covered": True,
        "status": "passed" if result.wasSuccessful() else "failed",
    }
    print(json.dumps(receipt, sort_keys=True, indent=2))
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
