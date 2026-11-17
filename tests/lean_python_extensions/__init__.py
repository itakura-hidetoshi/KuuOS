"""Ordinary discovery of additive Lean/Python extension tests.

The v0.4 native module calls this helper from its standard load_tests hook.
Source preflight runs before test imports. The helper does not run tests or
replace the incoming native suite. Tests remain trusted repository code.
Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from pathlib import Path
from unittest import TestSuite

REQUIRED_TEST_MODULES = (
    "tests.lean_python_extensions.test_mediator_transition_v0_12",
    "tests.lean_python_extensions.test_mediated_native_cycle_v0_12",
    "tests.lean_python_extensions.test_mediator_sources_v0_12",
)


def _case_ids(suite):
    for item in suite:
        if isinstance(item, TestSuite):
            yield from _case_ids(item)
        else:
            yield item.id()


def load_extension_tests(loader):
    """Return the discovered suite with normal test IDs and visible failures.

The fixed original runner selects the native module once. General repository
discovery can also select this package independently; no global deduplication
or protection from arbitrary test-module code is claimed.
"""
    from scripts.check_kuuos_lean_python_mediator_sources_v0_12 import check_sources

    package = Path(__file__).absolute().parent
    root = package.parent.parent
    issues = check_sources(root)
    if issues:
        raise RuntimeError("extension_source_preflight_blocked:" + ";".join(issues))
    error_count = len(loader.errors)
    suite = loader.discover(
        start_dir=str(package), pattern="test_*.py", top_level_dir=str(root),
    )
    # Preserve standard unittest import failures and their original tracebacks.
    # The returned FailedTest will fail the ordinary runner; never drop it.
    if len(loader.errors) != error_count:
        return suite
    ids = list(_case_ids(suite))
    if len(ids) != len(set(ids)):
        raise RuntimeError("duplicate_extension_test_id")
    missing = [
        module for module in REQUIRED_TEST_MODULES
        if not any(test_id.startswith(module + ".") for test_id in ids)
    ]
    if missing:
        raise RuntimeError("required_extension_tests_not_discovered:" + ";".join(missing))
    return suite

